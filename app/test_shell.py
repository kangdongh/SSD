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

    def __init__(self, basic_logic):
        self._logic = basic_logic
        self._test_app1 = None
        self._test_app2 = None

    def set_apps(self, test_app_1, test_app_2):
        self._test_app1 = test_app_1
        self._test_app2 = test_app_2
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

    def run(self, cmd, params=None) -> int:
        # Call _app.methods
        # return -1 for exit condition
        if cmd == 'EXIT':
            return -1
        if cmd == 'HELP':
            ret = self._logic.help()
        if cmd == 'WRITE':
            self._logic.write(params[0], params[1])
        if cmd == 'READ':
            self._logic.read(params[0])
        if cmd == 'FULLREAD':
            self._logic.full_read()
        if cmd == 'FULLWRITE':
            self._logic.full_write(params[0])
        if cmd == 'TESTAPP1':
            self._test_app1.run(self._logic)
        if cmd == 'TESTAPP2':
            self._test_app2.run(self._logic)
        return 0


if __name__ == '__main__':
    import os.path

    current_file_abspath = os.path.abspath(__file__)
    ssd_path = os.path.join(current_file_abspath, '../hardware/ssd.py')

    app = TestShell(BasicLogic(ssd_path))
    app.set_apps(TestApp1(), TestApp2())
    while True:
        try:
            inp = input()
            inp = inp.lower()
            # validation
            if not app.is_valid_command(inp):
                print("INVALID COMMAND")
                continue

            if app.run(inp) == -1:
                break
        except Exception as e:
            print(str(e))
