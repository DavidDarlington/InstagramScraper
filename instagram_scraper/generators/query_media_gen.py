import logging

import instagram_scraper.helpers as helpers

log = logging.getLogger(__name__)


def query_media_gen(user, last_scraped_time, media_repo):

    end_cursor = ''

    try:
        media, end_cursor = helpers.query_media(user_id=user['id'],
                                                end_cursor=end_cursor,
                                                media_repo=media_repo)
        if not media:
            return

        while True:
            for item in media:
                item_timestamp = helpers.get_timestamp(item)

                # skip media older than last scrape time
                if item_timestamp <= last_scraped_time:
                    return

                yield item

            if end_cursor:  # there is more media to fetch
                media, end_cursor = helpers.query_media(user_id=user['id'],
                                                        end_cursor=end_cursor,
                                                        media_repo=media_repo)
            else:
                return
    except Exception as e:
        log.exception('failed to query media for user {0} (end_cursor={1}): {2}'.
                      format(user['username'], end_cursor, e.message))
