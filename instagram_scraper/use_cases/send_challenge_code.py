def send_challenge_code(challenge_url, code, observer, challenge_repo):

    def success():
        observer.send_challenge_code_success()

    def failure(exception, response):
        content = response.json()
        observer.send_challenge_code_error(exception, content)

    challenge_repo.challenge_code(challenge_url=challenge_url,
                                  code=code,
                                  success=success,
                                  failure=failure)


