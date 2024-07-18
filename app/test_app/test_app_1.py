from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp
from logger import CommandLogger


class TestApp1(ITestApp):
    FULL_WRITE_VALUE = '0x00000001'

    def __init__(self, logger: CommandLogger = CommandLogger()):
        self._logger = logger

    def run(self, basic_logic: BasicLogic):
        logger = self._logger.get_logger('run', self.__class__.__name__, 'run')
        logger.info(f'TESTAPP1 received.')
        basic_logic.full_write(TestApp1.FULL_WRITE_VALUE)
        results = basic_logic.full_read().strip().split('\n')
        self._check_results_valid(results)

    def _check_results_valid(self, results):
        for result in results:
            if result.lower() != TestApp1.FULL_WRITE_VALUE.lower():
                raise RuntimeError(f"{self.__class__.__name__} Failure")

    def help(self):
        return f"- {self.__class__.__name__}: Full-Write, Read Test / usage: testapp1"
