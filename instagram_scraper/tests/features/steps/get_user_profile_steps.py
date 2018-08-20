from behave import given, when, then
from mock import MagicMock
from requests import HTTPError

from instagram_scraper.use_cases import get_user_profile


@given('a session and user repo')
def step_impl(context):
    context.session = MagicMock()
    context.user_repo = MagicMock()


@given('a username and an observer')
def step_impl(context):
    context.username = 'username'
    context.observer = MagicMock()


@when('get user profile returns a private user and you are not an approved follower')
def step_impl(context):
    def get_profile_fake(**kwargs):
        context.user = {
            'username': context.username,
            'is_private': True,
            'edge_owner_to_timeline_media': {
                'count': 100,
                'edges': []
            }
        }
        kwargs['success'](context.user)

    context.user_repo.get_profile.side_effect = get_profile_fake

    get_user_profile(username=context.username,
                     observer=context.observer,
                     user_repo=context.user_repo)


@then('tells the observer get user profile is private with the user')
def step_impl(context):
    context.observer.get_user_profile_is_private.assert_called_with(context.user)


@when('get user profile returns a private user and you are an approved follower')
def step_impl(context):
    def get_profile_fake(**kwargs):
        context.user = {
            'username': context.username,
            'is_private': True,
            'edge_owner_to_timeline_media': {
                'count': 100,
                'edges': [
                    {'node': {'id': 1}}
                ]
            }
        }
        kwargs['success'](context.user)

    context.user_repo.get_profile.side_effect = get_profile_fake

    get_user_profile(username=context.username,
                     observer=context.observer,
                     user_repo=context.user_repo)


@when('get user profile returns a public user')
def step_impl(context):
    def get_profile_fake(**kwargs):
        context.user = {'username': context.username, 'is_private': False}
        kwargs['success'](context.user)

    context.user_repo.get_profile.side_effect = get_profile_fake

    get_user_profile(username=context.username,
                     observer=context.observer,
                     user_repo=context.user_repo)


@then('tells the observer get user profile was successful with the user')
def step_impl(context):
    context.observer.get_user_profile_success.assert_called_with(context.user)


@when('get user profile fails')
def step_impl(context):
    def get_profile_fake(**kwargs):
        context.error = HTTPError('error')
        kwargs['failure'](context.error)

    context.user_repo.get_profile.side_effect = get_profile_fake

    get_user_profile(username=context.username,
                     observer=context.observer,
                     user_repo=context.user_repo)


@then('tells the observer get profile failed with the exception')
def step_impl(context):
    context.observer.get_user_profile_error.assert_called_with(context.error)
