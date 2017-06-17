import pytest
import salt.config
import salt.loader
import salt.client

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
