import logging

log = logging.getLogger(__name__)

__virtualname__ = 'example'


def __virtual__():
    return __virtualname__


def returner(ret):
    log.info(ret)
