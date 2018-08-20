import logging

from instagram_scraper.constants import GET_HIGHLIGHT_REELS_URL, HIGHLIGHT_MEDIA_URL
from instagram_scraper.helpers import deep_get

log = logging.getLogger(__name__)


class HighlightRepo(object):

    def __init__(self, session):
        self.session = session

    def find(self, user_id, success, failure):
        try:
            response = self.session.get(GET_HIGHLIGHT_REELS_URL.format(user_id))
            response.raise_for_status()
        except Exception as e:
            log.exception('find highlights for ' + user_id + ' failed')
            failure(e)
        else:
            content = response.json()
            reels = deep_get(content, 'data.user.edge_highlight_reels.edges')

            if reels and len(reels) > 0:
                reels = [reel['node'] for reel in reels]

                success(reels)
            else:
                success([])

    def find_media(self, highlight_reel_ids, success, failure):
        reel_ids = ','.join('%22{0}%22'.format(r) for r in highlight_reel_ids)

        try:
            response = self.session.get(HIGHLIGHT_MEDIA_URL.format(reel_ids))
            response.raise_for_status()
        except Exception as e:
            log.exception('find highlight media for ' + ''.join(highlight_reel_ids) + ' failed')
            failure(e)
        else:
            content = response.json()
            reels_media = deep_get(content, 'data.reels_media')

            if reels_media and len(reels_media) > 0:

                for reel_media in reels_media:
                    for item in reel_media['items']:
                        if item['__typename'] == 'GraphStoryVideo':
                            item['urls'] = [item['video_resources'][-1]['src']]
                        else:
                            item['urls'] = [ item['display_resources'][-1]['src']]

                success(reels_media)
            else:
                success([])