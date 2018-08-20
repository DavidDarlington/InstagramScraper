import os
import errno


def make_destination_dir(destination_path):
    try:
        os.makedirs(destination_path)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(destination_path):
            # Directory already exists
            pass
        else:
            # Target dir exists as a file, or a different error
            raise
