from abc import ABC, abstractmethod

from app.basic_logic import BasicLogic


class ITestApp(ABC):
    @abstractmethod
    def run(self, basic_logic: BasicLogic):
        pass