import os.path
from os.path import abspath, dirname
from typing import List

from app.input_checker import to_script_path
from app.shell_api import ShellAPI
from app.subprocess_wrapper import subprocess_run_ignore_stdout

SCRIPT_DIR_PATH = os.path.join(dirname(dirname(abspath(__file__))), "scripts")


class ScriptsRunner:
    _scripts: List[str]

    def __init__(self, scripts: List[str]):
        self._scripts = scripts

    def run(self, api: ShellAPI):
        for script in self._scripts:
            print(f"Run {script} ... ", end=' ', flush=True)
            script_path = to_script_path(script)
            if not os.path.exists(script_path):
                print("FAIL!")
                return
            result = subprocess_run_ignore_stdout(['python', script_path] + api.get_system_env())
            if result.returncode == 0:
                print("PASS")
            else:
                print("FAIL!")
                return


if __name__ == '__main__':
    if os.path.exists(SCRIPT_DIR_PATH):
        print(f"Exists: {SCRIPT_DIR_PATH}")
