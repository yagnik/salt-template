import pytest
import socket
import salt


SALT_BASE_PATH = "/srv/salt"


class TestBase(object):
    pass


@pytest.mark.skipif("master" not in socket.gethostname(), reason="Skipping cause test only runs on master")
class TestMaster(TestBase):

    @pytest.fixture
    def __salt_mastercall__(self):
        return salt.client.LocalClient()


@pytest.mark.skipif("master" in socket.gethostname(), reason="Skipping cause test only runs on master")
class TestMinion(TestBase):

    @pytest.fixture
    def __salt_call__(self):
        return salt.client.Caller()
