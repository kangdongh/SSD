from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp1(ITestApp):
    def run(self, basic_logic: BasicLogic):
        basic_logic.full_write('0xABCDFFFF')
        result = basic_logic.full_read()
        if result == '0xABCDFFFF':
            return True
        return False