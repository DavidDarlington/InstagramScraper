from behave import given, when, then
from mock import MagicMock
from requests import RequestException, Response

from instagram_scraper.use_cases import send_challenge_code


@given('a challenge url, code, observer, and challenge repo')
def step_impl(context):
    context.challenge_url = 'challenge url'
    context.code = '987123'
    context.observer = MagicMock()
    context.challenge_repo = MagicMock()


@when('a challenge code is successfully sent')
def step_impl(context):
    def challenge_code_fake(**kwargs):
        kwargs['success']()

    context.challenge_repo.challenge_code.side_effect = challenge_code_fake

    send_challenge_code(challenge_url=context.challenge_url,
                        code=context.code,
                        observer=context.observer,
                        challenge_repo=context.challenge_repo)


@then('calls the send challenge code success callback')
def step_impl(context):
    context.observer.send_challenge_code_success.assert_called()


@when('sending the challenge code fails')
def step_impl(context):
    def challenge_code_fake(**kwargs):
        context.exception = MagicMock(spec=RequestException)
        context.response = MagicMock(spec=Response)
        kwargs['failure'](context.exception, context.response)

    context.challenge_repo.challenge_code.side_effect = challenge_code_fake

    send_challenge_code(challenge_url=context.challenge_url,
                        code=context.code,
                        observer=context.observer,
                        challenge_repo=context.challenge_repo)


@then('the send challenge code error callback is called with the exception and response')
def step_impl(context):
    context.observer.send_challenge_code_error.assert_called_with(
        context.exception,
        context.response.json.return_value
    )