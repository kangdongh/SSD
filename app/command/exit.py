from typing import List

from app.command.interface import ICommand
from app.shell_api import ShellAPI


class ExitCommand(ICommand):

    def __init__(self, cmd: List[str]):
        if len(cmd) != 0:
            raise ValueError()

    def run(self, api: ShellAPI):
        exit(0)
