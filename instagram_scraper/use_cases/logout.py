def logout(csrf_token, observer, auth_repo):
    def success():
        observer.logout_success()

    def failure(exception):
        observer.logout_error(exception)

    auth_repo.logout(csrf_token=csrf_token,
                     success=success,
                     failure=failure)
