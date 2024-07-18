import os
from os.path import dirname, abspath
from typing import Callable, List

from app.shell_api import ShellAPI
from app.system_call_handler import SystemCallHandler
from customlogger.logger import CommandLogger

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


def run_script(func: Callable[[ShellAPI], None], argv: List[str]):
    logger = CommandLogger().get_logger()
    system_call_handler = None
    if len(argv) == 3:
        logger.info("Initialize system call with given args")
        system_call_handler = SystemCallHandler(argv[1], argv[2])
    try:
        func(ShellAPI(system_call_handler))
    except Exception as e:
        logger.error(f"FAIL :{e}")
        return -1
    logger.info("PASS")
    return 0
