from instagram_scraper.helpers import deep_get, first


def get_profile_picture(user, observer, user_repo):

    def success(user_info):
        if user_info.get('has_anonymous_profile_picture'):
            observer.get_profile_picture_is_default(user)
            return

        profile_pic_urls = [
            deep_get(user_info, 'hd_profile_pic_url_info.url'),
            deep_get(user_info, 'hd_profile_pic_versions[-1].url'),
            user.get('profile_pic_url_hd'),
            user_info.get('profile_pic_url')
        ]

        profile_pic_url = first(profile_pic_urls)

        observer.get_profile_picture_success(profile_pic_url)

    def failure(exception):
        observer.get_profile_picture_error(exception)

    user_repo.get_user_info(user_id=user['id'],
                            success=success,
                            failure=failure)
