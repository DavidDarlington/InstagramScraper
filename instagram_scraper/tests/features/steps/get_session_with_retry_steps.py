from behave import given, when, then
from hamcrest import assert_that, instance_of
from requests import Session
from urllib3.util.retry import Retry

from instagram_scraper.helpers import get_session_with_retry


@given('a session does not exist')
def step_impl(context):
    context.session = None


@when('we get the session with retry')
def step_impl(context):
    context.session = get_session_with_retry(session=context.session)


@then('returns a new session with retry capability')
def step_impl(context):
    assert_that(context.session, instance_of(Session))
    assert_that(context.session.adapters['http://'].max_retries, instance_of(Retry))
    assert_that(context.session.adapters['https://'].max_retries, instance_of(Retry))

