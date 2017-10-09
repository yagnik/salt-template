import json
import logging
import salt.utils.event

log = logging.getLogger(__name__)


def start():
    if __opts__['__role'] == 'master':
        event_bus = salt.utils.event.get_master_event(__opts__,
                                                      __opts__['sock_dir'],
                                                      listen=True)
    else:
        event_bus = salt.utils.event.get_event(
            'minion',
            transport=__opts__['transport'],
            opts=__opts__,
            sock_dir=__opts__['sock_dir'],
            listen=True)
        log.debug('test engine started')

    while True:
        event = event_bus.get_event()
        jevent = json.dumps(event)
        if event:
            log.debug(jevent)
