from abc import ABC, abstractmethod


class ISSDReader(ABC):
    @abstractmethod
    def read(self, logical_bytes_address: int) -> str:
        pass
