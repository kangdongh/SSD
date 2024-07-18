import os.path
from typing import List

from app.command.interface import ICommand
from app.scripts.script_path_utils import script_name_to_path
from app.shell_api import ShellAPI
from app.subprocess_wrapper import subprocess_run


class ExecuteCommand(ICommand):
    _script: str

    def __init__(self, cmd: List[str]):
        if len(cmd) != 1:
            raise ValueError()
        script_path = script_name_to_path(cmd[0])
        if not os.path.exists(script_path):
            raise ValueError()
        self._script = script_path

    def run(self, api: ShellAPI):
        subprocess_run(['python', self._script] + api.get_system_env())
