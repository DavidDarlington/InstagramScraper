from behave import given, when, then
from hamcrest import equal_to, assert_that

from instagram_scraper.helpers import process_node


@given('a node with media type image')
def step_impl(context):
    context.urls = ['https://scontent-lga3-1.cdninstagram.com/vp/00000_n.jpg']
    context.tags = ['test']
    context.location = None

    context.node = {
        '__typename': 'GraphImage',
        'display_url': context.urls[0],
        'caption': {
            'text': ' '.join(['#' + tag for tag in context.tags])
        }
    }


@given('include location is false')
def step_impl(context):
    context.include_location = False


@given('include location is true')
def step_impl(context):
    context.include_location = True


@when('we process the node')
def step_impl(context):
    context.result = process_node(node=context.node,
                                  include_location=context.include_location,
                                  media_repo=context.media_repo)


@then('returns a node with tags and urls')
def step_impl(context):
    assert_that(context.result['urls'], equal_to(context.urls))
    assert_that(context.result['tags'], equal_to(context.tags))
    assert_that(context.result['location'], equal_to(context.location))


@given('a node with media type video')
def step_impl(context):
    context.urls = ['https://scontent-lga3-1.cdninstagram.com/vp/00000_n.mp4']
    context.tags = ['foo', 'bar']
    context.location = None

    context.node = {
        '__typename': 'GraphVideo',
        'video_url': context.urls[0],
        'edge_media_to_caption': {
            'edges': [
                {
                    'node': {
                        'text': ' '.join(['#' + tag for tag in context.tags])
                    }
                }
            ]
        }
    }


@given('a node with media type video with no video url')
def step_impl(context):
    context.urls = ['https://scontent-lga3-1.cdninstagram.com/vp/00000_n.mp4']
    context.tags = []
    context.location = None

    context.node = {
        '__typename': 'GraphVideo',
        'shortcode': 'shortcode'
    }

    context.media_repo.get_media_details.return_value = {
        '__typename': 'GraphVideo',
        'video_url': context.urls[0]
    }


@given('a node with media type sidecar with items')
def step_impl(context):
    context.urls = ['https://scontent-lga3-1.cdninstagram.com/vp/00000_n.jpg']
    context.tags = ['test']
    context.location = None

    context.node = {
        '__typename': 'GraphSidecar',
        'caption': {
            'text': ' '.join(['#' + tag for tag in context.tags])
        },
        'edge_sidecar_to_children': {
            'edges': [
                {
                    'node': {
                        '__typename': 'GraphImage',
                        'display_url': context.urls[0]
                    }
                }
            ]
        }
    }


@given('a node with media type sidecar with no items')
def step_impl(context):
    context.urls = [
        'https://scontent-lga3-1.cdninstagram.com/vp/00000_n.jpg',
        'https://scontent-lga3-1.cdninstagram.com/vp/00000_n.mp4'
    ]
    context.tags = ['test']

    context.location = {
        'id': "00000000000001",
        'has_public_page': True,
        'name': 'name',
        'slug': 'slug'
    }

    context.node = {
        '__typename': 'GraphSidecar',
        'shortcode': 'shortcode',
        'caption': {
            'text': ' '.join(['#' + tag for tag in context.tags])
        }
    }

    context.media_repo.get_media_details.side_effect = [
        {
            '__typename': 'GraphSidecar',
            'location': context.location,
            'edge_sidecar_to_children': {
                'edges': [
                    {
                        'node': {
                            '__typename': 'GraphImage',
                            'display_url': context.urls[0]
                        }
                    },
                    {
                        'node': {
                            '__typename': 'GraphVideo',
                            'shortcode': 'shortcode'
                        }
                    }
                ]
            }
        },
        {
            '__typename': 'GraphVideo',
            'video_url': context.urls[1]
        }
    ]
