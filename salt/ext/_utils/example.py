import logging

log = logging.getLogger(__name__)


def __virtual__():
    return 'example'


def help():
    return "I'm trying to help again"
