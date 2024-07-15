from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp2(ITestApp):
    def run(self, basic_logic: BasicLogic):
        for i in range(5):
            for j in range(30):
                basic_logic.write(i, '0xAAAABBBB')
        for i in range(5):
            basic_logic.write(i, '0x12345678')

        for i in range(5):
            if basic_logic.read(i) != '0x12345678':
                return False
        return True

