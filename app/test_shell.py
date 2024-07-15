from app.advanced_logic import AdvancedLogic
from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2
from app.test_app.test_app_interface import ITestApp


class TestShell:
    _logic: BasicLogic
    _test_app1: ITestApp
    _test_app2: ITestApp

    def __init__(self, logic: BasicLogic):
        self._logic = logic
        self.set_test_app1(TestApp1())
        self.set_test_app2(TestApp2())

    def set_test_app2(self, test_app_2):
        self._test_app2 = test_app_2

    def set_test_app1(self, test_app_1):
        self._test_app1 = test_app_1

    def run(self, line) -> bool:
        # Call _app.methods
        # return True for exit condition
        return True


if __name__ == '__main__':
    logic = AdvancedLogic()
    app = TestShell(logic)
    while True:
        inp = input()
        exit_condition = app.run(inp)
        if exit_condition:
            break
