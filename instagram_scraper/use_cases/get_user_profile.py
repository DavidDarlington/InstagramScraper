from instagram_scraper.helpers import deep_get


def get_user_profile(username, observer, user_repo):

    def success(user):
        media = deep_get(user, 'edge_owner_to_timeline_media')

        if deep_get(user, 'is_private') and deep_get(media, 'count') > 0 and not deep_get(media, 'edges'):
            observer.get_user_profile_is_private(user)
            return

        observer.get_user_profile_success(user)

    def failure(exception):
        observer.get_user_profile_error(exception)

    user_repo.get_profile(username=username,
                          success=success,
                          failure=failure)