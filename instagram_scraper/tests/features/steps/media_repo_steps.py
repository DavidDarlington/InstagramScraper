from behave import given, when, then
from mock import MagicMock
from hamcrest import assert_that, equal_to
from requests import Session, HTTPError

from instagram_scraper.constants import STORIES_UA
from instagram_scraper.repos import MediaRepo


@given('a media repo')
def media_repo(context):
    context.session = MagicMock(spec=Session)
    context.session.headers = MagicMock(update=MagicMock())
    context.media_repo = MediaRepo(context.session)


@given('a user id and end cursor')
def step_impl(context):
    context.user_id = 'user id'
    context.end_cursor = 1


@when('query media succeeds')
def step_impl(context):
    context.user = {'id': 123}
    context.session.get.return_value.json.return_value = {
        'data': {
            'user': context.user
        }
    }

    context.result = context.media_repo.query_media(user_id=context.user_id,
                                                    end_cursor=context.end_cursor)


@then('updates the user-agent header to the stories user agent')
def step_impl(context):
    context.session.headers.update.assert_called_with({'user-agent': STORIES_UA})


@then('returns the user\'s media data')
def step_impl(context):
    assert_that(context.result, equal_to(context.user))


@when('query media fails')
def step_impl(context):
    context.error = HTTPError('error')
    context.session.get.side_effect = context.error

    try:
        context.media_repo.query_media(user_id=context.user_id,
                                       end_cursor=context.end_cursor)
    except Exception as e:
        context.exception = e


@then('raises the exception that caused the query media failure')
def step_impl(context):
    assert_that(context.exception, equal_to(context.error))


@given('a short code')
def step_impl(context):
    context.short_code = 'short code'


@when('get media details succeeds')
def step_impl(context):
    context.session.get.return_value.json.return_value = {
        'graphql': {
            'shortcode_media': {}
        }
    }

    context.result = context.media_repo.get_media_details(short_code=context.short_code)


@then('returns the media details')
def step_impl(context):
    assert_that(context.result, equal_to({}))


@when('get media details fails')
def step_impl(context):
    context.error = HTTPError('error')
    context.session.get.side_effect = context.error

    try:
        context.result = context.media_repo.get_media_details(short_code=context.short_code)
    except Exception as e:
        context.exception = e


@then('raises the exception that caused the get media details failure')
def step_impl(context):
    assert_that(context.exception, equal_to(context.error))
