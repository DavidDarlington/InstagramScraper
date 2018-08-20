from behave import given, when, then
from hamcrest import assert_that, equal_to

from instagram_scraper.helpers import get_destination_dir


@given('the destination is the current directory and retain username is false')
def step_impl(context):
    context.destination = './'
    context.retain_username = False
    context.username = 'username'


@when('we get the destination directory')
def step_impl(context):
    context.destination_path = get_destination_dir(
        destination=context.destination,
        retain_username=context.retain_username,
        username=context.username
    )


@then('returns ./username')
def step_impl(context):
    assert_that(context.destination_path, equal_to('./username'))


@given('the destination is not the current directory and retain username is false')
def step_impl(context):
    context.destination = '/dev/null'
    context.retain_username = False
    context.username = 'username'


@then('returns the destination directory')
def step_impl(context):
    assert_that(context.destination_path, equal_to('/dev/null'))


@given('the destination is not the current directory and retain username is true')
def step_impl(context):
    context.destination = '/home/user/instagram-scraper'
    context.retain_username = True
    context.username = 'username'


@then('returns the destination directory/username')
def step_impl(context):
    assert_that(context.destination_path, equal_to('/home/user/instagram-scraper/username'))