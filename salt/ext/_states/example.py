import logging

log = logging.getLogger(__name__)


def __virtual__():
    return 'example'


def managed(name):
    ret = {
        'name': 'example',
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {}
    }

    current_state = __salt__['example.func']()
    if current_state is True:
        ret['result'] = True
        ret['comment'] = 'System is already in the correct state'
        return ret

    if __opts__['test'] is True:
        ret['comment'] = 'The state will be changed.'
        ret['pchanges'] = {
            'old': current_state,
            'new': 'Description, diff, whatever of the new state',
        }
        # Return ``None`` when running with ``test=true``.
        ret['result'] = None
        return ret

    new_state = __salt__['example.util_func']()
    ret['comment'] = 'The state of was changed!'
    ret['changes'] = {
        'old': current_state,
        'new': new_state,
    }
    ret['result'] = True
    return ret
