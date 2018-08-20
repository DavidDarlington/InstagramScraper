import logging

from instagram_scraper.exceptions import ChallengeException

log = logging.getLogger(__name__)


class ChallengeRepo(object):

    def __init__(self, session):
        self.session = session

    def challenge_mode(self, challenge_url, mode, success, failure):
        data = {'choice': mode}

        try:
            self.session.headers.update({'Referer': challenge_url})
            response = self.session.post(challenge_url, data=data, allow_redirects=True)
            response.raise_for_status()
        except Exception as e:
            log.exception('send challenge mode failed')
            failure(e)
        else:
            content = response.text

            if 'Select a valid choice' in content:
                failure(ChallengeException('selected challenge mode is not supported'))
                return

            csrf_token = response.cookies['csrftoken']
            self.session.headers.update({
                'X-CSRFToken': csrf_token,
                'X-Instagram-AJAX': '1'
            })

            success()

    def challenge_code(self, challenge_url, code, success, failure):
        data = {'security_code': code}

        try:
            response = self.session.post(challenge_url, data=data, allow_redirects=True)
            response.raise_for_status()
        except Exception as e:
            log.exception('send challenge code failed')
            failure(e, response)
        else:
            content = response.json()

            if content.get('status') != 'ok':
                exception = ChallengeException('challenged code failed')
                failure(exception, response)
                return

            csrf_token = response.cookies['csrftoken']
            self.session.headers.update({'X-CSRFToken': csrf_token})

            success()
