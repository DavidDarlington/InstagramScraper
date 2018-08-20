import re


def parse_delimited_str(input):
    """Parse the string input as a list of delimited tokens."""
    assert input is not None

    return re.findall(r'[^,;\s]+', input)