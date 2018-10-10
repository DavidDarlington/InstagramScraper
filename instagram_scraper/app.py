#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import concurrent.futures
import configparser
import json
import logging
import hashlib
import os
import re
import requests
import sys
import textwrap
import threading
import time
import tqdm
import warnings

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from instagram_scraper.constants import *
from instagram_scraper.exceptions import *
from instagram_scraper.generators import *
from instagram_scraper.helpers import *
from instagram_scraper.use_cases import *
from instagram_scraper.repos import *

try:
    reload(sys)  # Python 2.7
    sys.setdefaultencoding("UTF8")
except NameError:
    pass

try:
    input = raw_input  # Python 2.7
except NameError:
    pass

warnings.filterwarnings('ignore')

log = logging.getLogger(__name__)

input_lock = threading.RLock()


class LockedStream(object):
    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        with input_lock:
            self.file.write(x)

    def flush(self):
        return getattr(self.file, 'flush', lambda: None)()


original_stdout, original_stderr = sys.stdout, sys.stderr
sys.stdout, sys.stderr = map(LockedStream, (sys.stdout, sys.stderr))


def threaded_input(prompt):
    with input_lock:
        try:
            with tqdm.external_write_mode():
                original_stdout.write(prompt)
                original_stdout.flush()
                return sys.stdin.readline()
        except AttributeError:
            original_stdout.write('\n')
            original_stdout.write(prompt)
            original_stdout.flush()
            return sys.stdin.readline()


input = threaded_input


class PartialContentException(Exception):
    pass


class InstagramScraper(object):
    """InstagramScraper scrapes and downloads an instagram user's photos and videos"""

    def __init__(self, **kwargs):
        default_attr = dict(username='', usernames=[], filename=None,
                            login_user=None, login_pass=None,
                            destination='./', retain_username=False, interactive=False,
                            quiet=False, maximum=0, media_metadata=False, latest=False,
                            latest_stamps=False,
                            media_types=['image', 'video', 'story-image', 'story-video'],
                            tag=False, location=False, search_location=False, comments=False,
                            verbose=2, file_log_level=False, include_location=False, filter=None,
                            template='{urlname}', session=get_session_with_retry(), repo_factory=None)

        allowed_attr = list(default_attr.keys())
        default_attr.update(kwargs)

        for key in default_attr:
            if key in allowed_attr:
                self.__dict__[key] = default_attr.get(key)

        # Set logger
        setup_logging(verbose=self.verbose, file_log_level=self.file_log_level)

        # story media type means story-image & story-video
        if 'story' in self.media_types:
            self.media_types.remove('story')
            if 'story-image' not in self.media_types:
                self.media_types.append('story-image')
            if 'story-video' not in self.media_types:
                self.media_types.append('story-video')

        # Read latest_stamps file with ConfigParser
        self.latest_stamps_parser = None
        if self.latest_stamps:
            parser = configparser.ConfigParser()
            parser.read(self.latest_stamps)
            self.latest_stamps_parser = parser
            # If we have a latest_stamps file, latest must be true as it's the common flag
            self.latest = True

        self.posts = []

        self.session.headers = {'user-agent': CHROME_WIN_UA}
        self.session.cookies.set('ig_pr', '1')

        if not self.repo_factory:
            self.repo_factory = RepoFactory(self.session)

        self.cookies = None
        self.logged_in = False
        self.last_scraped_filemtime = 0

        self.current_destination = None
        self.current_user = None
        self.future_to_item = {}

        if default_attr['filter']:
            self.filter = list(self.filter)

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS)
        self.quit = False

    # ========================================================================================
    # 1. get csrf token
    # 2. login
    #       + challenge prompt
    #           - select challenge mode
    #           - send challenge code
    # 3. logout
    # ========================================================================================

    # -------- GET CSRF TOKEN -------------------------------------------------

    def get_csrf_token(self):
        get_csrf_token(observer=self,
                       auth_repo=self.repo_factory.get_auth_repo())

    def get_csrf_token_success(self):
        login(username=self.login_user,
              password=self.login_pass,
              observer=self,
              auth_repo=self.repo_factory.get_auth_repo())

    def get_csrf_token_error(self, exception):
        log.error('get csrf token error: ' + exception.message)

    # -------- LOGIN ----------------------------------------------------------

    def login_success(self):
        self.logged_in = True

    def challenge_prompt(self, challenge_url):
        log.warning('Unable to login due to challenge prompt. Please verify your account at ' + challenge_url)

        if self.interactive:
            log.info('Interactive login challenge solving is enabled.')
            self.login_challenge(challenge_url)
        else:
            log.info('You can pass the -i argument to enable interactive login challenge solving.')
            log.warning('Scraping will be restricted to public accounts.')

    def login_error(self, exception, content):
        log.error('login error: ' + exception.message)
        log.debug(json.dumps(content))
        self._enumerate_errors(content)

        log.warning('falling back to anonymous scraping')

    # -------- SELECT CHALLENGE MODE ----------------------------------------------------------

    def login_challenge(self, challenge_url):
        mode = int(input('Choose a challenge mode (0 - SMS, 1 - Email): '))

        select_challenge_mode(challenge_url=challenge_url,
                              mode=str(mode).strip(),
                              observer=self,
                              challenge_repo=self.repo_factory.get_challenge_repo())

    def select_challenge_mode_success(self, challenge_url):
        code = int(input('Enter code received: '))

        send_challenge_code(challenge_url=challenge_url,
                            code=str(code).strip(),
                            observer=self,
                            challenge_repo=self.repo_factory.get_challenge_repo())

    def select_challenge_mode_error(self, exception):
        log.warning('select challenge mode error: ' + exception.message)

    # -------- SEND CHALLENGE CODE ----------------------------------------------------------

    def send_challenge_code_success(self):
        self.logged_in = True

    def send_challenge_code_error(self, exception, content):
        log.error('send challenge code error: ' + exception.message)
        log.debug(json.dumps(content))
        self._enumerate_errors(content)

    # -------- LOGOUT ----------------------------------------------------------

    def logout(self):
        if not self.logged_in:
            return

        csrf_token = self.session.cookies.get('csrftoken', default=None, domain=DOMAIN)

        logout(csrf_token=csrf_token,
               observer=self,
               auth_repo=self.repo_factory.get_auth_repo())

    def logout_success(self):
        pass

    def logout_error(self, exception):
        log.warning('logout error: ' + exception.message)

    # ========================================================================================
    # ========================================================================================

    # -------- GET USER PROFILE ----------------------------------------------------------

    def get_user_profile_success(self, user):
        self.current_user = user

        self.get_profile_picture()
        self.get_stories()
        self.get_highlights()
        self.get_media()

    def get_user_profile_is_private(self, user):
        self.current_user = user

        log.warning('{0} is private and you are NOT an approved follower'.format(user['username']))

        self.get_profile_picture()

    def get_user_profile_error(self, exception):
        log.warn('get user profile failed - unable to get media: ' + exception.message)

    # -------- GET PROFILE PICTURE ----------------------------------------------------------

    def get_profile_picture(self):
        if 'image' not in self.media_types:
            return

        get_profile_picture(user=self.current_user,
                            observer=self,
                            user_repo=self.repo_factory.get_user_repo())

    def get_profile_picture_success(self, profile_pic_url):
        if self.latest is True and profile_picture_exists(self.current_destination, profile_pic_url):
            return

        item = {
            'urls': [profile_pic_url],
            'username': self.current_user['username'],
            'shortcode': '',
            'created_time': 1286323200,
            '__typename': 'GraphProfilePic'
        }

        for item in tqdm.tqdm([item], desc='Searching {0} for profile pic'.format(self.current_user['username']), unit=" images",
                              ncols=0, disable=self.quiet):
            future = self.executor.submit(self.worker_wrapper, self.download, item, self.current_destination)
            self.future_to_item[future] = item

    def get_profile_picture_is_default(self, user):
        log.info('anonymous profile picture for ' + user['username'] + ' - skipping')

    def get_profile_picture_error(self, exception):
        log.warn('get profile picture failed: ' + exception.message)

    # -------- GET STORIES ----------------------------------------------------------

    def get_stories(self):
        if not self.logged_in or \
                ('story-image' not in self.media_types and 'story-video' not in self.media_types):
            return

        get_stories(user=self.current_user,
                    observer=self,
                    story_repo=self.repo_factory.get_story_repo())

    def get_stories_success(self, stories):
        iter = 0

        for item in tqdm.tqdm(stories, desc='Searching {0} for stories'.format(self.current_user['username']), unit=" media",
                              disable=self.quiet):
            if has_selected_story_media_types(item, self.media_types) and self.is_new_media(item):
                item['username'] = self.current_user['username']
                item['shortcode'] = ''
                future = self.executor.submit(self.worker_wrapper, self.download, item, self.current_destination)
                self.future_to_item[future] = item

            iter = iter + 1
            if self.maximum != 0 and iter >= self.maximum:
                break

    def get_stories_empty(self):
        log.info('no stories found for user: {0} (id={1})'.format(self.current_user['username'], self.current_user['id']))

    def get_stories_error(self, exception):
        log.error('get stories failed: ' + exception.message)

    # -------- GET HIGHLIGHTS ----------------------------------------------------------

    def get_highlights(self):
        if not self.logged_in or \
                ('story-image' not in self.media_types and 'story-video' not in self.media_types):
            return

        get_highlights(user=self.current_user,
                       observer=self,
                       highlight_repo=self.repo_factory.get_highlight_repo())

    def get_highlights_empty(self):
        log.info('no highlights found for user: {0} (id={1})'.format(self.current_user['username'], self.current_user['id']))

    def get_highlights_success(self, media):
        iter = 0

        for item in tqdm.tqdm(media, desc='Searching {0} for highlights'.format(self.current_user['username']), unit=" media",
                              disable=self.quiet):
            if has_selected_story_media_types(item, self.media_types) and self.is_new_media(item):
                item['username'] = self.current_user['username']
                item['shortcode'] = ''
                future = self.executor.submit(self.worker_wrapper, self.download, item, self.current_destination)
                self.future_to_item[future] = item

            iter = iter + 1
            if self.maximum != 0 and iter >= self.maximum:
                break

    def get_highlights_error(self, exception):
        log.error('get highlights failed: ' + exception.message)

    # -------- GET MEDIA ----------------------------------------------------------

    def get_media(self):
        """Scrapes the user's posts for media."""
        if 'image' not in self.media_types and 'video' not in self.media_types:
            return

        username = self.current_user['username']

        if self.include_location:
            media_exec = concurrent.futures.ThreadPoolExecutor(max_workers=5)

        iter = 0
        for item in tqdm.tqdm(query_media_gen(user=self.current_user,
                                              last_scraped_time=self.last_scraped_filemtime,
                                              media_repo=self.repo_factory.get_media_repo()),
                              desc='Searching {0} for posts'.format(username),
                              unit=' media', disable=self.quiet):

            process_node(node=item,
                         include_location=self.include_location,
                         media_repo=self.repo_factory.get_media_repo())

            # -Filter command line
            if self.filter:
                if 'tags' in item:
                    filtered = any(x in item['tags'] for x in self.filter)
                    if self.has_selected_media_types(item) and self.is_new_media(item) and filtered:
                        item['username'] = username

                        future = self.executor.submit(self.worker_wrapper, self.download, item, self.current_destination)
                        self.future_to_item[future] = item
                else:
                    # For when filter is on but media doesnt contain tags
                    pass
            else:
                if self.has_selected_media_types(item) and self.is_new_media(item):
                    item['username'] = username
                    future = self.executor.submit(self.worker_wrapper, self.download, item, self.current_destination)
                    self.future_to_item[future] = item

            if self.include_location:
                item['username'] = username
                media_exec.submit(self.worker_wrapper, self.__get_location, item)

            if self.comments:
                item['username'] = username
                item['comments'] = {'data': list(self.query_comments_gen(item['shortcode']))}

            if self.media_metadata or self.comments or self.include_location:
                item['username'] = username
                self.posts.append(item)

            iter = iter + 1
            if self.maximum != 0 and iter >= self.maximum:
                break

    # ========================================================================================
    # ========================================================================================

    def worker_wrapper(self, fn, *args, **kwargs):
        try:
            if self.quit:
                return
            return fn(*args, **kwargs)
        except:
            log.debug("Exception in worker thread", exc_info=sys.exc_info())
            raise

    def sleep(self, secs):
        min_delay = 1
        for _ in range(secs // min_delay):
            time.sleep(min_delay)
            if self.quit:
                return
        time.sleep(secs % min_delay)

    def _retry_prompt(self, url, exception_message):
        """Show prompt and return True: retry, False: ignore, None: abort"""
        answer = input('Repeated error {0}\n(A)bort, (I)gnore, (R)etry or retry (F)orever?'.format(exception_message))
        if answer:
            answer = answer[0].upper()
            if answer == 'I':
                log.info('The user has chosen to ignore {0}'.format(url))
                return False
            elif answer == 'R':
                return True
            elif answer == 'F':
                log.info('The user has chosen to retry forever')
                global MAX_RETRIES
                MAX_RETRIES = sys.maxsize
                return True
            else:
                log.info('The user has chosen to abort')
                return None

    def safe_get(self, *args, **kwargs):
        # out of the box solution
        # session.mount('https://', HTTPAdapter(max_retries=...))
        # only covers failed DNS lookups, socket connections and connection timeouts
        # It doesnt work when server terminate connection while response is downloaded
        retry = 0
        retry_delay = RETRY_DELAY
        while True:
            if self.quit:
                return
            try:
                response = self.session.get(timeout=CONNECT_TIMEOUT, cookies=self.cookies, *args, **kwargs)
                if response.status_code == 404:
                    return
                response.raise_for_status()
                content_length = response.headers.get('Content-Length')
                if content_length is not None and len(response.content) != int(content_length):
                    # if content_length is None we repeat anyway to get size and be confident
                    raise PartialContentException('Partial response')
                return response
            except (KeyboardInterrupt):
                raise
            except (requests.exceptions.RequestException, PartialContentException) as e:
                if 'url' in kwargs:
                    url = kwargs['url']
                elif len(args) > 0:
                    url = args[0]
                if retry < MAX_RETRIES:
                    log.warning('Retry after exception {0} on {1}'.format(repr(e), url))
                    self.sleep(retry_delay)
                    retry_delay = min(2 * retry_delay, MAX_RETRY_DELAY)
                    retry = retry + 1
                    continue
                else:
                    keep_trying = self._retry_prompt(url, repr(e))
                    if keep_trying == True:
                        retry = 0
                        continue
                    elif keep_trying == False:
                        return
                raise

    def get_json(self, *args, **kwargs):
        """Retrieve text from url. Return text as string or None if no data present """
        resp = self.safe_get(*args, **kwargs)

        if resp is not None:
            return resp.text

    def query_comments_gen(self, shortcode, end_cursor=''):
        """Generator for comments."""
        comments, end_cursor = self.__query_comments(shortcode, end_cursor)

        if comments:
            try:
                while True:
                    for item in comments:
                        yield item

                    if end_cursor:
                        comments, end_cursor = self.__query_comments(shortcode, end_cursor)
                    else:
                        return
            except ValueError:
                log.exception('Failed to query comments for shortcode ' + shortcode)

    def __query_comments(self, shortcode, end_cursor=''):
        params = QUERY_COMMENTS_VARS.format(shortcode, end_cursor)
        self.update_ig_gis_header(params)

        resp = self.get_json(QUERY_COMMENTS.format(params))

        if resp is not None:
            payload = json.loads(resp)['data']['shortcode_media']

            if payload:
                container = payload['edge_media_to_comment']
                comments = [node['node'] for node in container['edges']]
                end_cursor = container['page_info']['end_cursor']
                return comments, end_cursor

        return None, None

    def scrape_hashtag(self):
        self.__scrape_query(self.query_hashtag_gen)

    def scrape_location(self):
        self.__scrape_query(self.query_location_gen)

    def __scrape_query(self, media_generator,
                       executor=concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT_DOWNLOADS)):
        """Scrapes the specified value for posted media."""
        self.quit = False

        try:
            for username in self.usernames:
                self.posts = []
                self.last_scraped_filemtime = 0

                greatest_timestamp = 0
                future_to_item = {}

                destination = get_destination_dir(destination=self.destination,
                                          retain_username=self.retain_username,
                                          username=username)

                self.last_scraped_filemtime = self._get_last_scraped_filetime(username, destination)

                if self.include_location:
                    media_exec = concurrent.futures.ThreadPoolExecutor(max_workers=5)

                iter = 0
                for item in tqdm.tqdm(media_generator(username), desc='Searching {0} for posts'.format(username),
                                      unit=" media",
                                      disable=self.quiet):
                    if ((item['is_video'] is False and 'image' in self.media_types) or \
                        (item['is_video'] is True and 'video' in self.media_types)
                    ) and self.is_new_media(item):
                        future = executor.submit(self.worker_wrapper, self.download, item, destination)
                        future_to_item[future] = item

                    if self.include_location and 'location' not in item:
                        media_exec.submit(self.worker_wrapper, self.__get_location, item)

                    if self.comments:
                        item['edge_media_to_comment']['data'] = list(self.query_comments_gen(item['shortcode']))

                    if self.media_metadata or self.comments or self.include_location:
                        self.posts.append(item)

                    iter = iter + 1
                    if self.maximum != 0 and iter >= self.maximum:
                        break

                if future_to_item:
                    for future in tqdm.tqdm(concurrent.futures.as_completed(future_to_item),
                                            total=len(future_to_item),
                                            desc='Downloading', disable=self.quiet):
                        item = future_to_item[future]

                        if future.exception() is not None:
                            log.warning(
                                'Media for {0} at {1} generated an exception: {2}'.format(username, item['urls'],
                                                                                          future.exception()))
                        else:
                            timestamp = get_timestamp(item)
                            if timestamp > greatest_timestamp:
                                greatest_timestamp = timestamp
                # Even bother saving it?
                if greatest_timestamp > self.last_scraped_filemtime:
                    set_last_scraped_timestamp(parser=self.latest_stamps_parser,
                                               latest_stamps_file=self.latest_stamps,
                                               username=username,
                                               timestamp=greatest_timestamp)

                if (self.media_metadata or self.comments or self.include_location) and self.posts:
                    save_json(self.posts, '{0}/{1}.json'.format(destination, username))
        finally:
            self.quit = True

    def query_hashtag_gen(self, hashtag):
        return self.__query_gen(QUERY_HASHTAG, QUERY_HASHTAG_VARS, 'hashtag', hashtag)

    def query_location_gen(self, location):
        return self.__query_gen(QUERY_LOCATION, QUERY_LOCATION_VARS, 'location', location)

    def __query_gen(self, url, variables, entity_name, query, end_cursor=''):
        """Generator for hashtag and location."""
        nodes, end_cursor = self.__query(url, variables, entity_name, query, end_cursor)

        if nodes:
            try:
                while True:
                    for node in nodes:
                        yield node

                    if end_cursor:
                        nodes, end_cursor = self.__query(url, variables, entity_name, query, end_cursor)
                    else:
                        return
            except ValueError:
                log.exception('Failed to query ' + query)

    def __query(self, url, variables, entity_name, query, end_cursor):
        params = variables.format(query, end_cursor)
        self.update_ig_gis_header(params)

        resp = self.get_json(url.format(params))

        if resp is not None:
            payload = json.loads(resp)['data'][entity_name]

            if payload:
                nodes = []

                if end_cursor == '':
                    top_posts = payload['edge_' + entity_name + '_to_top_posts']
                    nodes.extend(self._get_nodes(top_posts))

                posts = payload['edge_' + entity_name + '_to_media']

                nodes.extend(self._get_nodes(posts))
                end_cursor = posts['page_info']['end_cursor']
                return nodes, end_cursor

        return None, None

    def _get_nodes(self, container):
        return [self.augment_node(node['node']) for node in container['edges']]

    def augment_node(self, node):
        self.extract_tags(node)

        details = None
        if self.include_location and 'location' not in node:
            details = self.__get_media_details(node['shortcode'])
            node['location'] = details.get('location') if details else None

        if 'urls' not in node:
            node['urls'] = []

        if node['is_video'] and 'video_url' in node:
            node['urls'] = [node['video_url']]
        elif '__typename' in node and node['__typename'] == 'GraphImage':
            node['urls'] = [self.get_original_image(node['display_url'])]
        else:
            if details is None:
                details = self.__get_media_details(node['shortcode'])

            if details:
                if '__typename' in details and details['__typename'] == 'GraphVideo':
                    node['urls'] = [details['video_url']]
                elif '__typename' in details and details['__typename'] == 'GraphSidecar':
                    urls = []
                    for carousel_item in details['edge_sidecar_to_children']['edges']:
                        urls += self.augment_node(carousel_item['node'])['urls']
                    node['urls'] = urls
                else:
                    node['urls'] = [self.get_original_image(details['display_url'])]

        return node

    def __get_media_details(self, shortcode):
        resp = self.get_json(VIEW_MEDIA_URL.format(shortcode))

        if resp is not None:
            try:
                return json.loads(resp)['graphql']['shortcode_media']
            except ValueError:
                log.warning('Failed to get media details for ' + shortcode)

        else:
            log.warning('Failed to get media details for ' + shortcode)

    def __get_location(self, item):
        code = item.get('shortcode', item.get('code'))

        if code:
            details = self.__get_media_details(code)
            item['location'] = details.get('location')

    def scrape(self):
        """Crawls through and downloads user's media"""
        try:
            for username in self.usernames:
                self.posts = []
                self.last_scraped_filemtime = 0

                greatest_timestamp = 0
                future_to_item = {}

                destination = get_destination_dir(destination=self.destination,
                                                  retain_username=self.retain_username,
                                                  username=username)

                self.last_scraped_filemtime = self._get_last_scraped_filetime(username, destination)

                self.current_destination = destination

                get_user_profile(username=username,
                                 observer=self,
                                 user_repo=self.repo_factory.get_user_repo())

                try:
                    if future_to_item:
                        for future in tqdm.tqdm(concurrent.futures.as_completed(future_to_item),
                                                total=len(future_to_item),
                                                desc='Downloading', disable=self.quiet):
                            item = future_to_item[future]

                            if future.exception() is not None:
                                log.error(
                                    'Media at {0} generated an exception: {1}'.format(item['urls'], future.exception()))
                            else:
                                timestamp = get_timestamp(item)

                                if timestamp > greatest_timestamp:
                                    greatest_timestamp = timestamp

                    if greatest_timestamp > self.last_scraped_filemtime:
                        set_last_scraped_timestamp(parser=self.latest_stamps_parser,
                                                   latest_stamps_file=self.latest_stamps,
                                                   username=username,
                                                   timestamp=greatest_timestamp)

                    if (self.media_metadata or self.comments or self.include_location) and self.posts:
                        save_json(self.posts, '{0}/{1}.json'.format(destination, username))
                except ValueError:
                    log.error("unable to scrape user - %s" % username)
        finally:
            self.logout()

    def query_media_gen(self, user, end_cursor=''):
        """Generator for media."""
        media, end_cursor = self.__query_media(user['id'], end_cursor)

        if media:
            try:
                while True:
                    for item in media:
                        if not self.is_new_media(item):
                            return
                        yield item

                    if end_cursor:
                        media, end_cursor = self.__query_media(user['id'], end_cursor)
                    else:
                        return
            except ValueError:
                log.exception('Failed to query media for user ' + user['username'])

    def __query_media(self, id, end_cursor=''):
        params = QUERY_MEDIA_VARS.format(id, end_cursor)
        self.update_ig_gis_header(params)

        resp = self.get_json(QUERY_MEDIA.format(params))

        if resp is not None:
            payload = json.loads(resp)['data']['user']

            if payload:
                container = payload['edge_owner_to_timeline_media']
                nodes = self._get_nodes(container)
                end_cursor = container['page_info']['end_cursor']
                return nodes, end_cursor

        return None, None

    def get_ig_gis(self, rhx_gis, params):
        data = rhx_gis + ":" + params
        if sys.version_info.major >= 3:
            return hashlib.md5(data.encode('utf-8')).hexdigest()
        else:
            return hashlib.md5(data).hexdigest()

    def update_ig_gis_header(self, params):
        self.session.headers.update({
            'x-instagram-gis': self.get_ig_gis(
                self.session.rhx_gis,
                params
            )
        })

    def has_selected_media_types(self, item):
        filetypes = {'jpg': 0, 'mp4': 0}

        for url in item['urls']:
            ext = get_file_extension(url)
            if ext not in filetypes:
                filetypes[ext] = 0
            filetypes[ext] += 1

        if ('image' in self.media_types and filetypes['jpg'] > 0) or \
                ('video' in self.media_types and filetypes['mp4'] > 0):
            return True

        return False

    def extract_tags(self, item):
        """Extracts the hashtags from the caption text."""
        caption_text = ''
        if 'caption' in item and item['caption']:
            if isinstance(item['caption'], dict):
                caption_text = item['caption']['text']
            else:
                caption_text = item['caption']

        elif 'edge_media_to_caption' in item and item['edge_media_to_caption'] and item['edge_media_to_caption'][
            'edges']:
            caption_text = item['edge_media_to_caption']['edges'][0]['node']['text']

        if caption_text:
            # include words and emojis
            item['tags'] = re.findall(
                r"(?<!&)#(\w+|(?:[\xA9\xAE\u203C\u2049\u2122\u2139\u2194-\u2199\u21A9\u21AA\u231A\u231B\u2328\u2388\u23CF\u23E9-\u23F3\u23F8-\u23FA\u24C2\u25AA\u25AB\u25B6\u25C0\u25FB-\u25FE\u2600-\u2604\u260E\u2611\u2614\u2615\u2618\u261D\u2620\u2622\u2623\u2626\u262A\u262E\u262F\u2638-\u263A\u2648-\u2653\u2660\u2663\u2665\u2666\u2668\u267B\u267F\u2692-\u2694\u2696\u2697\u2699\u269B\u269C\u26A0\u26A1\u26AA\u26AB\u26B0\u26B1\u26BD\u26BE\u26C4\u26C5\u26C8\u26CE\u26CF\u26D1\u26D3\u26D4\u26E9\u26EA\u26F0-\u26F5\u26F7-\u26FA\u26FD\u2702\u2705\u2708-\u270D\u270F\u2712\u2714\u2716\u271D\u2721\u2728\u2733\u2734\u2744\u2747\u274C\u274E\u2753-\u2755\u2757\u2763\u2764\u2795-\u2797\u27A1\u27B0\u27BF\u2934\u2935\u2B05-\u2B07\u2B1B\u2B1C\u2B50\u2B55\u3030\u303D\u3297\u3299]|\uD83C[\uDC04\uDCCF\uDD70\uDD71\uDD7E\uDD7F\uDD8E\uDD91-\uDD9A\uDE01\uDE02\uDE1A\uDE2F\uDE32-\uDE3A\uDE50\uDE51\uDF00-\uDF21\uDF24-\uDF93\uDF96\uDF97\uDF99-\uDF9B\uDF9E-\uDFF0\uDFF3-\uDFF5\uDFF7-\uDFFF]|\uD83D[\uDC00-\uDCFD\uDCFF-\uDD3D\uDD49-\uDD4E\uDD50-\uDD67\uDD6F\uDD70\uDD73-\uDD79\uDD87\uDD8A-\uDD8D\uDD90\uDD95\uDD96\uDDA5\uDDA8\uDDB1\uDDB2\uDDBC\uDDC2-\uDDC4\uDDD1-\uDDD3\uDDDC-\uDDDE\uDDE1\uDDE3\uDDEF\uDDF3\uDDFA-\uDE4F\uDE80-\uDEC5\uDECB-\uDED0\uDEE0-\uDEE5\uDEE9\uDEEB\uDEEC\uDEF0\uDEF3]|\uD83E[\uDD10-\uDD18\uDD80-\uDD84\uDDC0]|(?:0\u20E3|1\u20E3|2\u20E3|3\u20E3|4\u20E3|5\u20E3|6\u20E3|7\u20E3|8\u20E3|9\u20E3|#\u20E3|\\*\u20E3|\uD83C(?:\uDDE6\uD83C(?:\uDDEB|\uDDFD|\uDDF1|\uDDF8|\uDDE9|\uDDF4|\uDDEE|\uDDF6|\uDDEC|\uDDF7|\uDDF2|\uDDFC|\uDDE8|\uDDFA|\uDDF9|\uDDFF|\uDDEA)|\uDDE7\uD83C(?:\uDDF8|\uDDED|\uDDE9|\uDDE7|\uDDFE|\uDDEA|\uDDFF|\uDDEF|\uDDF2|\uDDF9|\uDDF4|\uDDE6|\uDDFC|\uDDFB|\uDDF7|\uDDF3|\uDDEC|\uDDEB|\uDDEE|\uDDF6|\uDDF1)|\uDDE8\uD83C(?:\uDDF2|\uDDE6|\uDDFB|\uDDEB|\uDDF1|\uDDF3|\uDDFD|\uDDF5|\uDDE8|\uDDF4|\uDDEC|\uDDE9|\uDDF0|\uDDF7|\uDDEE|\uDDFA|\uDDFC|\uDDFE|\uDDFF|\uDDED)|\uDDE9\uD83C(?:\uDDFF|\uDDF0|\uDDEC|\uDDEF|\uDDF2|\uDDF4|\uDDEA)|\uDDEA\uD83C(?:\uDDE6|\uDDE8|\uDDEC|\uDDF7|\uDDEA|\uDDF9|\uDDFA|\uDDF8|\uDDED)|\uDDEB\uD83C(?:\uDDF0|\uDDF4|\uDDEF|\uDDEE|\uDDF7|\uDDF2)|\uDDEC\uD83C(?:\uDDF6|\uDDEB|\uDDE6|\uDDF2|\uDDEA|\uDDED|\uDDEE|\uDDF7|\uDDF1|\uDDE9|\uDDF5|\uDDFA|\uDDF9|\uDDEC|\uDDF3|\uDDFC|\uDDFE|\uDDF8|\uDDE7)|\uDDED\uD83C(?:\uDDF7|\uDDF9|\uDDF2|\uDDF3|\uDDF0|\uDDFA)|\uDDEE\uD83C(?:\uDDF4|\uDDE8|\uDDF8|\uDDF3|\uDDE9|\uDDF7|\uDDF6|\uDDEA|\uDDF2|\uDDF1|\uDDF9)|\uDDEF\uD83C(?:\uDDF2|\uDDF5|\uDDEA|\uDDF4)|\uDDF0\uD83C(?:\uDDED|\uDDFE|\uDDF2|\uDDFF|\uDDEA|\uDDEE|\uDDFC|\uDDEC|\uDDF5|\uDDF7|\uDDF3)|\uDDF1\uD83C(?:\uDDE6|\uDDFB|\uDDE7|\uDDF8|\uDDF7|\uDDFE|\uDDEE|\uDDF9|\uDDFA|\uDDF0|\uDDE8)|\uDDF2\uD83C(?:\uDDF4|\uDDF0|\uDDEC|\uDDFC|\uDDFE|\uDDFB|\uDDF1|\uDDF9|\uDDED|\uDDF6|\uDDF7|\uDDFA|\uDDFD|\uDDE9|\uDDE8|\uDDF3|\uDDEA|\uDDF8|\uDDE6|\uDDFF|\uDDF2|\uDDF5|\uDDEB)|\uDDF3\uD83C(?:\uDDE6|\uDDF7|\uDDF5|\uDDF1|\uDDE8|\uDDFF|\uDDEE|\uDDEA|\uDDEC|\uDDFA|\uDDEB|\uDDF4)|\uDDF4\uD83C\uDDF2|\uDDF5\uD83C(?:\uDDEB|\uDDF0|\uDDFC|\uDDF8|\uDDE6|\uDDEC|\uDDFE|\uDDEA|\uDDED|\uDDF3|\uDDF1|\uDDF9|\uDDF7|\uDDF2)|\uDDF6\uD83C\uDDE6|\uDDF7\uD83C(?:\uDDEA|\uDDF4|\uDDFA|\uDDFC|\uDDF8)|\uDDF8\uD83C(?:\uDDFB|\uDDF2|\uDDF9|\uDDE6|\uDDF3|\uDDE8|\uDDF1|\uDDEC|\uDDFD|\uDDF0|\uDDEE|\uDDE7|\uDDF4|\uDDF8|\uDDED|\uDDE9|\uDDF7|\uDDEF|\uDDFF|\uDDEA|\uDDFE)|\uDDF9\uD83C(?:\uDDE9|\uDDEB|\uDDFC|\uDDEF|\uDDFF|\uDDED|\uDDF1|\uDDEC|\uDDF0|\uDDF4|\uDDF9|\uDDE6|\uDDF3|\uDDF7|\uDDF2|\uDDE8|\uDDFB)|\uDDFA\uD83C(?:\uDDEC|\uDDE6|\uDDF8|\uDDFE|\uDDF2|\uDDFF)|\uDDFB\uD83C(?:\uDDEC|\uDDE8|\uDDEE|\uDDFA|\uDDE6|\uDDEA|\uDDF3)|\uDDFC\uD83C(?:\uDDF8|\uDDEB)|\uDDFD\uD83C\uDDF0|\uDDFE\uD83C(?:\uDDF9|\uDDEA)|\uDDFF\uD83C(?:\uDDE6|\uDDF2|\uDDFC))))[\ufe00-\ufe0f\u200d]?)+",
                caption_text, re.UNICODE)
            item['tags'] = list(set(item['tags']))

        return item

    def get_original_image(self, url):
        """Gets the full-size image from the specified url."""
        # these path parts somehow prevent us from changing the rest of media url
        # url = re.sub(r'/vp/[0-9A-Fa-f]{32}/[0-9A-Fa-f]{8}/', '/', url)
        # remove dimensions to get largest image
        # url = re.sub(r'/[sp]\d{3,}x\d{3,}/', '/', url)
        # get non-square image if one exists
        # url = re.sub(r'/c\d{1,}.\d{1,}.\d{1,}.\d{1,}/', '/', url)
        return url

    def download(self, item, save_dir='./'):
        """Downloads the media file."""
        for full_url, base_name in self.templatefilename(item):
            url = full_url.split('?')[0]  # try the static url first, stripping parameters

            file_path = os.path.join(save_dir, base_name)

            if not os.path.exists(os.path.dirname(file_path)):
                make_destination_dir(destination_path=os.path.dirname(file_path))

            if not os.path.isfile(file_path):
                headers = {'Host': urlparse(url).hostname}

                part_file = file_path + '.part'
                downloaded = 0
                total_length = None
                with open(part_file, 'wb') as media_file:
                    try:
                        retry = 0
                        retry_delay = RETRY_DELAY
                        while (True):
                            if self.quit:
                                return
                            try:
                                downloaded_before = downloaded
                                headers['Range'] = 'bytes={0}-'.format(downloaded_before)

                                with self.session.get(url, cookies=self.cookies, headers=headers, stream=True,
                                                      timeout=CONNECT_TIMEOUT) as response:
                                    if response.status_code == 404:
                                        # instagram don't lie on this
                                        break
                                    if response.status_code == 403 and url != full_url:
                                        # see issue #254
                                        url = full_url
                                        continue
                                    response.raise_for_status()

                                    if response.status_code == 206:
                                        try:
                                            match = re.match(r'bytes (?P<first>\d+)-(?P<last>\d+)/(?P<size>\d+)',
                                                             response.headers['Content-Range'])
                                            range_file_position = int(match.group('first'))
                                            if range_file_position != downloaded_before:
                                                raise Exception()
                                            total_length = int(match.group('size'))
                                            media_file.truncate(total_length)
                                        except:
                                            raise requests.exceptions.InvalidHeader(
                                                'Invalid range response "{0}" for requested "{1}"'.format(
                                                    response.headers.get('Content-Range'), headers.get('Range')))
                                    elif response.status_code == 200:
                                        if downloaded_before != 0:
                                            downloaded_before = 0
                                            downloaded = 0
                                            media_file.seek(0)
                                        content_length = response.headers.get('Content-Length')
                                        if content_length is None:
                                            log.warning(
                                                'No Content-Length in response, the file {0} may be partially downloaded'.format(
                                                    base_name))
                                        else:
                                            total_length = int(content_length)
                                            media_file.truncate(total_length)
                                    else:
                                        raise PartialContentException('Wrong status code {0}', response.status_code)

                                    for chunk in response.iter_content(chunk_size=64 * 1024):
                                        if chunk:
                                            downloaded += len(chunk)
                                            media_file.write(chunk)
                                        if self.quit:
                                            return

                                if downloaded != total_length and total_length is not None:
                                    raise PartialContentException(
                                        'Got first {0} bytes from {1}'.format(downloaded, total_length))

                                break

                            # In case of exception part_file is not removed on purpose,
                            # it is easier to examine it later when analyzing logs.
                            # Please do not add os.remove here.
                            except (KeyboardInterrupt):
                                raise
                            except (requests.exceptions.RequestException, PartialContentException) as e:
                                if downloaded - downloaded_before > 0:
                                    # if we got some data on this iteration do not count it as a failure
                                    log.warning('Continue after exception {0} on {1}'.format(repr(e), url))
                                    retry = 0  # the next fail will be first in a row with no data
                                    continue
                                if retry < MAX_RETRIES:
                                    log.warning('Retry after exception {0} on {1}'.format(repr(e), url))
                                    self.sleep(retry_delay)
                                    retry_delay = min(2 * retry_delay, MAX_RETRY_DELAY)
                                    retry = retry + 1
                                    continue
                                else:
                                    keep_trying = self._retry_prompt(url, repr(e))
                                    if keep_trying == True:
                                        retry = 0
                                        continue
                                    elif keep_trying == False:
                                        break
                                raise
                    finally:
                        media_file.truncate(downloaded)

                if downloaded == total_length or total_length is None:
                    os.rename(part_file, file_path)
                    timestamp = get_timestamp(item)
                    file_time = int(timestamp if timestamp else time.time())
                    os.utime(file_path, (file_time, file_time))

    def templatefilename(self, item):
        for url in item['urls']:
            filename, extension = os.path.splitext(os.path.split(url.split('?')[0])[1])
            try:
                template = self.template
                template_values = {
                    'username': item['username'],
                    'urlname': filename,
                    'shortcode': str(item['shortcode']),
                    'mediatype': item['__typename'][5:],
                    'datetime': time.strftime('%Y%m%d %Hh%Mm%Ss',
                                              time.localtime(get_timestamp(item))),
                    'date': time.strftime('%Y%m%d', time.localtime(get_timestamp(item))),
                    'year': time.strftime('%Y', time.localtime(get_timestamp(item))),
                    'month': time.strftime('%m', time.localtime(get_timestamp(item))),
                    'day': time.strftime('%d', time.localtime(get_timestamp(item))),
                    'h': time.strftime('%Hh', time.localtime(get_timestamp(item))),
                    'm': time.strftime('%Mm', time.localtime(get_timestamp(item))),
                    's': time.strftime('%Ss', time.localtime(get_timestamp(item)))}

                customfilename = str(template.format(**template_values) + extension)
                yield url, customfilename
            except KeyError:
                customfilename = str(filename + extension)
                yield url, customfilename

    def is_new_media(self, item):
        """Returns True if the media is new."""
        if self.latest is False or self.last_scraped_filemtime == 0:
            return True

        current_timestamp = get_timestamp(item)
        return current_timestamp > 0 and current_timestamp > self.last_scraped_filemtime

    def _get_last_scraped_filetime(self, username, path):
        if self.latest_stamps_parser:
            return get_last_scraped_timestamp(parser=self.latest_stamps_parser, username=username)
        elif os.path.isdir(path):
            return get_last_scraped_filemtime(path)

        return 0

    # -------- search locations ----------------------------------------------------------

    def search_locations(self, query):
        search_locations(query=query,
                         observer=self,
                         location_repo=self.repo_factory.get_location_repo())

    def search_locations_success(self, places):
        for item in places[0:5]:
            place = item['place']
            print('location-id: {0}, title: {1}, subtitle: {2}, city: {3}, lat: {4}, lng: {5}'.format(
                place['location']['pk'],
                place['title'],
                place['subtitle'],
                place['location']['city'],
                place['location']['lat'],
                place['location']['lng']
            ))

    def no_locations_found(self, exception):
        self.search_locations_error(exception)

    def search_locations_error(self, exception):
        log.error('search locations failed: ' + exception.message)

    def _enumerate_errors(self, content):
        if not content.get('errors'):
            return

        for count, error in enumerate(content['errors'].get('error')):
            count += 1
            log.error('Session error %(count)s: "%(error)s"' % locals())


def main():
    parser = argparse.ArgumentParser(
        description="instagram-scraper scrapes and downloads an instagram user's photos and videos.",
        epilog=textwrap.dedent("""
        You can hide your credentials from the history, by reading your
        username from a local file:

        $ instagram-scraper @insta_args.txt user_to_scrape

        with insta_args.txt looking like this:
        -u=my_username
        -p=my_password

        You can add all arguments you want to that file, just remember to have
        one argument per line.

        Customize filename:
        by adding option --template or -T
        Default is: {urlname}
        And there are some option:
        {username}: Instagram user(s) to scrape.
        {shortcode}: post shortcode, but profile_pic and story are none.
        {urlname}: filename form url.
        {mediatype}: type of media.
        {datetime}: date and time that photo/video post on,
                     format is: 20180101 01h01m01s
        {date}: date that photo/video post on,
                 format is: 20180101
        {year}: format is: 2018
        {month}: format is: 01-12
        {day}: format is: 01-31
        {h}: hour, format is: 00-23h
        {m}: minute, format is 00-59m
        {s}: second, format is 00-59s

        """),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars='@')

    parser.add_argument('username', help='Instagram user(s) to scrape', nargs='*')
    parser.add_argument('--destination', '-d', default='./', help='Download destination')
    parser.add_argument('--login-user', '--login_user', '-u', default=None, help='Instagram login user', required=True)
    parser.add_argument('--login-pass', '--login_pass', '-p', default=None, help='Instagram login password',
                        required=True)
    parser.add_argument('--filename', '-f', help='Path to a file containing a list of users to scrape')
    parser.add_argument('--quiet', '-q', default=False, action='store_true', help='Be quiet while scraping')
    parser.add_argument('--maximum', '-m', type=int, default=0, help='Maximum number of items to scrape')
    parser.add_argument('--retain-username', '--retain_username', '-n', action='store_true', default=False,
                        help='Creates username subdirectory when destination flag is set')
    parser.add_argument('--media-metadata', '--media_metadata', action='store_true', default=False,
                        help='Save media metadata to json file')
    parser.add_argument('--include-location', '--include_location', action='store_true', default=False,
                        help='Include location data when saving media metadata')
    parser.add_argument('--media-types', '--media_types', '-t', nargs='+', default=['image', 'video', 'story'],
                        help='Specify media types to scrape')
    parser.add_argument('--latest', action='store_true', default=False, help='Scrape new media since the last scrape')
    parser.add_argument('--latest-stamps', '--latest_stamps', default=None,
                        help='Scrape new media since timestamps by user in specified file')
    parser.add_argument('--tag', action='store_true', default=False, help='Scrape media using a hashtag')
    parser.add_argument('--filter', default=None, help='Filter by tags in user posts', nargs='*')
    parser.add_argument('--location', action='store_true', default=False, help='Scrape media using a location-id')
    parser.add_argument('--search-location', action='store_true', default=False, help='Search for locations by name')
    parser.add_argument('--comments', action='store_true', default=False, help='Save post comments to json file')
    parser.add_argument('--interactive', '-i', action='store_true', default=False,
                        help='Enable interactive login challenge solving')
    parser.add_argument('--retry-forever', action='store_true', default=False,
                        help='Retry download attempts endlessly when errors are received')
    parser.add_argument('--verbose', '-v', type=int, default=2, help='Logging verbosity level')
    parser.add_argument('--file-log-level', type=int, default=False, choices=range(0, 4),
                        help='File logging verbosity level')
    parser.add_argument('--template', '-T', type=str, default='{urlname}', help='Customize filename template')

    args = parser.parse_args()

    if (args.login_user and args.login_pass is None) or (args.login_user is None and args.login_pass):
        parser.print_help()
        raise ValueError('Must provide login user AND password')

    if not args.username and args.filename is None:
        parser.print_help()
        raise ValueError('Must provide username(s) OR a file containing a list of username(s)')
    elif args.username and args.filename:
        parser.print_help()
        raise ValueError('Must provide only one of the following: username(s) OR a filename containing username(s)')

    if args.tag and args.location:
        parser.print_help()
        raise ValueError('Must provide only one of the following: hashtag OR location')

    if args.tag and args.filter:
        parser.print_help()
        raise ValueError('Filters apply to user posts')

    if args.filename:
        args.usernames = parse_usernames_file(args.filename)
    else:
        args.usernames = parse_delimited_str(','.join(args.username))

    if args.media_types and len(args.media_types) == 1 and re.compile(r'[,;\s]+').findall(args.media_types[0]):
        args.media_types = parse_delimited_str(args.media_types[0])

    if args.retry_forever:
        global MAX_RETRIES
        MAX_RETRIES = sys.maxsize

    scraper = InstagramScraper(**vars(args))

    scraper.get_csrf_token()

    if args.tag:
        scraper.scrape_hashtag()
    elif args.location:
        scraper.scrape_location()
    elif args.search_location:
        scraper.search_locations(' '.join(args.usernames))
    else:
        scraper.scrape()


if __name__ == '__main__':
    main()
