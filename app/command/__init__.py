import os
import textwrap
from typing import List

from app.command.erase import EraseCommand
from app.command.erase_range import EraseRangeCommand
from app.command.execute import ExecuteCommand
from app.command.exit import ExitCommand
from app.command.flush import FlushCommand
from app.command.full_read import FullReadCommand
from app.command.full_write import FullWriteCommand
from app.command.help import HelpCommand
from app.command.interface import ICommand
from app.command.read import ReadCommand
from app.command.read import ReadCommand
from app.command.write import WriteCommand
from app.command.write import WriteCommand

__COMMAND_DICT__ = {
    'EXIT': ExitCommand,
    'HELP': HelpCommand,
    'WRITE': WriteCommand,
    'READ': ReadCommand,
    'FULLREAD': FullReadCommand,
    'FULLWRITE': FullWriteCommand,
    'ERASE': EraseCommand,
    'ERASE_RANGE': EraseRangeCommand,
    'FLUSH': FlushCommand,
}

from app.scripts.script_path_utils import is_script_name, get_script_dir_path


def command_factory(cmd: List[str]) -> ICommand:
    if len(cmd) < 1:
        raise ValueError()
    command_type = cmd[0].upper()
    if command_type == 'HELP':
        print_help()
    if command_type in __COMMAND_DICT__:
        cls = __COMMAND_DICT__[command_type]
        return cls(cmd[1:])
    if is_script_name(cmd[0]):
        return ExecuteCommand(cmd)
    raise ValueError()


HELP_PREFIX = textwrap.dedent("""
********************* COMMAND HELP ***********************
""").strip()

HELP_POSTFIX = textwrap.dedent("""
*********************************************************
""").strip()


def print_help():
    print(HELP_PREFIX)
    for name, command in __COMMAND_DICT__.items():
        desc = command.description()
        print(f'- {name.lower()}: {desc}')
    script_dir = get_script_dir_path()
    script_list = []
    for script in os.listdir(script_dir):
        if '.py' in script:
            script_list.append(script.split('.')[0])
    if len(script_list) > 0:
        print("- Available Tests")
    for script_name in script_list:
        print(f"   * {script_name}")
    print(HELP_POSTFIX)
