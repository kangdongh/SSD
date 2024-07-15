from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2
from app.test_app.test_app_interface import ITestApp

COMMAND_LIST = ['read', 'write', 'exit', 'help', 'fullread', 'fullwrite', 'testapp1', 'testapp2']

class TestShell:
    _logic: BasicLogic
    _test_app1: ITestApp
    _test_app2: ITestApp

    def __init__(self, path):
        self._logic = BasicLogic(path)
        self._test_app1 = TestApp1()
        self._test_app2 = TestApp2()

    def _check_cmd(self):
        pass

    def _check_address(self):
        pass

    def _check_value(self):
        pass

    def is_valid_command(self, cmd):
        if cmd == 'read' or cmd == 'read 0' or cmd == 'write 3 0xAAAAAAAA':
            return 1
        if cmd == 'cmd1' or cmd == 'read 101' or cmd == 'write 3 0xAAAAAAAZ':
            return "INVALID COMMAND"

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
            # validation
            if not app.is_valid_command(inp):
                print("INVALID COMMAND")
                continue

            exit_condition = app.run(inp)
            if exit_condition:
                break
        except Exception as e:
            print(str(e))
