from typing import List

from app.command.interface import ICommand
from app.return_code import ReturnCode
from app.shell_api import ShellAPI


class ExitCommand(ICommand):

    def __init__(self, cmd: List[str]):
        if len(cmd) != 0:
            raise ValueError()

    def run(self, api: ShellAPI):
        return ReturnCode.EXIT

    @classmethod
    def description(cls):
        return "Exit program / usage: exit"
