import os
import glob

class PathHelper(object):

    @staticmethod
    def state():
        return StatePathHelper()

    @staticmethod
    def pillar():
        return PillarPathHelper()

    @staticmethod
    def orch():
        return OrchPathHelper()

    @staticmethod
    def reactor():
        return ReactorPathHelper()

    @staticmethod
    def ext():
        return ExtPathHelper()

    @staticmethod
    def root_path():
        return os.path.abspath("%s/../../" % os.path.dirname(os.path.realpath(__file__)))

    @staticmethod
    def ext_path():
        return "%s/salt/ext" % PathHelper.root_path()

    @staticmethod
    def test_path():
        return "%s/tests/unit" % PathHelper.root_path()

    def __init__(self):
        self.root_path = PathHelper.root_path()
        self.kind = "*"

    def names(self, env="*"):
        all_files = glob.glob("%s/salt/%s/%s/*" % (self.root_path, env, self.kind))
        filtered_files = filter(lambda file: not file.endswith("/top.sls"), all_files)
        return map(lambda file: os.path.splitext(os.path.basename(file))[0], filtered_files)

    def paths_with_env(self, env="*"):
        return glob.glob("%s/salt/%s/%s" % (self.root_path, env, self.kind))

    def top_file(self, env="base"):
        return "%s/salt/%s/%s/top.sls" % (self.root_path, env, self.kind)


class PillarPathHelper(PathHelper):
    def __init__(self):
        super(PillarPathHelper, self).__init__()
        self.kind = "pillars"

class StatePathHelper(PathHelper):
    def __init__(self):
        super(StatePathHelper, self).__init__()
        self.kind = "states"

class OrchPathHelper(PathHelper):
    def __init__(self):
        super(OrchPathHelper, self).__init__()
        self.kind = "orch"

class ReactorPathHelper(PathHelper):
    def __init__(self):
        super(ReactorPathHelper, self).__init__()
        self.kind = "reactors"

class ExtPathHelper(PathHelper):
    def __init__(self):
        super(ExtPathHelper, self).__init__()
        self.kind = "*"
