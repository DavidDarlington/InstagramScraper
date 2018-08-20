from behave import given, when, then
from hamcrest import assert_that, equal_to, instance_of
from mock import patch, mock_open

from instagram_scraper.helpers import parse_usernames_file


@given('we have a file that does not exist')
def step_impl(context):
    context.file_path = '/path/to/invalid/file'


@when('we try to parse the file')
def step_impl(context):
    try:
        context.result = parse_usernames_file(context.file_path)
    except Exception as e:
        context.e = e


@then('throws an error')
def step_impl(context):
    assert_that(context.e, instance_of(Exception))


@given('we have an empty file')
def step_impl(context):
    context.file_path = '/path/to/invalid/file'


@when('we try to parse the empty file')
def step_impl(context):
    open_name = '%s.open' % __name__
    with patch(open_name, mock_open(read_data='')):
        context.result = parse_usernames_file(context.file_path)


@given('we have a file with a single user')
def step_impl(context):
    context.file_path = '/path/to/valid/file'


@when('we try to parse a file with a single user')
def step_impl(context):
    open_name = '%s.open' % __name__
    with patch(open_name, mock_open(read_data='user')):
        context.result = parse_usernames_file(context.file_path)


@then('returns a list with a single user')
def step_impl(context):
    assert_that(context.result, equal_to(['user']))


@given('we have a file with several users')
def step_impl(context):
    context.file_path = '/path/to/valid/file'


@when('we try to parse a file with several users')
def step_impl(context):
    open_name = '%s.open' % __name__
    with patch(open_name, mock_open(read_data='''\n\n
        user1 
        user2,user3 ;,user4
        , user5\t\tuser6;
        ;user7
    ,,
    ''')):
        context.result = parse_usernames_file(context.file_path)


@then('returns a list with several users')
def step_impl(context):
    assert_that(context.result, equal_to([
        'user1',
        'user2',
        'user3',
        'user4',
        'user5',
        'user6',
        'user7'
    ]))