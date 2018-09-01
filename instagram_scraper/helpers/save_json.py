import codecs
import json
import logging
import os

log = logging.getLogger(__name__)


def save_json(data, dst='./data.json'):
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    with open(dst, 'wb') as f:
        json.dump(data,
                  codecs.getwriter('utf-8')(f),
                  indent=4,
                  sort_keys=True,
                  ensure_ascii=False)
