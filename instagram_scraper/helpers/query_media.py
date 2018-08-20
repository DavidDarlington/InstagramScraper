import logging

from instagram_scraper.helpers import deep_get

log = logging.getLogger(__name__)


def query_media(user_id, end_cursor, media_repo):

    user = media_repo.query_media(user_id=user_id, end_cursor=end_cursor)

    nodes = deep_get(user, 'edge_owner_to_timeline_media.edges')

    if not nodes:
        return None, None

    end_cursor = deep_get(user, 'page_info.end_cursor')

    return nodes, end_cursor
