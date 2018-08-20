import logging

from instagram_scraper.helpers import get_hashtags, deep_get

log = logging.getLogger(__name__)


def process_node(node, include_location, media_repo):

    if 'tags' not in node:
        node['tags'] = get_hashtags(node)

    if 'urls' not in node:
        node['urls'] = []

    if 'location' not in node:
        node['location'] = None

    details = None

    if include_location and not node['location']:
        _get_media_details(node, details, media_repo)
        return node

    media_type = node['__typename']

    if media_type == 'GraphImage':
        node['urls'].append(node['display_url'])
    elif media_type == 'GraphVideo':
        if 'video_url' in node:
            node['urls'].append(node['video_url'])
        else:
            _get_media_details(node, details, media_repo)

    elif media_type == 'GraphSidecar':
        carousel_items = deep_get(node, 'edge_sidecar_to_children.edges')

        if carousel_items:
            for carousel_item in carousel_items:
                node['urls'] += process_node(carousel_item['node'], False, media_repo)['urls']
        else:
            _get_media_details(node, details, media_repo)

    return node


def _get_media_details(node, details, media_repo):
    try:
        if details is None:
            details = media_repo.get_media_details(node['shortcode'])

        node['location'] = details.get('location') if details else None

        node['urls'] += process_node(details, False, media_repo)['urls']
    except Exception as e:
        log.exception('failed to get media details for shortcode=' + node['shortcode'])

