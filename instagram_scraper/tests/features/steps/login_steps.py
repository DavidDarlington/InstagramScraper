from behave import given, when, then
from mock import MagicMock, patch
from requests import HTTPError, ConnectionError, Response
from hamcrest import assert_that, instance_of

from instagram_scraper.constants import *
from instagram_scraper.exceptions import InvalidCredentialsException
from instagram_scraper.use_cases import login


@given('an observer and auth repo')
def step_impl(context):
    context.observer = MagicMock()
    context.auth_repo = MagicMock()


@when('the login is successful')
def step_impl(context):
    def login_fake(**kwargs):
        kwargs['success']()

    context.auth_repo.login.side_effect = login_fake

    login(username=context.username,
          password=context.password,
          observer=context.observer,
          auth_repo=context.auth_repo)


@then('tells the observer the login was successful')
def step_impl(context):
    context.observer.login_success.assert_called()


@when('the login request is successful but the user is not authenticated')
def step_impl(context):
    def login_fake(**kwargs):
        response = MagicMock(spec=Response,
                             json=MagicMock(return_value={}),
                             status_code=200)
        context.error = InvalidCredentialsException()

        kwargs['failure'](context.error, response)

    context.auth_repo.login.side_effect = login_fake

    login(username=context.username,
          password=context.password,
          observer=context.observer,
          auth_repo=context.auth_repo)


@then('tells the observer the login failed with the exception and response content')
def step_impl(context):
    exception = context.observer.login_error.call_args[0][0]
    assert_that(exception, instance_of(InvalidCredentialsException))
    context.observer.login_error.assert_called_with(context.error, {})


@when('the login request fails due to a required challenge')
def step_impl(context):
    def login_fake(**kwargs):
        response = MagicMock(status_code=400)
        context.checkpoint_url = '/challenge'
        response.json = MagicMock(return_value={'checkpoint_url': context.checkpoint_url})

        kwargs['failure'](MagicMock(spec=HTTPError), response)

    context.auth_repo.login.side_effect = login_fake

    login(username=context.username,
          password=context.password,
          observer=context.observer,
          auth_repo=context.auth_repo)


@then('tells the observer a challenge is prompted with the challenge url')
def step_impl(context):
    expected_challenge_url = BASE_URL[:-1] + context.checkpoint_url
    context.observer.challenge_prompt.assert_called_with(expected_challenge_url)
