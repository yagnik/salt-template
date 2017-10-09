import os
import re
import hashlib
import yaml


class TestFile(object):

    def test_all_files_are_snake_case(self, path_helper):
        for subdir, dirs, files in os.walk(path_helper.root_path()):
            for file in filter(lambda file: file.endswith(".py") or file.endswith(".sls"), files):
                assert file.islower(), "%s/%s name needs to be lower case" % (subdir, file)
                assert re.compile('^[a-z0-9_\.]+$').match(file) is not None, "%s/%s needs to be snake case" % (subdir, file)

    def test_all_pillars_have_root_key_same_as_file_name(self, path_helper):
        for pillar_env_path in path_helper.pillar().paths_with_env():
            for subdir, dirs, files in os.walk(pillar_env_path):
                for file in filter(lambda file: file.endswith(".sls") and file != "top.sls", files):
                    folder = os.path.basename(subdir.split(pillar_env_path)[-1])
                    path = "%s/%s" % (subdir, file)
                    if folder is not '':
                        key = folder
                        assert SyntaxChecker(file=path, key=key).check(), "Top level pillar is not same as base name for %s" % path
                    else:
                        key = os.path.basename(file).split('.')[0]
                        assert SyntaxChecker(file=path, key=key).check(), "Top level pillar is not same as base name for %s" % path

    def test_common_pillars_in_multiple_env(self, path_helper):
        md5_hash = {}
        for pillar_env_path in path_helper.pillar().paths_with_env():
            for subdir, dirs, files in os.walk(pillar_env_path):
                for file in files:
                    path = "%s/%s" % (subdir, file)
                    md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
                    if md5 in md5_hash.keys():
                        assert False, "%s file and %s file is exactly the same, move them to higher env" % (path, md5_hash[md5])
                    else:
                        md5_hash[md5] = path

    def test_top_files_has_all_pillars(self, __envs__, path_helper):
        yml = yaml.load(open(path_helper.pillar().top_file(), 'r'))
        assert yml.keys().sort() == __envs__.sort(), "Environment mismatch!"

        for env, target_dict in yml.iteritems():
            pillars = path_helper.pillar().names(env=env)
            for target, target_pillars in target_dict.iteritems():
                assert set(target_pillars).intersection(set(pillars)) == set(pillars), "%s not listed in top file in env %s" % (set(pillars).difference(set(target_pillars)), env)
                assert set(pillars).intersection(set(target_pillars)) == set(target_pillars), "%s not listed in pillar directory in env %s" % (set(target_pillars).difference(set(pillars)), env)

    def test_common_states_in_multiple_env(self, path_helper):
            md5_hash = {}
            for state_env_path in path_helper.state().paths_with_env():
                for subdir, dirs, files in os.walk(state_env_path):
                    for file in files:
                        path = "%s/%s" % (subdir, file)
                        md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
                        if md5 in md5_hash.keys():
                            assert False, "%s file and %s file is exactly the same, move them to higher env" % (path, md5_hash[md5])
                        else:
                            md5_hash[md5] = path

    # # def test_ensure_state_has_core_files(self, __envs__, path_helper):
    # #     core_files = ('init.sls', 'verify.sls', 'map.jinja', 'defaults.yaml', 'metadata.yaml', 'README.md', 'requisite.sls')
    # #     for state in path_helper.states():
    # #         for state in os.listdir(state_path):
    # #             for version in os.listdir(os.path.join(env_path, state)):
    # #                 if version != "latest.sls":
    # #                     files = os.listdir(os.path.join(env_path, state, version))
    # #                     assert set(core_files).intersection(set(files)) == set(core_files)

    # def test_ensure_external_module_has_test_file(self, path_helper):
    #     for ext_type_path in path_helper.ext().paths_with_env(env="ext"):
    #         for subdir, dirs, files in os.walk(ext_type_path):
    #             for file in filter(lambda file: file.endswith(".py") and file != "__init__.py", files):
    #                 ext_module_file_path = "%s/test_%s" % (subdir, file)
    #                 test_module_file_path = ext_module_file_path.replace(path_helper.ext_path(), path_helper.test_path())
    #                 assert os.path.exists(test_module_file_path), "%s file is missing" % test_module_file_path


class SyntaxChecker(object):
    def __init__(self, file, key):
        self.file = file
        self.key = key

    def check(self):
        with open(self.file, "r") as file:
            lines = file.readlines()
            lines = filter(lambda line: self.is_top_level(line), lines)
            lines = filter(lambda line: not self.is_jinja(line), lines)
            lines = filter(lambda line: not self.is_include(line), lines)
            if len(lines) == 1 and self.top_level_key(lines[0]):
                return True
            elif len(lines) == 0:
                return True
            else:
                return False

    def is_include(self, line):
        return line.startswith('include:')

    def is_jinja(self, line):
        return line.startswith('{{') or line.startswith('{%')

    def is_top_level(self, line):
        return not line.startswith(' ')

    def top_level_key(self, line):
        return line.startswith("%s:" % self.key)
