from behave import given, when, then
from mock import MagicMock
from requests import HTTPError

from instagram_scraper.use_cases import get_highlights


@given('a mock session and highlight repo')
def step_impl(context):
    context.session = MagicMock()
    context.highlight_repo = MagicMock()


@given('a user, observer, and highlight repo')
def step_impl(context):
    context.user = {'id': 'user id'}

    context.destination = './'
    context.future_to_item = {}
    context.observer = MagicMock()


@when('get highlights succeeds')
def step_impl(context):
    context.reels = [
        {'id': '1'},
        {'id': '2'}
    ]

    def find_fake(**kwargs):
        kwargs['success'](context.reels)

    context.reels_media = [
        {'items': ['item 1']},
        {'items': ['item 2']}
    ]

    def find_media_fake(**kwargs):
        kwargs['success'](context.reels_media)

    context.highlight_repo.find.side_effect = find_fake
    context.highlight_repo.find_media.side_effect = find_media_fake

    get_highlights(user=context.user,
                   observer=context.observer,
                   highlight_repo=context.highlight_repo)


@then('calls the get highlights success callback with the highlights media')
def step_impl(context):
    context.observer.get_highlights_success.assert_called_with(['item 1', 'item 2'])


@when('get highlights fails')
def step_impl(context):
    context.exception = HTTPError('error')

    def find_fake(**kwargs):
        kwargs['failure'](context.exception)

    context.highlight_repo.find.side_effect = find_fake

    get_highlights(user=context.user,
                   observer=context.observer,
                   highlight_repo=context.highlight_repo)


@then('calls the get highlights failure callback with the exception')
def step_impl(context):
    context.observer.get_highlights_error.assert_called_with(context.exception)


@when('get highlights returns no media')
def step_impl(context):
    context.reels = []

    def find_fake(**kwargs):
        kwargs['success'](context.reels)

    context.highlight_repo.find.side_effect = find_fake

    get_highlights(user=context.user,
                   observer=context.observer,
                   highlight_repo=context.highlight_repo)


@then('calls the get highlights empty callback')
def step_impl(context):
    context.observer.get_highlights_empty.assert_called()
