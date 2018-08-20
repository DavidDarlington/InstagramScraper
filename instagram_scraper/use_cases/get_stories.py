def get_stories(user, observer, story_repo):

    def success(stories):
        if not stories:
            observer.get_stories_empty()
            return

        observer.get_stories_success(stories)

    def failure(exception):
        observer.get_stories_error(exception)

    story_repo.find(user_id=user['id'],
                    success=success,
                    failure=failure)
