import logging

from instagram_scraper.constants import SEARCH_URL

log = logging.getLogger(__name__)


class LocationRepo(object):

    def __init__(self, session):
        self.session = session

    def search(self, query, success, failure):
        try:
            response = self.session.get(SEARCH_URL.format(query))
            response.raise_for_status()
        except Exception as e:
            log.exception('search locations failed')
            failure(e)
        else:
            places = response.json().get('places')
            success(places)