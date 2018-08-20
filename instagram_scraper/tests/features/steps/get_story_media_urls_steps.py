from behave import given, when, then
from hamcrest import equal_to, assert_that

from instagram_scraper.helpers import get_story_media_urls


@given('item with video and image urls')
def step_impl(context):
    context.item = {
        'video_resources': [
            {'src': 'lower quality url1'},
            {'src': 'url1'}
        ],
        'display_resources': [
            {'src': 'lower quality url2'},
            {'src': 'url2?'}
        ]
    }


@when('we get the story urls')
def step_impl(context):
    context.result = get_story_media_urls(context.item)


@then('returns a list of story image and video urls')
def step_impl(context):
    assert_that(context.result, equal_to(['url1', 'url2']))


@given('item with no video and image urls')
def step_impl(context):
    context.item = {}


@then('returns an empty list with no urls')
def step_impl(context):
    assert_that(context.result, equal_to([]))
