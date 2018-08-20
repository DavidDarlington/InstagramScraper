from behave import given, when, then
from mock import MagicMock
from requests import HTTPError

from instagram_scraper.use_cases import get_stories


@given('a mock session and story repo')
def step_impl(context):
    context.session = MagicMock()
    context.story_repo = MagicMock()


@given('a user, observer, and story repo')
def step_impl(context):
    context.user = {'id': 'user id'}

    context.destination = './'
    context.future_to_item = {}
    context.observer = MagicMock()


@when('get stories succeeds')
def step_impl(context):
    context.stories = [
        {'urls': ['url1', 'url2']},
        {'urls': ['url3', 'url4']}
    ]

    def find_fake(**kwargs):
        kwargs['success'](context.stories)

    context.story_repo.find.side_effect = find_fake

    get_stories(user=context.user,
                observer=context.observer,
                story_repo=context.story_repo)


@then('calls the get stories success callback with the stories')
def step_impl(context):
    context.observer.get_stories_success.assert_called_with(context.stories)


@when('get stories fails')
def step_impl(context):
    context.exception = HTTPError('error')

    def find_fake(**kwargs):
        kwargs['failure'](context.exception)

    context.story_repo.find.side_effect = find_fake

    get_stories(user=context.user,
                observer=context.observer,
                story_repo=context.story_repo)


@then('calls the get stories failure callback with the exception')
def step_impl(context):
    context.observer.get_stories_error.assert_called_with(context.exception)


@when('get stories returns no stories')
def step_impl(context):
    context.stories = []

    def find_fake(**kwargs):
        kwargs['success'](context.stories)

    context.story_repo.find.side_effect = find_fake

    get_stories(user=context.user,
                observer=context.observer,
                story_repo=context.story_repo)


@then('calls the get stories empty callback')
def step_impl(context):
    context.observer.get_stories_empty.assert_called()
