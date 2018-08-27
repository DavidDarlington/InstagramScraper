import logging
import json

from instagram_scraper.constants import BASE_URL, LOGIN_URL, LOGOUT_URL, STORIES_UA, CHROME_WIN_UA
from instagram_scraper.exceptions import InvalidCredentialsException, MissingSharedData


log = logging.getLogger(__name__)


class AuthRepo(object):

    def __init__(self, session):
        self.session = session

    def find_csrf_token(self, success, failure):
        try:
            self.session.headers.update({'Referer': BASE_URL, 'user-agent': STORIES_UA})
            response = self.session.get(BASE_URL)
            response.raise_for_status()
        except Exception as e:
            log.exception('find csrf token failed')
            failure(e)
        else:
            content = response.text

            if not content or '_sharedData' not in content:
                failure(MissingSharedData('missing _sharedData'))
                return

            try:
                shared_data = content.split('window._sharedData = ')[1].split(';</script>')[0]
                self.session.rhx_gis = json.loads(shared_data)['rhx_gis']
            except (TypeError, KeyError, IndexError) as e:
                log.exception('failed to get rhx_gis value')
                failure(e)
                return

            csrf_token = response.cookies['csrftoken']
            self.session.headers.update({'X-CSRFToken': csrf_token})

            success()

    def login(self, username, password, success, failure):
        data = {'username': username, 'password': password}

        try:
            response = self.session.post(LOGIN_URL, data=data, allow_redirects=True)
            response.raise_for_status()
        except Exception as e:
            log.exception('login failed')
            failure(e, response)
        else:
            content = response.json()
            csrf_token = response.cookies['csrftoken']

            if not content.get('authenticated', False):
                exception = InvalidCredentialsException('authentication failed for credentials: ' + username)
                failure(exception, response)
                return

            self.session.headers.update({'X-CSRFToken': csrf_token})
            self.session.headers.update({'user-agent': CHROME_WIN_UA})
            success()

    def logout(self, csrf_token, success, failure):
        data = {'csrfmiddlewaretoken': csrf_token}

        try:
            response = self.session.post(LOGOUT_URL, data=data)
            response.raise_for_status()
        except Exception as e:
            log.warning('logout failed')
            failure(e)
        else:
            success()

