from behave import given, when, then
from hamcrest import assert_that, equal_to

from instagram_scraper.helpers import get_file_extension

@given('a file with an extension')
def step_impl(context):
    context.file = 'file.txt'


@when('we get the file extension')
def step_impl(context):
    context.file_ext = get_file_extension(context.file)


@then('returns the file extension')
def step_impl(context):
    assert_that(context.file_ext, equal_to('txt'))


@given('a file without an extension')
def step_impl(context):
    context.file = 'file'


@then('returns empty string')
def step_impl(context):
    assert_that(context.file_ext, equal_to(''))


@given('a path with a file with an extension')
def step_impl(context):
    context.file = '/path/to/file.txt'


@given('a path with a file without an extension')
def step_impl(context):
    context.file = '/path/to/file'

