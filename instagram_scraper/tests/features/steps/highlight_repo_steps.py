from behave import given, when, then
from mock import MagicMock
from requests import Session, HTTPError

from instagram_scraper.repos import HighlightRepo


@given('a session and highlight repo')
def highlight_repo(context):
    context.session = MagicMock(spec=Session)
    context.highlight_repo = HighlightRepo(context.session)


@when('find highlights fails')
def step_impl(context):
    context.failure = MagicMock()
    context.error = HTTPError('error')
    context.session.get.side_effect = context.error

    context.highlight_repo.find(user_id=context.user_id,
                                success=None,
                                failure=context.failure)


@then('calls the find highlights failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)


@when('find highlights succeeds with no highlights')
def step_impl(context):
    context.success = MagicMock()
    context.session.get.return_value.json.return_value = {
        'data': {
            'user': {
                'edge_highlight_reels': {
                    'edges': []
                }
            }
        }
    }

    context.highlight_repo.find(user_id=context.user_id,
                                success=context.success,
                                failure=None)


@then('calls the find highlights success callback with an empty list')
def step_impl(context):
    context.success.assert_called_with([])


@when('find highlights succeeds with highlights')
def step_impl(context):
    context.success = MagicMock()
    context.items = [
        {
            'node': {
                '__typename': 'GraphHighlightReel',
                'id': '1'
            }
        },
        {
            'node': {
                '__typename': 'GraphHighlightReel',
                'id': '2'
            }
        }
    ]

    context.session.get.return_value.json.return_value = {
        'data': {
            'user': {
                'edge_highlight_reels': {
                    'edges': context.items
                }
            }
        }
    }

    context.highlight_repo.find(user_id=context.user_id,
                                success=context.success,
                                failure=None)


@then('calls the find highlights success callback with a list of highlights')
def step_impl(context):
    context.success.assert_called_with([item['node'] for item in context.items])


@given('a list of highlight reel ids')
def step_impl(context):
    context.highlight_reel_ids = ['1', '2', '3']


@when('find highlight media fails')
def step_impl(context):
    context.failure = MagicMock()
    context.error = HTTPError('error')
    context.session.get.side_effect = context.error

    context.highlight_repo.find_media(highlight_reel_ids=context.highlight_reel_ids,
                                      success=None,
                                      failure=context.failure)


@then('calls the find highlight media failure callback with the exception')
def step_impl(context):
    context.failure.assert_called_with(context.error)


@when('find highlight media succeeds with no media')
def step_impl(context):
    context.success = MagicMock()
    context.session.get.return_value.json.return_value = {
        'data': {
            'reels_media': []
        }
    }

    context.highlight_repo.find_media(highlight_reel_ids=context.highlight_reel_ids,
                                      success=context.success,
                                      failure=None)


@then('calls the find highlight media success callback with an empty list')
def step_impl(context):
    context.success.assert_called_with([])


@when('find highlight media succeeds with media')
def step_impl(context):
    context.success = MagicMock()
    context.reels_media = [
        {
            'items': [
                {
                    '__typename': 'GraphStoryVideo',
                    'video_resources': [
                        {'src': 'src'}
                    ]
                },
                {
                    '__typename': 'GraphStoryImage',
                    'display_resources': [
                        {'src': 'src'}
                    ]
                }
            ]
        },
        {
            'items': [
                {
                    '__typename': 'GraphStoryImage',
                    'display_resources': [
                        {'src': 'src'}
                    ]
                }
            ]
        }
    ]

    context.session.get.return_value.json.return_value = {
        'data': {
            'reels_media': context.reels_media
        }
    }

    context.highlight_repo.find_media(highlight_reel_ids=context.highlight_reel_ids,
                                      success=context.success,
                                      failure=None)


@then('calls the find highlight media success callback with a list of media')
def step_impl(context):
    context.success.assert_called_with(context.reels_media)
