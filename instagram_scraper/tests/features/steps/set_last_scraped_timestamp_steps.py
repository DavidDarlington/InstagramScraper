from behave import given, when, then
from hamcrest import assert_that, equal_to
from mock import MagicMock, patch
import configparser

from instagram_scraper.helpers import set_last_scraped_timestamp
from instagram_scraper.constants import LATEST_STAMPS_USER_SECTION


@given('no parser for last scraped timestamps')
def step_impl(context):
    context.parser = None
    context.latest_stamps_file = None
    context.username = None
    context.ts = None


@when('we set the timestamp to the file')
def step_impl(context):
    with patch('%s.open' % __name__):
        set_last_scraped_timestamp(parser=context.parser,
                                   latest_stamps_file=context.latest_stamps_file,
                                   username=context.username,
                                   timestamp=context.ts)


@then('does not write to the timestamps file')
def step_impl(context):
    pass


@given('a parser and a file without a users section')
def step_impl(context):
    context.parser = MagicMock()
    context.parser.has_section.return_value = False
    context.latest_stamps_file = '/path/to/file'
    context.username = 'username'
    context.ts = 100000


@then('adds the users section')
def step_impl(context):
    context.parser.add_section.assert_called_with(LATEST_STAMPS_USER_SECTION)


@then('sets the timestamp for the user')
def step_impl(context):
    context.parser.set.assert_called_with(LATEST_STAMPS_USER_SECTION, context.username, str(context.ts))


@then('writes the timestamp to the timestamps file')
def step_impl(context):
    context.parser.write.assert_called()


@then('does not add the users section')
def step_impl(context):
    context.parser.add_section.assert_not_called()


@given('a parser and a file with a users section')
def step_impl(context):
    context.parser = MagicMock()
    context.parser.has_section.return_value = True
    context.latest_stamps_file = '/path/to/file'
    context.username = 'username'
    context.ts = 100000