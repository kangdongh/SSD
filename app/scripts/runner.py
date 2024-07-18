import os.path
from typing import List

from app.scripts.script_path_utils import script_name_to_path
from app.shell_api import ShellAPI
from app.subprocess_wrapper import subprocess_run_ignore_stdout


class ScriptsRunner:
    _scripts: List[str]

    def __init__(self, scripts: List[str]):
        self._scripts = scripts

    def run(self, api: ShellAPI):
        for script in self._scripts:
            print(f"Run {script} ... ", end=' ', flush=True)
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
