def select_challenge_mode(challenge_url, mode, observer, challenge_repo):
    def success():
        observer.select_challenge_mode_success(challenge_url)

    def failure(exception):
        observer.select_challenge_mode_error(exception)

    challenge_repo.challenge_mode(challenge_url=challenge_url,
                                  mode=mode,
                                  success=success,
                                  failure=failure)


