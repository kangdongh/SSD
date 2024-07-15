from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp2(ITestApp):
    DUPL_WRITE_COUNT = 30
    FIRST_WRITE_VALUE = '0xAAAABBBB'
    OVERWRITE_VALUE = '0x12345678'

    def run(self, basic_logic: BasicLogic):
        pass
