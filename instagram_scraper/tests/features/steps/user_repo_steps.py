from behave import given, when, then
from mock import MagicMock
from requests import Session, HTTPError

from instagram_scraper.repos import UserRepo


@given('a user repo')
def user_repo(context):
    context.session = MagicMock(spec=Session)
    context.user_repo = UserRepo(context.session)


@given('a username and session')
def step_impl(context):
    context.username = 'username'


@when('get profile fails')
def step_impl(context):
    context.error = HTTPError('error')
    context.session.get.side_effect = context.error
    context.failure = MagicMock()

    context.user_repo.get_profile(username=context.username,
                                  success=None,
                                  failure=context.failure)


@then('calls the get profile failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)


@when('get profile fails due to missing content')
def step_impl(context):
    context.session.get.return_value = MagicMock(text={})
    context.failure = MagicMock()

    context.user_repo.get_profile(username=context.username,
                                  success=None,
                                  failure=context.failure)


@then('calls the get profile failure callback with a profile exception')
def step_impl(context):
    error = context.failure.call_args[0][0]
    context.failure.assert_called_with(error)


@when('get profile fails due to parse content error')
def step_impl(context):
    response_text = 'window._sharedData = {"entry_data": {"ProfilePage": [{"wrong_key": {}}]}};</script>'
    context.session.get.return_value = MagicMock(text=response_text)
    context.failure = MagicMock()

    context.user_repo.get_profile(username=context.username,
                                  success=None,
                                  failure=context.failure)


@when('get profile succeeds')
def step_impl(context):
    response_text = 'window._sharedData = {"entry_data": {"ProfilePage": [{"graphql": {"user": {"id": 1}}}]}};</script>'
    context.session.get.return_value = MagicMock(text=response_text)
    context.success = MagicMock()

    context.user_repo.get_profile(username=context.username,
                                  success=context.success,
                                  failure=None)


@then('calls the get profile success callback with the user')
def step_impl(context):
    context.success.assert_called_with({'id': 1})


@given('a user id')
def step_impl(context):
    context.user_id = 'user id'


@when('get user info fails')
def step_impl(context):
    context.error = HTTPError()
    context.session.get.side_effect = context.error
    context.failure = MagicMock()

    context.user_repo.get_user_info(user_id=context.user_id,
                                    success=None,
                                    failure=context.failure)


@then('calls the get user info failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)


@when('get user info succeeds')
def step_impl(context):
    context.response = {'user': {}}
    context.session.get.return_value = MagicMock(json=MagicMock(return_value=context.response))
    context.success = MagicMock()

    context.user_repo.get_user_info(user_id=context.user_id,
                                    success=context.success,
                                    failure=None)


@then('calls the get user info success callback with the user')
def step_impl(context):
    context.success.assert_called_with(context.response['user'])