class TestExample(object):
    def test_pillar(self, __salt__):
        # using get is not enough cause get doesn't go to master to refresh pillar
        # items refreshes pillar
        assert __salt__['pillar.items']()['example_pillar'] == 1
        assert __salt__['pillar.items']()['example_pillar2'] == 2
