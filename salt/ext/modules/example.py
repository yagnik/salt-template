import logging

log = logging.getLogger(__name__)


def __virtual__():
    return 'example'


def func():
    return False


def util_func():
    return __utils__['example.help']()
