from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp2(ITestApp):
    PREDEFINED_LBA_HEAD = 0
    PREDEFINED_LBA_TAIL = 5
    DUPL_WRITE_COUNT = 30
    FIRST_WRITE_VALUE = '0xAAAABBBB'
    OVERWRITE_VALUE = '0x12345678'

    def run(self, basic_logic: BasicLogic):
        for j in range(TestApp2.DUPL_WRITE_COUNT):
            self._write_values_for_predefined_lba_range(basic_logic, TestApp2.FIRST_WRITE_VALUE)

        self._write_values_for_predefined_lba_range(basic_logic, TestApp2.OVERWRITE_VALUE)
        self._check_data_overwritten_for_predefined_lba_range(basic_logic)

        print(f"{self.__class__.__name__} PASS")

    def _check_data_overwritten_for_predefined_lba_range(self, basic_logic):
        for i in self._predefined_range():
            read = basic_logic.read(str(i))
            if read != TestApp2.OVERWRITE_VALUE:
                print(f"{self.__class__.__name__} Failure, read {read} vs Expected {TestApp2.OVERWRITE_VALUE}")
                raise RuntimeError()

    def _write_values_for_predefined_lba_range(self, basic_logic, write_value):
        for i in self._predefined_range():
            basic_logic.write(str(i), write_value)

    def _predefined_range(self):
        return range(TestApp2.PREDEFINED_LBA_HEAD, TestApp2.PREDEFINED_LBA_TAIL + 1)
