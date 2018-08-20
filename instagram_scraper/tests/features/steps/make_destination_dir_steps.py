from behave import given, when, then
from mock import patch
from hamcrest import assert_that, equal_to, instance_of
import errno

from instagram_scraper.helpers import make_destination_dir


@given('a destination path to make')
def step_impl(context):
    context.destination_path = '/tmp'


@when('we make the destination directory')
def step_impl(context):
    with patch('os.makedirs') as makedirs_mock:
        context.makedirs = makedirs_mock
        make_destination_dir(destination_path=context.destination_path)


@then('makes the destination directory')
def step_impl(context):
    context.makedirs.assert_called_with(context.destination_path)


@when('we make the destination directory and it already exists')
def step_impl(context):
    with patch('os.makedirs') as makedirs_mock, patch('os.path.isdir') as isdir_mock:
        makedirs_mock.side_effect = OSError(errno.EEXIST, 'error')
        isdir_mock.return_value = True

        context.result = make_destination_dir(destination_path=context.destination_path)


@when('we make the destination directory and it fails due to error')
def step_impl(context):
    with patch('os.makedirs') as makedirs_mock:
        makedirs_mock.side_effect = OSError

        try:
            make_destination_dir(destination_path=context.destination_path)
        except Exception as e:
            context.e = e


@then('raises an os error from makedirs')
def step_impl(context):
    assert_that(context.e, instance_of(OSError))
