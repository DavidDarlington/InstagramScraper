import logging
import json

from instagram_scraper.constants import BASE_URL, USER_INFO
from instagram_scraper.exceptions import ProfileException

log = logging.getLogger(__name__)


class UserRepo(object):

    def __init__(self, session):
        self.session = session

    def get_profile(self, username, success, failure):
        try:
            response = self.session.get(BASE_URL + username)
            response.raise_for_status()
        except Exception as e:
            log.exception('get profile for ' + username + ' failed')
            failure(e)
        else:
            content = response.text

            if content and '_sharedData' in content:
                try:
                    shared_data = content.split('window._sharedData = ')[1].split(';</script>')[0]
                    user = json.loads(shared_data)['entry_data']['ProfilePage'][0]['graphql']['user']

                    success(user)
                    return
                except (TypeError, KeyError, IndexError):
                    log.exception('failed to parse profile content')

            error = ProfileException('failed to get profile data for ' + username)
            failure(error)

    def get_user_info(self, user_id, success, failure):
        try:
            response = self.session.get(USER_INFO.format(user_id))
            response.raise_for_status()
        except Exception as e:
            log.exception('get profile picture failed for ' + user_id + ' failed')
            failure(e)
        else:
            content = response.json()
            success(content['user'])