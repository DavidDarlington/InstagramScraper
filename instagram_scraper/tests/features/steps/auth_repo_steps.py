from behave import given, when, then
from hamcrest import equal_to, assert_that, instance_of
from mock import MagicMock
from requests import Session, HTTPError, Response

from instagram_scraper.constants import BASE_URL, STORIES_UA
from instagram_scraper.exceptions import MissingSharedData, InvalidCredentialsException
from instagram_scraper.repos import AuthRepo


@given('an auth repo')
def auth_repo(context):
    context.session = MagicMock(spec=Session, headers={})
    context.session.headers = MagicMock()
    context.auth_repo = AuthRepo(context.session)


@given('a session')
def step_impl(context):
    pass


@when('find csrf token fails')
def step_impl(context):
    context.failure = MagicMock()

    context.error = HTTPError('error')
    context.session.get = MagicMock(side_effect=context.error)

    context.auth_repo.find_csrf_token(success=None,
                                      failure=context.failure)


@when('find csrf token fails with no shared data')
def step_impl(context):
    context.failure = MagicMock()

    context.error = MissingSharedData('missing _sharedData')
    context.session.get.return_value = MagicMock(
        cookies={'csrftoken': 'token'},
        text=''
    )

    context.auth_repo.find_csrf_token(success=None,
                                      failure=context.failure)


@when('find csrf token fails with no rhx gis value')
def step_impl(context):
    context.failure = MagicMock()

    response_text = 'window._sharedData = {};</script>'

    context.session.get.return_value = MagicMock(
        cookies={'csrftoken': 'token'},
        text=response_text
    )

    context.auth_repo.find_csrf_token(success=None,
                                      failure=context.failure)


@then('calls the failure callback with the missing shared data exception')
def step_impl(context):
    assert_that(context.failure.call_args[0][0], instance_of(MissingSharedData))


@then('calls the failure callback with an exception')
def step_impl(context):
    assert_that(context.failure.call_args[0][0], instance_of(KeyError))


@then('updates the referer and user-agent headers')
def step_impl(context):
    assert_that(context.session.headers.update.call_args_list[0][0][0],
                equal_to({'Referer': BASE_URL, 'user-agent': STORIES_UA}))


@then('calls the failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)


@when('find csrf token is successful')
def step_impl(context):
    context.success = MagicMock()

    response_text = 'window._sharedData = {"rhx_gis": "rhx_gis_value"};</script>'

    context.session.get.return_value = MagicMock(
        cookies={'csrftoken': 'token'},
        text=response_text
    )

    context.auth_repo.find_csrf_token(success=context.success,
                                      failure=None)


@then('calls the find the csrf token success callback')
def step_impl(context):
    context.success.assert_called()


@given('a username and password')
def step_impl(context):
    context.username = 'username'
    context.password = 'password'


@when('login fails')
def step_impl(context):
    context.failure = MagicMock()

    context.http_error = HTTPError('error')
    context.response = MagicMock(spec=Response)
    context.response.raise_for_status = MagicMock(side_effect=context.http_error)

    def fake_post(url, data, allow_redirects):
        return context.response

    context.session.post = MagicMock(side_effect=fake_post)

    context.auth_repo.login(username=context.username,
                            password=context.password,
                            success=None,
                            failure=context.failure)


@then('calls the failure callback with the exception and response')
def step_impl(context):
    context.failure.assert_called_with(context.http_error, context.response)


@when('login fails due to authentication failure')
def step_impl(context):
    context.failure = MagicMock()

    context.response = MagicMock(cookies={'csrftoken': 'token'})
    context.response.json.return_value = {'authenticated': False}

    def fake_post(url, data, allow_redirects):
        return context.response

    context.session.post = MagicMock(side_effect=fake_post)

    context.auth_repo.login(username=context.username,
                            password=context.password,
                            success=None,
                            failure=context.failure)


@then('calls the failure callback with an invalid credentials exception and response')
def step_impl(context):
    failure_spy_args = context.failure.call_args[0]
    assert_that(failure_spy_args[0], instance_of(InvalidCredentialsException))
    assert_that(failure_spy_args[1], equal_to(context.response))


@when('login succeeds')
def step_impl(context):
    context.success = MagicMock()

    context.response = MagicMock(cookies={'csrftoken': 'token'})
    context.response.json.return_value = {'authenticated': True}

    def fake_post(url, data, allow_redirects):
        return context.response

    context.session.post = MagicMock(side_effect=fake_post)

    context.auth_repo.login(username=context.username,
                            password=context.password,
                            success=context.success,
                            failure=None)


@then('calls the login success callback')
def step_impl(context):
    context.success.assert_called()


@given('a session and a csrf token')
def step_impl(context):
    pass


@when('logout is successful')
def step_impl(context):
    context.success = MagicMock()

    context.auth_repo.logout(csrf_token='csrf token',
                             success=context.success,
                             failure=None)


@then('calls the success callback')
def step_impl(context):
    context.success.assert_called()


@when('logout fails')
def step_impl(context):
    context.failure = MagicMock()
    context.error = HTTPError('error')

    def fake_post(url, data):
        raise context.error

    context.session.post = MagicMock(side_effect=fake_post)

    context.auth_repo.logout(csrf_token='csrf token',
                             success=None,
                             failure=context.failure)


@then('updates the X-CSRFToken header')
def step_impl(context):
    context.session.headers.update.assert_called_with({'X-CSRFToken': 'token'})