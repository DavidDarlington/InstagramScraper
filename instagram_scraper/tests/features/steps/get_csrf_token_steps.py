from behave import given, when, then
from mock import MagicMock, patch

from instagram_scraper.use_cases import get_csrf_token


@given('an observer and auth_repo setup')
def step_impl(context):
    context.auth_repo = MagicMock()
    context.observer = MagicMock()


@when('get csrf token is successful')
def step_impl(context):
    def fake_success(success, failure):
        success()

    context.auth_repo.find_csrf_token.side_effect = fake_success
    get_csrf_token(observer=context.observer, auth_repo=context.auth_repo)


@then('calls the get csrf token success callback')
def step_impl(context):
    context.observer.get_csrf_token_success.assert_called()


@when('get csrf token fails')
def step_impl(context):
    context.exception = Exception('error')

    def fake_failure(success, failure):
        failure(context.exception)

    context.auth_repo.find_csrf_token.side_effect = fake_failure
    get_csrf_token(observer=context.observer, auth_repo=context.auth_repo)


@then('calls the get csrf token failure callback with the exception')
def step_impl(context):
    context.observer.get_csrf_token_error.assert_called_with(context.exception)