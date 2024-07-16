from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp1(ITestApp):
    FULL_WRITE_VALUE = '0x00000001'

    def run(self, basic_logic: BasicLogic):
        pass
