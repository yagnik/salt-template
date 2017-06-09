import logging


log = logging.getLogger(__name__)


def base():
    return {
        "dc": __opts__['id'],
        "environment": "a",
        "organization": "",
        "namespace": "",
        "service": "",
        "type": "",
    }
