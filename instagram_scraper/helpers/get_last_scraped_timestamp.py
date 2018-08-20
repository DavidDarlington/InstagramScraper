import configparser

from instagram_scraper.constants import LATEST_STAMPS_USER_SECTION


def get_last_scraped_timestamp(parser, username):
    if parser:
        try:
            return parser.getint(LATEST_STAMPS_USER_SECTION, username)
        except configparser.Error:
            pass

    return 0

