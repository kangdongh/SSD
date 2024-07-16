from abc import ABC, abstractmethod


class ISSDWriter(ABC):
    @abstractmethod
    def write(self, write_file_name: str, logical_bytes_address: int, data_to_write: str, max_lba: int = 100):
        pass
