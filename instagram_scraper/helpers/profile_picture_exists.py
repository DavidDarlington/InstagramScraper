import os


def profile_picture_exists(dir, url):
    file_name = url.split('/')[-1]

    profile_pic_path = os.path.join(dir, file_name)

    return os.path.isfile(profile_pic_path)