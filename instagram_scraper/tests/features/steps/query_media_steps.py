from behave import given, when, then
from hamcrest import equal_to, assert_that
from mock import MagicMock

from instagram_scraper.helpers import query_media


@given('a fake media repo')
def step_impl(context):
    context.media_repo = MagicMock()


@when('query media returns no media')
def step_impl(context):
    def query_media_fake(**kwargs):
        return [], None

    context.media_repo.query_media.side_effect = query_media_fake

    context.result = query_media(user_id=context.user_id,
                                 end_cursor=context.end_cursor,
                                 media_repo=context.media_repo)


@then('returns no nodes and no end cursor')
def step_impl(context):
    assert_that(context.result, equal_to((None, None)))


@when('query media returns media with no end cursor')
def step_impl(context):
    def query_media_fake(**kwargs):
        context.nodes = [
            {'node': {}},
            {'node': {}}
        ]

        return {
            'edge_owner_to_timeline_media': {
                'edges': context.nodes
            }
        }

    context.media_repo.query_media.side_effect = query_media_fake

    context.result = query_media(user_id=context.user_id,
                                 end_cursor=context.end_cursor,
                                 media_repo=context.media_repo)


@then('returns media and no end cursor')
def step_impl(context):
    assert_that(context.result, equal_to(([node['node'] for node in context.nodes], None)))


@when('query media returns media with an end cursor')
def step_impl(context):
    def query_media_fake(**kwargs):
        context.nodes = [
            {'node': {}},
            {'node': {}}
        ]

        return {
            'edge_owner_to_timeline_media': {
                'edges': context.nodes,
                'page_info': {
                    'end_cursor': 9
                }
            }
        }

    context.media_repo.query_media.side_effect = query_media_fake

    context.result = query_media(user_id=context.user_id,
                                 end_cursor=context.end_cursor,
                                 media_repo=context.media_repo)


@then('returns media and end cursor')
def step_impl(context):
    assert_that(context.result, equal_to(([node['node'] for node in context.nodes], 9)))
