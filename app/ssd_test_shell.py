import os
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from customlogger.logger import CommandLogger
from app.return_code import ReturnCode
from app.command import command_factory
from app.scripts.runner import ScriptsRunner
from app.shell_api import ShellAPI

from typing import List


class SSDTestShell:
    INVALID_CMD = "INVALID COMMAND"

    def __init__(self, api: ShellAPI):
        self.api = api
        self._logger = CommandLogger().get_logger()

    def run(self, shell_cmd: str) -> ReturnCode:
        shell_cmd = shell_cmd.strip()
        if len(shell_cmd) == 0:
            return ReturnCode.FAILURE
        shell_cmd = shell_cmd.split(' ')
        try:
            command = command_factory(shell_cmd)
        except ValueError as e:
            self._logger.error(e)
            return ReturnCode.FAILURE
        self._logger.debug(f"Created: {command}")
        self._logger.debug(f"Execute safe_run of {command.__class__.__name__}")
        return command.safe_run(self.api)

    def start_progress(self):
        while True:
            try:
                inp = input()
            except Exception as e:
                self._logger.error(f"Error {e} occurs while processing stdin. Exit")
                break
            self._logger.debug(f"Process input: {inp}")
            return_code = self.run(inp)
            if return_code == return_code.FAILURE:
                print(self.INVALID_CMD)
            if return_code == return_code.EXIT:
                break

    def start_runner(self, runner_file_path):
        runner_file_path = os.path.abspath(runner_file_path)
        with open(runner_file_path, 'r') as file:
            scripts = [line.strip() for line in file.readlines()]
            runner = ScriptsRunner(scripts)
            runner.run(self.api)


def main(sys_argv: List[str]):
    shell_api = ShellAPI()
    shell = SSDTestShell(shell_api)
    if len(sys_argv) > 1:
        shell.start_runner(sys_argv[1])
    else:
        shell.start_progress()


if __name__ == '__main__':
    main(sys.argv)
