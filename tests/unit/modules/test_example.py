class TestExample(object):
    def test_func(self, __salt__):
        assert __salt__['example.func']()

    def util_func(self, __salt__, __utils__):
        # figure out a way to overwrite util
        assert __salt__['example.util_func']() == "I'm helping"
