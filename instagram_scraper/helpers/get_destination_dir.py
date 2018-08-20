import os


def get_destination_dir(destination, retain_username, username):
    if destination == './':
        destination_path = os.path.join('./', username)
    else:
        if retain_username:
            destination_path = os.path.join(destination, username)
        else:
            destination_path = destination

    return destination_path
