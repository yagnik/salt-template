import os
import re
import hashlib
import yaml


class TestFile(object):
    ROOT = os.path.abspath("%s/../../" % os.path.dirname(os.path.realpath(__file__)))

    def test_all_files_are_snake_case(self):
        for subdir, dirs, files in os.walk(self.ROOT):
            for file in filter(lambda file: file.endswith(".py") or file.endswith(".sls"), files):
                assert file.islower(), "%s/%s name needs to be lower case" % (subdir, file)
                assert re.compile('^[a-z0-9_\.]+$').match(file) is not None, "%s/%s needs to be snake case" % (subdir, file)

    def test_all_pillars_have_root_key_same_as_file_name(self, __envs__):
        pillar_root = "%s/salt/pillars" % self.ROOT
        for env in __envs__:
            pillar_env_path = "%s/%s" % (pillar_root, env)
            for subdir, dirs, files in os.walk(pillar_env_path):
                for file in filter(lambda file: file.endswith(".sls"), files):
                    folder = os.path.basename(subdir.split(pillar_env_path)[-1])
                    path = "%s/%s" % (subdir, file)
                    if folder is not '':
                        key = folder
                        assert SyntaxChecker(file=path, key=key).check(), "Top level pillar is not same as base name for %s" % path
                    else:
                        key = os.path.basename(file).split('.')[0]
                        assert SyntaxChecker(file=path, key=key).check(), "Top level pillar is not same as base name for %s" % path

    def test_common_pillars_in_base_env(self):
        pillar_root = "%s/salt/pillars" % self.ROOT
        md5_hash = {}
        for subdir, dirs, files in os.walk(pillar_root):
            for file in files:
                path = "%s/%s" % (subdir, file)
                md5 = hashlib.md5(open(path, 'rb').read()).hexdigest()
                if md5 in md5_hash.keys():
                    assert False, "%s file and %s file is exactly the same, move them to base env" % (path, md5_hash[md5])
                else:
                    md5_hash[md5] = path

    def test_top_files_has_all_pillars(self, __envs__):
        pillar_root = "%s/salt/pillars" % self.ROOT
        top_file = "%s/top.sls" % pillar_root
        yml = yaml.load(open(top_file, 'r'))
        assert yml.keys().sort() == __envs__.sort(), "Environment mismatch!"

        for env, target_dict in yml.iteritems():
            pillars = map(lambda file: os.path.basename(file).split('.')[0], os.listdir("%s/%s" % (pillar_root, env)))
            for target, target_pillars in target_dict.iteritems():
                assert set(target_pillars).intersection(set(pillars)) == set(pillars), "%s not listed in top file" % (set(pillars).difference(set(target_pillars)))
                assert set(pillars).intersection(set(target_pillars)) == set(target_pillars), "%s not listed in pillar directory" % (set(target_pillars).difference(set(pillars)))

    def test_ensure_state_files_are_symlinked_if_similar(self, __envs__):
        production_env = 'prd'
        state_path = "%s/salt/states" % self.ROOT
        production_env_path = "%s/%s" % (state_path, production_env)
        for env in filter(lambda env: env != production_env, __envs__):
            env_path = "%s/%s" % (state_path, env)
            if os.path.exists(env_path):
                for state in os.listdir(env_path):
                    state_full_path = "%s/%s" % (env_path, state)
                    state_prd_full_path = "%s/%s" % (production_env_path, state)
                    if not os.path.islink(state_full_path):
                        assert Hasher(state_full_path).hash() != Hasher(state_prd_full_path).hash(), "prd and another environment state file collision, make it a symlink!"

    def test_ensure_state_has_core_files(self, __envs__):
        state_path = "%s/salt/states" % self.ROOT
        core_files = ('init.sls', 'verify.sls', 'map.jinja', 'defaults.yaml')
        for env in __envs__:
            env_path = "%s/%s" % (state_path, env)
            if os.path.exists(env_path):
                for state in os.listdir(env_path):
                    for version in os.listdir(os.path.join(env_path, state)):
                        if version != "latest.sls":
                            files = os.listdir(os.path.join(env_path, state, version))
                            assert set(core_files).intersection(set(files)) == set(core_files)

    def test_ensure_external_module_has_test_file(self):
        external_module_path = "%s/salt/ext" % self.ROOT
        test_path = "%s/tests/unit" % self.ROOT
        for subdir, dirs, files in os.walk(external_module_path):
            for file in filter(lambda file: file.endswith(".py") and file != "__init__.py", files):
                ext_module_file_path = "%s/test_%s" % (subdir, file)
                test_module_file_path = ext_module_file_path.replace(external_module_path, test_path)
                assert os.path.exists(test_module_file_path), "%s file is missing" % test_module_file_path


class Hasher(object):
    def __init__(self, path):
        self.path = path

    def hash(self):
        hasher = hashlib.md5()
        for subdir, dirs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(subdir, file)
                with open(str(file_path), 'rb') as afile:
                    hasher.update(afile.read())
        return hasher.hexdigest()


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
