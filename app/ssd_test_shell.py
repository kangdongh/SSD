from app.basic_logic import BasicLogic
from app.system_call_handler import SystemCallHandler
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2


class CommandValidator:
    COMMAND_LIST = ['READ', 'WRITE', 'EXIT', 'HELP', 'FULLREAD', 'FULLWRITE']
    TESTAPP_LIST = ['TESTAPP1', 'TESTAPP2']

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

    def is_valid_command(self, cmd):
        cmd_split = cmd.split(" ")
        cmd_split[0] = cmd_split[0].upper()
        return (self._is_valid_cmd_length(cmd_split) and
                self._is_valid_cmd(cmd_split[0]) and
                self._is_valid_address(cmd_split) and
                self._is_valid_value(cmd_split))

    def _is_valid_cmd_length(self, cmds):
        if len(cmds) == 0:
            return False
        if cmds[0] in ['EXIT', 'HELP', 'FULLREAD'] + self.TESTAPP_LIST and len(cmds) != 1:
            return False
        if cmds[0] in ['READ', 'FULLWRITE'] and len(cmds) != 2:
            return False
        if cmds[0] in ['WRITE'] and len(cmds) != 3:
            return False
        return True

    def _is_valid_cmd(self, cmd):
        return cmd in self.COMMAND_LIST or cmd in self.TESTAPP_LIST

    def _is_valid_address(self, cmd):
        if cmd[0] not in ['WRITE', 'READ']:
            return True
        address = self._get_integer(cmd[1])
        return 0 <= address <= 99

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
        if bytes[:2] != '0x':
            return False
        return self._get_hex(bytes[2:]) >= 0


class SSDTestShell:
    INVALID_CMD = "INVALID COMMAND"

    def __init__(self, basic_logic: BasicLogic, validator: CommandValidator, test_app1=None, test_app2=None):
        self._logic = basic_logic
        self._validator = validator
        self._test_app1 = test_app1
        self._test_app2 = test_app2
        self._cmd = None
        self._params = None

    def set_apps(self, test_app_1, test_app_2):
        self._test_app1 = test_app_1
        self._test_app2 = test_app_2

    def _set_command(self, cmd_split):
        self._cmd = cmd_split[0].upper()
        self._params = cmd_split[1:] if len(cmd_split) > 1 else None

    def run(self, cmd) -> int:
        self._set_command(cmd.split(" "))
        if self._cmd == 'EXIT':
            return -1
        if self._cmd == 'HELP':
            print(self._logic.help())
        elif self._cmd == 'WRITE':
            self._logic.write(self._params[0], self._params[1])
        elif self._cmd == 'READ':
            print(self._logic.read(self._params[0]))
        elif self._cmd == 'FULLREAD':
            print(self._logic.full_read())
        elif self._cmd == 'FULLWRITE':
            self._logic.full_write(self._params[0])
        elif self._cmd == 'TESTAPP1':
            self._test_app1.run(self._logic)
        elif self._cmd == 'TESTAPP2':
            self._test_app2.run(self._logic)
        return 0

    def start_progress(self):
        while True:
            try:
                inp = input()
                if not self._validator.is_valid_command(inp):
                    print(self.INVALID_CMD)
                    continue
                if self.run(inp) == -1:
                    break
            except Exception as e:
                print(str(e))


def main():
    import os.path
    current_dir_abspath = os.path.dirname(os.path.abspath(__file__))
    ssd_path = os.path.join(current_dir_abspath, '../hardware/ssd.py')
    result_file_path = os.path.join(current_dir_abspath, '../hardware/result.txt')
    system_call_handler = SystemCallHandler(ssd_path, result_file_path)

    basic_logic = BasicLogic(system_call_handler)
    validator = CommandValidator()
    shell = SSDTestShell(basic_logic, validator)

    test_app1 = TestApp1()
    test_app2 = TestApp2()
    shell.set_apps(test_app1, test_app2)

    shell.start_progress()


if __name__ == '__main__':
    main()
