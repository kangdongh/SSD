from abc import ABC, abstractmethod


class ISSDWriter(ABC):
    @abstractmethod
    def write(self, logical_bytes_address: int, length_to_write: int, data_to_write: str):
        pass
