def get_highlights(user, observer, highlight_repo):
    def success(reels):
        if not reels:
            observer.get_highlights_empty()
            return

        def _success(reels_media):
            media = []

            for reel_media in reels_media:
                media.extend(reel_media['items'])

            observer.get_highlights_success(media)

        def _failure(exception):
            observer.get_highlights_error(exception)

        highlight_reel_ids = [reel['id'] for reel in reels]

        highlight_repo.find_media(highlight_reel_ids=highlight_reel_ids,
                                  success=_success,
                                  failure=_failure)

    def failure(exception):
        observer.get_highlights_error(exception)

    highlight_repo.find(user_id=user['id'],
                        success=success,
                        failure=failure)
