import logging

from instagram_scraper.constants import QUERY_MEDIA, QUERY_MEDIA_VARS, VIEW_MEDIA_URL
from instagram_scraper.helpers import deep_get

log = logging.getLogger(__name__)


class MediaRepo(object):

    def __init__(self, session):
        self.session = session

    def query_media(self, user_id, end_cursor):
        params = QUERY_MEDIA_VARS.format(id, end_cursor)

        try:
            response = self.session.get(QUERY_MEDIA.format(params))
            response.raise_for_status()
            return deep_get(response.json(), 'data.user')
        except Exception as e:
            log.exception('query media for user_id=' + user_id + ' failed')
            raise e

    def get_media_details(self, short_code):
        try:
            response = self.session.get(VIEW_MEDIA_URL.format(short_code))
            response.raise_for_status()
            return deep_get(response.json(), 'graphql.shortcode_media')
        except Exception as e:
            log.exception('get media details for shortcode=' + short_code + ' failed')
            raise e

