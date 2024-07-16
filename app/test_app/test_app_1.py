from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp1(ITestApp):
    FULL_WRITE_VALUE = '0x00000001'

    def run(self, basic_logic: BasicLogic):
        basic_logic.full_write(TestApp1.FULL_WRITE_VALUE)
        results = basic_logic.full_read().strip().split('\n')
        for result in results:
            if result.lower() != TestApp1.FULL_WRITE_VALUE.lower():
                raise RuntimeError(f"{self.__class__.__name__} Failure")
        print(f"{self.__class__.__name__} PASS")
