from behave import given, when, then
from hamcrest import equal_to, assert_that
from instagram_scraper.helpers import first

@given('an empty list')
def step_impl(context):
    context.list = []


@when('first is called')
def step_impl(context):
    context.result = first(context.list)


@then('returns None')
def step_impl(context):
    assert_that(context.result, equal_to(None))


@given('a list with a value')
def step_impl(context):
    context.list = [None, 'test']


@then('returns the value')
def step_impl(context):
    assert_that(context.result, equal_to('test'))


@given('a list of None values')
def step_impl(context):
    context.list = [None, None, None]


@given('a list of None values and a default value')
def step_impl(context):
    context.list = [None, None, None]
    context.default = 'default'


@when('first is called with a default')
def step_impl(context):
    context.result = first(context.list, default=context.default)


@then('returns the default value')
def step_impl(context):
    assert_that(context.result, equal_to('default'))


@given('a list with a value and a default')
def step_impl(context):
    context.list = [None, None, 'test']
    context.default = 'default'
