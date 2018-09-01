from behave import given, when, then
from mock import patch

from instagram_scraper.helpers import save_json


@given('a json object to be saved')
def step_impl(context):
    context.json = {'foo': 'bar'}
    context.dest = './file.json'


@when('we save the json to a file and the dest exists')
def step_impl(context):
    with patch('%s.open' % __name__, create=True) as open_mock, \
            patch('json.dump') as dump_mock, \
            patch('os.path.exists') as path_exists_mock, \
            patch('codecs.getwriter') as getwriter_mock:
        path_exists_mock.return_value = True
        context.open_mock = open_mock
        context.dump_mock = dump_mock
        context.getwriter = getwriter_mock

        save_json(context.json, context.dest)


@when('we save the json to a file and the dest does not exist')
def step_impl(context):
    with patch('%s.open' % __name__, create=True) as open_mock, \
            patch('json.dump') as dump_mock, \
            patch('os.path.exists') as path_exists_mock, \
            patch('os.makedirs') as makedirs_mock, \
            patch('codecs.getwriter') as getwriter_mock:
        path_exists_mock.return_value = False

        context.makedirs = makedirs_mock
        context.open_mock = open_mock
        context.dump_mock = dump_mock
        context.getwriter = getwriter_mock

        save_json(context.json, context.dest)


@then('creates the destination directory')
def step_impl(context):
    context.makedirs.assert_called()


@then('calls open to write the json to the file')
def step_impl(context):
    context.open_mock.assert_called_with(context.dest, 'wb')
    context.dump_mock.assert_called()
    context.getwriter.assert_called()
