from tests import TestMinion


class TestBase(TestMinion):
    def test_base(self, __opts__, __grains__):
        assert __grains__['dc'] == __opts__['id']
