class TestExample(object):
    def test_pillar(self, __utils__):
        assert __utils__['example.help']() == "I'm trying to help again"
