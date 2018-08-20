import re

ends_with_index = re.compile(r'\[(.*?)\]$')  # foo[0]
split_array_index = re.compile(r'[.\[\]]+')  # ['foo', '0']


def deep_get(dict, path, default=None):
    keylist = path.split('.')

    val = dict

    for key in keylist:
        try:
            if ends_with_index.search(key):
                for prop in _split_indexes(key):
                    if prop.lstrip('-').isdigit():
                        val = val[int(prop)]
                    else:
                        val = val[prop]
            else:
                val = val[key]
        except (KeyError, IndexError, TypeError):
            return default

    return val


def _split_indexes(key):
    return filter(None, split_array_index.split(key))