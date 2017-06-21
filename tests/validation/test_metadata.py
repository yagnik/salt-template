import os
import yaml

class TestFile(object):
    ROOT = os.path.abspath("%s/../../" % os.path.dirname(os.path.realpath(__file__)))
    METADATA_SCHEMA = [
      "name",
      "type",
      "version",
      "packages",
      "files",
      "services"
    ]

    def test_state_metadata(self):
        state_path = "%s/salt/states" % self.ROOT
        for subdir, dirs, files in os.walk(state_path):
            for file in filter(lambda file: file == "metadata.yaml", files):
                metadata = yaml.load(open(os.path.join(subdir, file), 'r'))
                for key in self.METADATA_SCHEMA:
                    assert key in metadata.keys(), "Unable to find %s in metadata" % key
