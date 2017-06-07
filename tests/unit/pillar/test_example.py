class TestExample(object):
    def test_pillar(self, __salt__):
        assert __salt__['pillar.get']('example_pillar') == 1
        assert __salt__['pillar.get']('example_pillar2') == 2
