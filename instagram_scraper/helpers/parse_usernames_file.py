import re


def parse_usernames_file(file_path):
    """Parse the specified file for a list of usernames."""
    assert file_path is not None

    users = []

    try:
        with open(file_path) as users_file:
            for line in users_file.readlines():
                # Find all usernames delimited by ,; or whitespace
                users += re.findall(r'[^,;\s]+', line.split("#")[0])
    except IOError as err:
        raise ValueError('File not found ' + str(err))

    return users
