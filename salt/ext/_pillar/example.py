import logging

log = logging.getLogger(__name__)
__virtualname__ = 'example'


def __virtual__():
    return __virtualname__


def ext_pillar(minion_id, pillar, *args, **kwargs):
    return {
        'example_pillar': 1,
        'example_pillar2': 2
    }
