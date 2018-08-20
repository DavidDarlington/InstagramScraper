from behave import given, when, then
from hamcrest import equal_to, assert_that

from instagram_scraper.helpers import get_caption_text


@given('an item without a caption')
def step_impl(context):
    context.item = {}


@when('we get caption text')
def step_impl(context):
    context.result = get_caption_text(context.item)


@then('returns None for the caption text')
def step_impl(context):
    assert_that(context.result, equal_to(None))


@given('an item with a string caption')
def step_impl(context):
    context.item = {'caption': 'string caption'}


@then('returns the caption text')
def step_impl(context):
    assert_that(context.result, equal_to('string caption'))


@given('an item with a dict caption')
def step_impl(context):
    context.item = {'caption': {'text': 'string caption'}}


@given('an item with a nested caption')
def step_impl(context):
    context.item = {
        'edge_media_to_caption': {
            'edges': [
                {'node': {'text': 'string caption'}}
            ]
        }
    }
