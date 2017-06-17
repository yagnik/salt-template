from tests import TestMinion


class TestExample(TestMinion):
    def test_pillar(self, __utils__):
        assert __utils__['example.help']() == "I'm trying to help again"
