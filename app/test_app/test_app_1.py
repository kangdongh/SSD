from app.basic_logic import BasicLogic
from app.test_app.test_app_interface import ITestApp


class TestApp1(ITestApp):
    def run(self, basic_logic: BasicLogic):
        pass
