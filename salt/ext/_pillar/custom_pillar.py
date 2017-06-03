import logging

log = logging.getLogger(__name__)
__virtualname__ = 'custom_pillar'

def __virtual__():
    return __virtualname__

def ext_pillar(minion_id, pillar, *args, **kwargs):
    return {
        'custom_pillar': 1
    }
