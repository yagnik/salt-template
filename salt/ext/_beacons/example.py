import logging

log = logging.getLogger(__name__)

__virtualname__ = 'example'


def __virtual__():
    return __virtualname__


def __validate__(config):
    return True, 'Valid beacon configuration'


def beacon(config):
    return [{'data': 1}]
