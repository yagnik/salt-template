import pytest
import os
from tests import TestMaster
from tests import TestMinion


ROOT = os.path.abspath("%s/../../" % os.path.dirname(os.path.realpath(__file__)))
STATE_PATH = os.path.join(ROOT, "salt/states")
ENV_STATE_LIST = []
for env in os.listdir(STATE_PATH):
    for state in os.listdir(os.path.join(STATE_PATH, env)):
        for version in os.listdir(os.path.join(STATE_PATH, env, state)):
            if version != "latest.sls":
                ENV_STATE_LIST.append((env, state, version))


class TestStateMasterMinion(TestMaster):
    @pytest.mark.parametrize("env, state, version", ENV_STATE_LIST)
    def test_states_execution(self, __salt_mastercall__, env, state, version):
        total_results = __salt_mastercall__.cmd('*', 'state.sls', arg=["%s.%s.requisite" % (state, version)], kwarg={'saltenv': env})
        for minion_id, results in total_results.iteritems():
            for result in results.values():
                assert result['result'], "%s state requisite failed to apply in env %s" % (state, env)

        total_results = __salt_mastercall__.cmd('*', 'state.sls', arg=["%s.%s" % (state, version)], kwarg={'saltenv': env})
        for minion_id, results in total_results.iteritems():
            for result in results.values():
                assert result['result'], "%s state failed to apply in env %s" % (state, env)


        total_results = __salt_mastercall__.cmd('*', 'state.sls', arg=["%s.%s.verify" % (state, version)], kwarg={'saltenv': env})
        for minion_id, results in total_results.iteritems():
            for result in results.values():
                assert result['result'], "%s state verification failed to apply in env %s" % (state, env)


class TestStateMinion(TestMinion):
    @pytest.mark.parametrize("env, state, version", ENV_STATE_LIST)
    def test_states_parsing(self, __salt_call__, env, state, version):
        state_sls = __salt_call__.cmd('state.show_sls', "%s.%s" % (state, version), saltenv=env)
        assert type(state_sls) == dict

    @pytest.mark.parametrize("env, state, version", ENV_STATE_LIST)
    @pytest.mark.usefixtures("filesystem_watch")
    def test_states_execution(self, __salt_call__, env, state, version):
        total_results = __salt_call__.cmd('state.sls', "%s.%s.requisite" % (state, version), saltenv=env)
        for result in total_results.values():
            assert result['result'], "%s state requisite failed to apply in env %s" % (state, env)

        total_results = __salt_call__.cmd('state.sls', "%s.%s" % (state, version), saltenv=env)
        for result in total_results.values():
            assert result['result'], "%s state failed to apply in env %s" % (state, env)

        total_results = __salt_call__.cmd('state.sls', "%s.%s.verify" % (state, version), saltenv=env)
        for result in total_results.values():
            assert result['result'], "%s state verification failed to apply in env %s" % (state, env)
