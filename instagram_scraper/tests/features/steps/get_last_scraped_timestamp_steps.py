from behave import given, when, then
from hamcrest import assert_that, equal_to
from mock import MagicMock
import configparser

from instagram_scraper.helpers import get_last_scraped_timestamp


@given('a username with no parser')
def step_impl(context):
    context.parser = None
    context.username = 'username'


@when('we get the timestamp from the file')
def step_impl(context):
    context.timestamp = get_last_scraped_timestamp(parser=context.parser,
                                                   username=context.username)


@then('returns 0 as the timestamp')
def step_impl(context):
    assert_that(context.timestamp, equal_to(0))


@given('a parser and a username')
def step_impl(context):
    context.parser = MagicMock()
    context.parser.getint.return_value = 1000000
    context.username = 'username'


@then('returns the last scraped timestamp')
def step_impl(context):
    assert_that(context.timestamp, equal_to(1000000))


@given('a parser that fails with error and a username')
def step_impl(context):
    context.parser = MagicMock()
    context.parser.getint.side_effect = configparser.Error
    context.username = 'username'