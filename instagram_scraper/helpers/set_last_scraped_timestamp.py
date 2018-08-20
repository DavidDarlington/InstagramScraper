from instagram_scraper.constants import LATEST_STAMPS_USER_SECTION


def set_last_scraped_timestamp(parser, latest_stamps_file, username, timestamp):
    if not parser:
        return

    if not parser.has_section(LATEST_STAMPS_USER_SECTION):
        parser.add_section(LATEST_STAMPS_USER_SECTION)

    parser.set(LATEST_STAMPS_USER_SECTION, username, str(timestamp))

    with open(latest_stamps_file, 'w') as f:
        parser.write(f)

