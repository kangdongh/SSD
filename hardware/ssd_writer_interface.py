from abc import ABC, abstractmethod


class ISSDWriter(ABC):
    @abstractmethod
    def write(self, logical_bytes_address: int):
        pass
