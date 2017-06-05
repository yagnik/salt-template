class TestBase(object):
    def test_base(self, __grains__):
        assert __grains__['environment'] == ''
