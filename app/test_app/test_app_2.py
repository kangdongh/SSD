from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp2(ITestApp):
    DUPL_WRITE_COUNT = 30
    FIRST_WRITE_VALUE = '0xAAAABBBB'
    OVERWRITE_VALUE = '0x12345678'

    def run(self, basic_logic: BasicLogic):
        for j in range(TestApp2.DUPL_WRITE_COUNT):
            for i in range(0, 6):
                basic_logic.write(str(i), TestApp2.FIRST_WRITE_VALUE)

        for i in range(0, 6):
            basic_logic.write(str(i), TestApp2.OVERWRITE_VALUE)

        for i in range(0, 6):
            read = basic_logic.read(str(i))
            print(read)
            if read != TestApp2.OVERWRITE_VALUE:
                print(f"{self.__class__.__name__} Failure, read {read} vs Expected {TestApp2.OVERWRITE_VALUE}")
                raise RuntimeError()

        print(f"{self.__class__.__name__} PASS")
