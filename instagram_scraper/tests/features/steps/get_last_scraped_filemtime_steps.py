from behave import given, when, then
from mock import patch
from hamcrest import assert_that, equal_to
from operator import itemgetter

from instagram_scraper.helpers import get_last_scraped_filemtime


@given('a directory')
def step_impl(context):
    context.dir = 'dir'
    context.mock_files = []


@when('the directory does not contain jpg or mp4 files')
def step_impl(context):
    pass


@when('we get the last modified time of the newest file')
def step_impl(context):
    with patch('glob.glob') as glob_mock, \
            patch('os.path.getmtime') as getmtime_mock:

        glob_mock.side_effect = [context.mock_files, []]  # return mock files once
        getmtime_mock.side_effect = __mock_getmtime

        context.filemtime = get_last_scraped_filemtime('/')


@then('returns 0 as the filemtime')
def step_impl(context):
    assert_that(context.filemtime, equal_to(0))


@when('the directory contains mp4 files')
def step_impl(context):
    context.mock_files.extend([
        {'filename': 'oldest.mp4', 'mtime': 1},
        {'filename': 'newest.mp4', 'mtime': 1000},
        {'filename': 'older.mp4', 'mtime': 2},
    ])


@when('the directory contains jpg files')
def step_impl(context):
    context.mock_files.extend([
        {'filename': 'newest.jpg', 'mtime': 999}
    ])


@then('returns the filemtime of the latest file')
def step_impl(context):
    latest_file = max(context.mock_files, key=__mock_getmtime)

    assert_that(context.filemtime, equal_to(latest_file['mtime']))


def __mock_getmtime(file):
    return file['mtime']