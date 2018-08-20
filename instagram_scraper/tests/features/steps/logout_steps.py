from behave import given, when, then
from requests import RequestException

from instagram_scraper.use_cases import logout


@given('a csrf token')
def step_impl(context):
    context.csrf_token = 'csrf token'


@when('the logout fails due to an error')
def step_impl(context):
    context.exception = RequestException('error')

    def logout_fake(**kwargs):
        kwargs['failure'](context.exception)

    context.auth_repo.logout.side_effect = logout_fake

    logout(csrf_token=context.csrf_token,
           observer=context.observer,
           auth_repo=context.auth_repo)


@then('tells the observer logout failed with an error')
def step_impl(context):
    context.observer.logout_error.assert_called_with(context.exception)


@when('logout succeeds')
def step_impl(context):
    def logout_fake(**kwargs):
        kwargs['success']()

    context.auth_repo.logout.side_effect = logout_fake

    logout(csrf_token=context.csrf_token,
           observer=context.observer,
           auth_repo=context.auth_repo)


@then('tells the observer logout is successful')
def step_impl(context):
    context.observer.logout_success.assert_called()
