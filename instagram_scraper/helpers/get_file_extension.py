import os


def get_file_extension(path):
    return os.path.splitext(path)[1][1:].strip().lower()