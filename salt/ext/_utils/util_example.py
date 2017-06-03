import logging

log = logging.getLogger(__name__)

def __virtual__():
    return 'util_example'

def help():
    return "I'm helping"
