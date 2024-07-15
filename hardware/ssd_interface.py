from abc import ABC, abstractmethod
from typing import List

from hardware.ssd_reader_interface import ISSDReader
from hardware.ssd_writer_interface import ISSDWriter


class ISSD(ABC):
    _reader: ISSDReader
    _writer: ISSDWriter

    @abstractmethod
    def run(self, argv: List[str]):
        pass
