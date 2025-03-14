import os.path
from typing import List

from app.scripts.script_utils import script_name_to_path
from app.shell_api import ShellAPI
from app.subprocess_wrapper import subprocess_run_ignore_stdout
from customlogger.logger import CommandLogger


class ScriptsRunner:
    _scripts: List[str]

    def __init__(self, scripts: List[str]):
        self._scripts = scripts
        self._logger = CommandLogger().get_logger()

    def run(self, api: ShellAPI):
        for script in self._scripts:
            print(f"{script}  ---  Run...", end='', flush=True)
            script_path = script_name_to_path(script)
            if not os.path.exists(script_path):
                print("FAIL!")
                return
            result = subprocess_run_ignore_stdout(['python', script_path] + api.get_system_env())
            if result.returncode == 0:
                print("PASS")
            else:
                print("FAIL!")
                return
