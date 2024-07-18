import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.command import command_factory
from app.scripts_runner import ScriptsRunner
from app.shell_api import ShellAPI

import textwrap
from typing import List

HELP_PREFIX = textwrap.dedent("""
**********************************************************
********************* COMMAND HELP ***********************
**********************************************************
""").strip()

HELP_POSTFIX = textwrap.dedent("""
*********************************************************
""").strip()


class SSDTestShellNew:
    INVALID_CMD = "INVALID COMMAND"

    def __init__(self, api: ShellAPI):
        self.api = api

    def run(self, shell_cmd: str) -> int:
        shell_cmd = shell_cmd.strip()
        if len(shell_cmd) == 0:
            return -1
        shell_cmd = shell_cmd.split(' ')
        try:
            command = command_factory(shell_cmd)
            command.run(self.api)
        except ValueError as e:
            return -1
        return 0

    def start_progress(self):
        while True:
            inp = input()
            if self.run(inp) == -1:
                print(self.INVALID_CMD)

    def start_runner(self, runner_file_path):
        runner_file_path = os.path.abspath(runner_file_path)
        with open(runner_file_path, 'r') as file:
            scripts = [l.strip() for l in file.readlines()]
            runner = ScriptsRunner(scripts)
            runner.run(self.api)


def main(sys_argv: List[str]):
    shell_api = ShellAPI()
    shell = SSDTestShellNew(shell_api)
    if len(sys_argv) > 1:
        shell.start_runner(sys_argv[1])
    else:
        shell.start_progress()


if __name__ == '__main__':
    main(sys.argv)
