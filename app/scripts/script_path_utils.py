import os
from os.path import dirname, abspath

_script_dir_path = os.path.join(dirname(abspath(__file__)), "examples")


def is_script_name(name: str):
    return os.path.exists(script_name_to_path(name))


def script_name_to_path(name: str):
    return os.path.join(_script_dir_path, name + '.py')


def get_script_dir_path():
    return _script_dir_path


def set_script_dir_path(dir_path: str):
    if os.path.isdir(dir_path):
        global _script_dir_path
        _script_dir_path = dir_path
    raise ValueError()
