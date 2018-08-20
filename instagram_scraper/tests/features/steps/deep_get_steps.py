from behave import given, when, then
from hamcrest import assert_that, equal_to

from instagram_scraper.helpers import deep_get


@given('an empty dict')
def step_impl(context):
    context.dict = {}
    context.path = 'foo.bar.baz'

@given('a None dict')
def step_impl(context):
    context.dict = None
    context.path = 'foo.bar.baz'

@when('we deep get')
def step_impl(context):
    context.result = deep_get(context.dict, context.path)


@then('returns None for the key value')
def step_impl(context):
    assert_that(context.result, equal_to(None))


@given('an dict with nested keys')
def step_impl(context):
    context.dict = {
        'foo': {
            'bar': {
                'baz': 'hello'
            }
        }
    }
    context.path = 'foo.bar.baz'


@then('returns the value for the nested key')
def step_impl(context):
    assert_that(context.result, equal_to(context.dict['foo']['bar']['baz']))


@given('a dict with a missing nested key')
def step_impl(context):
    context.dict = {
        'foo': {
            'wrong_key': {
                'baz': 'hello'
            }
        }
    }
    context.path = 'foo.bar.baz'


@given('a dict that is None')
def step_impl(context):
    context.dict = None
    context.path = 'foo.bar.baz'


@given('a dict with a nested array index')
def step_impl(context):
    context.dict = {
        'foo': {
            'bar': [
                [{'baz': {'0': False}}],
                [{'baz': {'0': True}}]
            ]
        }
    }
    context.path = 'foo.bar[1][0].baz.0'


@then('returns the nested key value')
def step_impl(context):
    assert_that(context.result, equal_to(context.dict['foo']['bar'][1][0]['baz']['0']))


@given('a dict with a missing nested key and default')
def step_impl(context):
    context.dict = {
        'foo': {
            'wrong_key': {
                'baz': 'hello'
            }
        }
    }
    context.path = 'foo.bar.baz'
    context.default = 'default'


@when('we deep get with a default')
def step_impl(context):
    context.result = deep_get(context.dict, context.path, context.default)


@then('returns the default as the value')
def step_impl(context):
    assert_that(context.result, equal_to('default'))


@given('a dict with a nested negative array index')
def step_impl(context):
    context.dict = {
        'foo': {
            'bar': [
                [{'baz': {'0': False}}],
                [{'baz': {'0': True}}, {'baz': {'0': False}}]
            ]
        }
    }
    context.path = 'foo.bar[-1][-1].baz.0'


@then('returns the nested negative index key value')
def step_impl(context):
    assert_that(context.result, equal_to(context.dict['foo']['bar'][-1][-1]['baz']['0']))
