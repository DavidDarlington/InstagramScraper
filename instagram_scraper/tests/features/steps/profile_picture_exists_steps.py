from behave import given, when, then
from hamcrest import equal_to, assert_that
from mock import patch

from instagram_scraper.helpers import profile_picture_exists


@when('we call profile picture exists')
def step_impl(context):
    context.exists = profile_picture_exists(context.dir, context.url)


@then('returns False for profile picture exists')
def step_impl(context):
    assert_that(context.exists, equal_to(False))


@given('a dir and a profile picture url')
def step_impl(context):
    context.dir = '/path/to/dir'
    context.url = 'http://example.com/image.jpg'


@when('the file exists and we call profile picture exists')
def step_impl(context):
    with patch('os.path.isfile') as isfile_mock:
        isfile_mock.return_value = True

        context.exists = profile_picture_exists(context.dir, context.url)


@then('returns True for profile picture exists')
def step_impl(context):
    assert_that(context.exists, equal_to(True))


@when('the file doesn\'t exist and we call profile picture exists')
def step_impl(context):
    with patch('os.path.isfile') as isfile_mock:
        isfile_mock.return_value = False

        context.exists = profile_picture_exists(context.dir, context.url)
