from behave import given, when, then
from mock import MagicMock
from requests import HTTPError

from instagram_scraper.use_cases import get_profile_picture


@given('a user and an observer')
def step_impl(context):
    context.user = {'id': 1}
    context.observer = MagicMock()


@when('get profile picture succeeds with the highest quality picture')
def step_impl(context):
    def get_user_info_fake(**kwargs):
        context.profile_pic_url = 'highest quality url'
        context.user_info = {
            'hd_profile_pic_url_info': {
                'url':  context.profile_pic_url
            }
        }
        kwargs['success'](context.user_info)

    context.user_repo.get_user_info.side_effect = get_user_info_fake

    get_profile_picture(user=context.user,
                        observer=context.observer,
                        user_repo=context.user_repo)


@when('get profile picture succeeds with the lowest quality picture')
def step_impl(context):
    def get_user_info_fake(**kwargs):
        context.profile_pic_url = 'lowest quality url'
        context.user_info = {
            'profile_pic_url': context.profile_pic_url
        }
        kwargs['success'](context.user_info)

    context.user_repo.get_user_info.side_effect = get_user_info_fake

    get_profile_picture(user=context.user,
                        observer=context.observer,
                        user_repo=context.user_repo)


@when('get profile picture succeeds with no profile pictures')
def step_impl(context):
    context.user['profile_pic_url_hd'] = 'url from user'
    context.profile_pic_url_from_user = context.user['profile_pic_url_hd']

    def get_user_info_fake(**kwargs):
        context.user_info = {}
        kwargs['success'](context.user_info)

    context.user_repo.get_user_info.side_effect = get_user_info_fake

    get_profile_picture(user=context.user,
                        observer=context.observer,
                        user_repo=context.user_repo)


@then('tells the observer get profile picture was successful with the profile picture url')
def step_impl(context):
    context.observer.get_profile_picture_success.assert_called_with(context.profile_pic_url)


@then('tells the observer get profile picture was successful with the profile picture url from the user')
def step_impl(context):
    context.observer.get_profile_picture_success.assert_called_with(context.profile_pic_url_from_user)


@when('get profile picture fails')
def step_impl(context):
    def get_user_info_fake(**kwargs):
        context.error = HTTPError('error')
        kwargs['failure'](context.error)

    context.user_repo.get_user_info.side_effect = get_user_info_fake

    get_profile_picture(user=context.user,
                        observer=context.observer,
                        user_repo=context.user_repo)


@then('tells the observer get profile picture failed with the exception')
def step_impl(context):
    context.observer.get_profile_picture_error.assert_called_with(context.error)


@when('get profile picture is anonymous')
def step_impl(context):
    def get_user_info_fake(**kwargs):
        context.user_info = {
            'has_anonymous_profile_picture': True
        }
        kwargs['success'](context.user_info)

    context.user_repo.get_user_info.side_effect = get_user_info_fake

    get_profile_picture(user=context.user,
                        observer=context.observer,
                        user_repo=context.user_repo)


@then('tells the observer get profile picture is default')
def step_impl(context):
    context.observer.get_profile_picture_is_default.assert_called_with(context.user)

