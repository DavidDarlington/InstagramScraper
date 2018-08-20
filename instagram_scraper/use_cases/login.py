from instagram_scraper.constants import *


def login(username, password, observer, auth_repo):

    def success():
        observer.login_success()

    def failure(exception, response):
        content = response.json()
        challenge_path = content.get('checkpoint_url', False)

        if response.status_code == 400 and challenge_path:
            observer.challenge_prompt(BASE_URL[:-1] + challenge_path)
        else:
            observer.login_error(exception, content)

    auth_repo.login(username=username,
                    password=password,
                    success=success,
                    failure=failure)


