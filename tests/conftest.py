import pytest
import salt.config
import salt.loader


@pytest.fixture(scope="function")
def __opts__():
    return _load('opts')


@pytest.fixture(scope="function")
def __grains__():
    return _load('grains')


@pytest.fixture(scope="function")
def __utils__():
    return _load('utils')


@pytest.fixture(scope="function")
def __salt__():
    return _load('salt')


# @TODO(yagnik) this is ugly, could be made better
def _load(name):
    config = '/etc/salt/minion'
    opts = salt.config.minion_config(config)
    grains = salt.loader.grains(opts)
    opts['grains'] = grains
    utils = salt.loader.utils(opts)
    _salt = salt.loader.minion_mods(opts, utils=utils)
    return {
        'opts': opts,
        'grains': grains,
        'utils': utils,
        'salt': _salt
    }[name]
