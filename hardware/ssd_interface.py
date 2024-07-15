from abc import ABC, abstractmethod
from typing import List


class ISSD(ABC):

    @abstractmethod
    def initialize(self):
        # if required data is not detected, create data
        pass

    @abstractmethod
    def run(self, argv: List[str]):
        pass
