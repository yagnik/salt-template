import logging

log = logging.getLogger(__name__)


def __virtual__():
    return 'example'


def run():
    return True
