from behave import given, when, then
from hamcrest import assert_that, equal_to

from instagram_scraper.helpers import parse_delimited_str

@given('we have a string "{string}"')
def step_impl(context, string):
    context.string = string


@when('we parse the string')
def step_impl(context):
    context.result = parse_delimited_str(context.string)


@then('returns a list of tokens {tokens}')
def step_impl(context, tokens):
    assert_that(context.result, equal_to(tokens.split(',')))


@given('we have an empty string')
def step_impl(context):
    context.string = ''


@then('returns an empty list')
def step_impl(context):
    assert_that(context.result, equal_to([]))
