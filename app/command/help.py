from app.command.interface import ICommand
from app.shell_api import ShellAPI


class HelpCommand(ICommand):
    def __init__(self, *args):
        pass

    def run(self, api: ShellAPI):
        pass

    @classmethod
    def description(cls):
        return "Help command"
