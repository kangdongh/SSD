from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2
from app.test_app.test_app_interface import ITestApp

COMMAND_LIST = ['READ', 'WRITE', 'EXIT', 'HELP', 'FULLREAD', 'FULLWRITE', 'TESTAPP1', 'TESTAPP2']
INVALID_CMD = "INVALID COMMAND"


class TestShell:
    _logic: BasicLogic
    _test_app1: ITestApp
    _test_app2: ITestApp

    def __init__(self, path):
        self._logic = BasicLogic(path)
        self._test_app1 = TestApp1()
        self._test_app2 = TestApp2()

    def _get_integer(self, value):
        try:
            return int(value)
        except ValueError:
            return -1

    def _get_hex(self, value):
        try:
            return int(value, 16)
        except ValueError:
            return -1

    def _is_valid_cmd_length(self, cmds):
        if len(cmds) == 0:
            return False
        if cmds[0] in ['EXIT', 'HELP', 'FULLREAD'] and len(cmds) != 1:
            return False
        if cmds[0] in ['READ', 'FULLWRITE'] and len(cmds) != 2:
            return False
        if cmds[0] in ['WRITE'] and len(cmds) != 3:
            return False
        return True

    def _is_valid_cmd(self, cmd):
        if cmd in COMMAND_LIST:
            return True
        return False

    def _is_valid_address(self, cmd):
        if cmd[0] not in ['WRITE', 'READ']:
            return True
        address = self._get_integer(cmd[1])
        if address < 0 or address > 99:
            return False
        return True

    def _is_valid_value(self, cmd):
        bytes = None
        if cmd[0] == 'WRITE':
            bytes = cmd[2]
        elif cmd[0] == 'FULLWRITE':
            bytes = cmd[1]
        else:
            return True
        if len(bytes) != 10:
            return False
        if bytes[:2] != '0X':
            return False
        return self._get_hex(bytes[2:]) > 0

    def is_valid_command(self, cmd):
        cmd = cmd.upper()
        cmd_split = cmd.split(" ")

        return self._is_valid_cmd_length(cmd_split) and \
            self._is_valid_cmd(cmd_split[0]) and \
            self._is_valid_address(cmd_split) and \
            self._is_valid_value(cmd_split)

    def run(self, line) -> bool:
        # Call _app.methods
        # return True for exit condition
        return True


if __name__ == '__main__':
    import os.path

    current_file_abspath = os.path.abspath(__file__)
    ssd_path = os.path.join(current_file_abspath, '../hardware/ssd.py')

    app = TestShell(ssd_path)

    while True:
        try:
            inp = input()
            inp = inp.lower()
            # validation
            if not app.is_valid_command(inp):
                print("INVALID COMMAND")
                continue

            exit_condition = app.run(inp)
            if exit_condition:
                break
        except Exception as e:
            print(str(e))
