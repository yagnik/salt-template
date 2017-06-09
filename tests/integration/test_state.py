import os
import pytest

class TestState(object):
    ROOT = os.path.abspath("%s/../../" % os.path.dirname(os.path.realpath(__file__)))
    STATE_PATH = os.path.join(ROOT, "salt/states")
    ENV_STATE_LIST = []
    for env in os.listdir(STATE_PATH):
        for state in os.listdir(os.path.join(STATE_PATH, env)):
            ENV_STATE_LIST.append((env, state))

    @pytest.mark.parametrize("env, state", ENV_STATE_LIST)
    def test_states(self, __salt_call__, env, state):
        total_results = __salt_call__.cmd('state.sls', state, saltenv=env)
        for result in total_results.values():
            assert result['result'], "%s state failed to apply in env %s" % (state, env)

        total_results = __salt_call__.cmd('state.sls', "%s.verify" % state, saltenv=env)
        for result in total_results.values():
            assert result['result'], "%s state verification failed to apply in env %s" % (state, env)

