class TestBase(object):
    def test_base(self, __opts__, __grains__):
        assert __grains__['dc'] == __opts__['id']
