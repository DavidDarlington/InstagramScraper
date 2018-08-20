import glob
import os


def get_last_scraped_filemtime(dir):
    """Gets the last modified time of newest file in a directory."""
    files = []

    for file_type in ('*.jpg', '*.mp4'):
        files.extend(glob.glob(os.path.join(dir, file_type)))

    if files:
        latest_file = max(files, key=os.path.getmtime)
        return int(os.path.getmtime(latest_file))

    return 0
