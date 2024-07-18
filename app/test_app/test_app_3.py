from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp3(ITestApp):
    START_LBA = 0
    ERASE_SIZE = 10
    INIT_VALUE = '0x00000000'

    def run(self, basic_logic: BasicLogic):
        basic_logic.erase(TestApp3.START_LBA, TestApp3.ERASE_SIZE)

        results = []
        for lba in range(10):
            results.append(basic_logic.read(str(lba).strip()))
        self._check_results_valid(results)

    def _check_results_valid(self, results):
        for result in results:
            if result.lower() != TestApp3.INIT_VALUE.lower():
                raise RuntimeError(f"{self.__class__.__name__} Failure")

    def help(self):
        return f"- {self.__class__.__name__}: Erase LBA from 0 by size 10, Read Test to compare / usage: testapp3"