from behave import given, when, then
from hamcrest import assert_that, equal_to

from instagram_scraper.helpers import get_timestamp


@given('an item with no timestamp fields')
def step_impl(context):
    context.item = {}


@when('we get the timestamp from the media item')
def step_impl(context):
    context.ts = get_timestamp(context.item)


@then('returns 0 for the timestamp')
def step_impl(context):
    assert_that(context.ts, equal_to(0))


@given('an item with a not a number timestamp field value')
def step_impl(context):
    context.item = {
        'created_time': False,
        'date': 'a string timestamp'
    }


@given('an item with timestamp fields')
def step_impl(context):
    context.item_timestamp = 1517169889
    context.item = {
        'taken_at_timestamp': 0,
        'created_time': None,
        'taken_at': context.item_timestamp
    }


@then('returns the timestamp')
def step_impl(context):
    assert_that(context.ts, equal_to(context.item_timestamp))
