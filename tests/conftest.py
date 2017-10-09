import pytest
import salt.config
import salt.loader
import salt.client
from utils.path import PathHelper
# import watchdog
# import time

_config = '/etc/salt/minion'
_opts = salt.config.minion_config(_config)
_opts['pillar_raise_on_missing'] = True
_grains = salt.loader.grains(_opts)
_opts['grains'] = _grains
_utils = salt.loader.utils(_opts)
_salt = salt.loader.minion_mods(_opts, utils=_utils)


@pytest.fixture
def __opts__():
    return _opts


@pytest.fixture
def __grains__():
    return _grains


@pytest.fixture
def __utils__():
    return _utils


@pytest.fixture
def __salt__():
    return _salt


@pytest.fixture
def __envs__():
    return ['base', 'dev', 'stg', 'prd']


@pytest.fixture
def path_helper():
    return PathHelper
# from watchdog.observers import Observer
# from watchdog.events import PatternMatchingEventHandler
# class MyEventHandler(PatternMatchingEventHandler):
#     def __init__(self, ignore_patterns):
#         super(MyEventHandler, self).__init__(ignore_patterns=ignore_patterns)
#         self.files = []
#     def on_any_event(self, event):
#         self.files.append(event.src_path)


# @pytest.fixture
# def filesystem_watch(env, state):
#     pass
#     event_handler = MyEventHandler(ignore_patterns=["/var/cache/*", "/var/log/*", "/tmp/*"])
#     observer = Observer()
#     observer.schedule(event_handler, "/", recursive=True)
#     observer.start()
#     yield
#     time.sleep(2)
#     observer.stop()
#     observer.join()
#     print event_handler.files
#     assert False
