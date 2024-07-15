from abc import ABC, abstractmethod


class ISSDReader(ABC):
    @abstractmethod
    def read(self, read_file_name, logical_bytes_address: int) -> str:
        pass
