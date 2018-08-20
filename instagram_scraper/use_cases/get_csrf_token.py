def get_csrf_token(observer, auth_repo):
    def success():
        observer.get_csrf_token_success()

    def failure(exception):
        observer.get_csrf_token_error(exception)

    auth_repo.find_csrf_token(success=success,
                              failure=failure)