import os.path
import subprocess
from typing import List

from app.command.interface import ICommand
from app.input_checker import to_script_path
from app.shell_api import ShellAPI


class ExecuteCommand(ICommand):
    _script: str

    def __init__(self, cmd: List[str]):
        if len(cmd) != 1:
            raise ValueError()
        script_path = to_script_path(cmd[0])
        if not os.path.exists(script_path):
            raise ValueError()
        self._script = script_path

    def run(self, api: ShellAPI):
        subprocess.run(['python', self._script] + api.get_system_env())

