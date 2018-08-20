from behave import given, when, then
from hamcrest import equal_to, assert_that

from instagram_scraper.helpers import has_selected_story_media_types


@given('an item with media type image and selected media types includes images')
def step_impl(context):
    context.item = {'media_type': 1}
    context.selected = ['story-image']


@when('we call has selected story media types')
def step_impl(context):
    context.result = has_selected_story_media_types(context.item, context.selected)


@then('returns true for has selected story media types')
def step_impl(context):
    assert_that(context.result, equal_to(True))


@given('an item with media type video and selected media types includes videos')
def step_impl(context):
    context.item = {'media_type': 2}
    context.selected = ['story-video']


@given('an item with story type image and selected media types includes images')
def step_impl(context):
    context.item = {'__typename': 'GraphStoryImage'}
    context.selected = ['story-image']


@given('an item with story type video and selected media types includes videos')
def step_impl(context):
    context.item = {'__typename': 'GraphStoryVideo'}
    context.selected = ['story-video']


@given('an item without media type')
def step_impl(context):
    context.item = {}
    context.selected = ['story-image']


@then('returns false for has selected story media types')
def step_impl(context):
    assert_that(context.result, equal_to(False))