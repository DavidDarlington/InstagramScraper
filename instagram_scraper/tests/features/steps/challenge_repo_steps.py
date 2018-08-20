from behave import given, when, then
from hamcrest import assert_that, instance_of
from mock import MagicMock, call, ANY
from requests import RequestException, Response

from instagram_scraper.exceptions import ChallengeException
from instagram_scraper.repos import ChallengeRepo


@given('a session and challenge repo')
def challenge_repo(context):
    context.session = MagicMock()
    context.session.headers.return_value = {
        'update': MagicMock()
    }
    context.challenge_repo = ChallengeRepo(context.session)


@given('a challenge url and selected mode')
def step_impl(context):
    context.challenge_url = 'challenge url'
    context.mode = 1


@when('the challenge mode choice is successfully sent')
def step_impl(context):
    context.session.post.return_value = MagicMock(cookies={'csrftoken': 'token'})
    context.success = MagicMock()

    context.challenge_repo.challenge_mode(challenge_url=context.challenge_url,
                                          mode=context.mode,
                                          success=context.success,
                                          failure=None)


@then('updates the Referer, X-CSRFToken, and X-Instagram-AJAX headers')
def step_impl(context):
    context.session.headers.update.assert_has_calls([
        call({'Referer': context.challenge_url}),
        call({
            'X-CSRFToken': 'token',
            'X-Instagram-AJAX': '1'
        })
    ])


@then('calls the challenge mode success callback')
def step_impl(context):
    context.success.assert_called()


@when('the challenge mode choice request fails')
def step_impl(context):
    context.exception = RequestException('error')
    context.session.post = MagicMock(side_effect=context.exception)
    context.failure = MagicMock()

    context.challenge_repo.challenge_mode(challenge_url=context.challenge_url,
                                          mode=context.mode,
                                          success=None,
                                          failure=context.failure)


@then('calls the challenge mode failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.exception)


@when('the challenge mode choice request fails due to unsupported mode')
def step_impl(context):
    context.session.post.return_value = MagicMock(text='Select a valid choice')
    context.failure = MagicMock()

    context.challenge_repo.challenge_mode(challenge_url=context.challenge_url,
                                          mode=context.mode,
                                          success=None,
                                          failure=context.failure)


@then('calls the challenge mode failure callback with a challenge exception')
def step_impl(context):
    actual_exception = context.failure.call_args[0][0]
    assert_that(actual_exception, instance_of(ChallengeException))
    context.failure.assert_called()


@given('a challenge url and code')
def step_impl(context):
    context.challenge_url = 'challenge url'
    context.code = 987123


@when('the challenge code is successful')
def step_impl(context):
    context.response = MagicMock(spec=Response,
                                 json=MagicMock(return_value={'status': 'ok'}),
                                 cookies={'csrftoken': 'token'})
    context.session.post.return_value = context.response
    context.success = MagicMock()

    context.challenge_repo.challenge_code(challenge_url=context.challenge_url,
                                          code=context.code,
                                          success=context.success,
                                          failure=None)


@then('calls the challenge code success callback')
def step_impl(context):
    context.success.assert_called()


@when('the challenge code fails')
def step_impl(context):
    context.response = MagicMock(spec=Response)
    context.session.post.return_value = context.response

    context.exception = RequestException('error')
    context.response.raise_for_status = MagicMock(side_effect=context.exception)

    context.failure = MagicMock()

    context.challenge_repo.challenge_code(challenge_url=context.challenge_url,
                                          code=context.code,
                                          success=None,
                                          failure=context.failure)


@when('the challenge code fails due to invalid code')
def step_impl(context):
    context.response = MagicMock(spec=Response,
                                 json=MagicMock(return_value={'status': 'fail'}),
                                 cookies={'csrftoken': 'token'})
    context.session.post.return_value = context.response

    context.failure = MagicMock()

    context.challenge_repo.challenge_code(challenge_url=context.challenge_url,
                                          code=context.code,
                                          success=None,
                                          failure=context.failure)


@then('calls the challenge code failure callback with the exception and response')
def step_impl(context):
    context.failure.assert_called_with(context.exception, context.response)


@then('calls the challenge code failure callback with a challenge exception and response')
def step_impl(context):
    actual_exception = context.failure.call_args[0][0]
    assert_that(actual_exception, instance_of(ChallengeException))

    context.failure.assert_called_with(ANY, context.response)
