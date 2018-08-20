import json
import codecs
import logging

log = logging.getLogger(__name__)


def save_json(data, dst='./data.json'):
    with open(dst, 'wb') as f:
        json.dump(data,
                  codecs.getwriter('utf-8')(f),
                  indent=4,
                  sort_keys=True,
                  ensure_ascii=False)