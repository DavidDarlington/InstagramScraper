from instagram_scraper.repos.auth_repo import AuthRepo
from instagram_scraper.repos.challenge_repo import ChallengeRepo
from instagram_scraper.repos.highlight_repo import HighlightRepo
from instagram_scraper.repos.location_repo import LocationRepo
from instagram_scraper.repos.media_repo import MediaRepo
from instagram_scraper.repos.story_repo import StoryRepo
from instagram_scraper.repos.user_repo import UserRepo


class RepoFactory(object):

    def __init__(self, session):
        self.session = session

    def get_auth_repo(self):
        return AuthRepo(self.session)

    def get_challenge_repo(self):
        return ChallengeRepo(self.session)

    def get_highlight_repo(self):
        return HighlightRepo(self.session)

    def get_location_repo(self):
        return LocationRepo(self.session)

    def get_media_repo(self):
        return MediaRepo(self.session)

    def get_story_repo(self):
        return StoryRepo(self.session)

    def get_user_repo(self):
        return UserRepo(self.session)