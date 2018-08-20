from behave import given, when, then
from hamcrest import equal_to, assert_that

from instagram_scraper.helpers import get_hashtags


@given('an item with no caption text')
def step_impl(context):
    context.item = {}


@when('we get the hashtags')
def step_impl(context):
    context.result = get_hashtags(context.item)


@then('returns an empty list for the hashtags')
def step_impl(context):
    assert_that(context.result, equal_to([]))


@given('caption without hashtags')
def step_impl(context):
    context.item = {
        'caption':  'caption without hashtags'
    }


@given('caption with hashtags')
def step_impl(context):
    context.item = {
        'caption': '#foo text #bar #baz text'
    }


@then('returns a list of hashtags')
def step_impl(context):
    assert_that(sorted(context.result), equal_to(sorted(['foo', 'bar', 'baz'])))


@given('caption with hashtag emojis')
def step_impl(context):
    context.item = {
        'caption': u'#\xA9'
    }


@then('returns a list of hashtags emojis')
def step_impl(context):
    assert_that(sorted(context.result), equal_to([u'\xA9']))