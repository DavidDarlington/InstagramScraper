import logging

from instagram_scraper.constants import STORIES_URL
from instagram_scraper.helpers import deep_get, get_story_media_urls

log = logging.getLogger(__name__)


class StoryRepo(object):

    def __init__(self, session):
        self.session = session

    def find(self, user_id, success, failure):
        try:
            response = self.session.get(STORIES_URL.format(user_id))
            response.raise_for_status()
        except Exception as e:
            log.exception('find stories for ' + user_id + ' failed')
            failure(e)
        else:
            content = response.json()
            items = deep_get(content, 'data.reels_media[0].items')

            if items and len(items) > 0:
                for item in items:
                    item['urls'] = get_story_media_urls(item)

                success(items)
            else:
                success([])