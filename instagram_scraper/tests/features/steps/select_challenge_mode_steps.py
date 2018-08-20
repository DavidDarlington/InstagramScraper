from behave import given, when, then
from mock import MagicMock
from requests import RequestException

from instagram_scraper.use_cases import select_challenge_mode


@given('a challenge url, mode, observer, and challenge repo')
def step_impl(context):
    context.challenge_url = 'challenge url'
    context.mode = 1
    context.observer = MagicMock()
    context.challenge_repo = MagicMock()


@when('a challenge mode is successfully selected')
def step_impl(context):
    def challenge_mode_fake(**kwargs):
        kwargs['success']()

    context.challenge_repo.challenge_mode.side_effect = challenge_mode_fake

    select_challenge_mode(challenge_url=context.challenge_url,
                          mode=context.mode,
                          observer=context.observer,
                          challenge_repo=context.challenge_repo)


@then('calls the select challenge mode success callback with the challenge url')
def step_impl(context):
    context.observer.select_challenge_mode_success.assert_called_with(context.challenge_url)


@when('challenge mode selection fails')
def step_impl(context):
    def challenge_mode_fake(**kwargs):
        context.exception = MagicMock(spec=RequestException)
        kwargs['failure'](context.exception)

    context.challenge_repo.challenge_mode.side_effect = challenge_mode_fake

    select_challenge_mode(challenge_url=context.challenge_url,
                          mode=context.mode,
                          observer=context.observer,
                          challenge_repo=context.challenge_repo)


@then('calls the select challenge mode failure callback with the exception')
def step_impl(context):
    context.observer.select_challenge_mode_error(context.exception)
