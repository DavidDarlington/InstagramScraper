from behave import given, when, then
from mock import MagicMock
from requests import Session, HTTPError

from instagram_scraper.repos import StoryRepo


@given('a session and story repo')
def story_repo(context):
    context.session = MagicMock(spec=Session)
    context.story_repo = StoryRepo(context.session)


@given('user id')
def step_impl(context):
    context.user_id = 'user id'


@when('find stories fails')
def step_impl(context):
    context.failure = MagicMock()
    context.error = HTTPError('error')
    context.session.get.side_effect = context.error

    context.story_repo.find(user_id=context.user_id,
                            success=None,
                            failure=context.failure)


@then('calls the find stories failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)


@when('find stories succeeds with no stories')
def step_impl(context):
    context.success = MagicMock()
    context.session.get.return_value.json.return_value = {
        'data': {
            'reels_media': []
        }
    }

    context.story_repo.find(user_id=context.user_id,
                            success=context.success,
                            failure=None)


@then('calls the find stories success callback with an empty list')
def step_impl(context):
    context.success.assert_called_with([])


@when('find stories succeeds with stories')
def step_impl(context):
    context.success = MagicMock()
    context.items = [
        {
            'video_versions': [{'url': 'url1'}],
            'image_versions2': {
                'candidates': [{'url': 'url2'}]
            }
        },
        {
            'image_versions2': {
                'candidates': [{'url': 'url3'}]
            }
        },
        {
            'video_versions': [{'url': 'url4'}]
        }
    ]

    context.session.get.return_value.json.return_value = {
        'data': {
            'reels_media': [
                {'items': context.items}
            ]
        }
    }

    context.story_repo.find(user_id=context.user_id,
                            success=context.success,
                            failure=None)


@then('calls the find stories success callback with a list of stories')
def step_impl(context):
    context.items[0]['urls'] = ['url1', 'url2', 'url3', 'url4']
    context.success.assert_called_with(context.items)
