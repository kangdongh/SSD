from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp1(ITestApp):
    FULL_WRITE_VALUE = '0x00000001'

    def run(self, basic_logic: BasicLogic):
        basic_logic.full_write(TestApp1.FULL_WRITE_VALUE)
        results = basic_logic.full_read().strip().split('\n')
        self._check_results_valid(results)
        print(f"{self.__class__.__name__} PASS")

    def _check_results_valid(self, results):
        for result in results:
            if result.lower() != TestApp1.FULL_WRITE_VALUE.lower():
                raise RuntimeError(f"{self.__class__.__name__} Failure")

    def help(self):
        return f"- {self.__class__.__name__}: Full-Write, Read Test / usage: testapp1"
