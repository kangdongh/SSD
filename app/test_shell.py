from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2
from app.test_app.test_app_interface import ITestApp


class TestShell:
    _logic: BasicLogic
    _test_app1: ITestApp
    _test_app2: ITestApp

    def __init__(self, logic: BasicLogic, test_app1: ITestApp, test_app2: ITestApp):
        self._logic = logic
        self._test_app1 = test_app1
        self._test_app2 = test_app2

    def run(self, line) -> bool:
        # Call _app.methods
        # return True for exit condition
        return True


if __name__ == '__main__':
    import os.path

    current_file_abspath = os.path.abspath(__file__)
    ssd_path = os.path.join(current_file_abspath, '../hardware/ssd.py')
    basic_logic = BasicLogic(ssd_path)
    app = TestShell(basic_logic, TestApp1(), TestApp2())
    while True:
        inp = input()
        exit_condition = app.run(inp)
        if exit_condition:
            break
