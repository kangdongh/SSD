import os
from typing import List

from hardware.ssd_interface import ISSD
from hardware.ssd_reader import SSDReader
from hardware.ssd_reader_interface import ISSDReader
from hardware.ssd_writer import SSDWriter
from hardware.ssd_writer_interface import ISSDWriter

CURRENT_FILE_PATH = os.path.abspath(__file__)
DATA_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'nand.txt')
RESULT_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'result.txt')
INITIAL_DATA_VALUE = '0x00000000'


class SSD(ISSD):
    _reader: ISSDReader
    _writer: ISSDWriter

    def __init__(
            self,
            ssd_reader: ISSDReader = SSDReader(),
            ssd_writer: ISSDWriter = SSDWriter(),
            data_file_dir: str = DATA_FILE_DIR,
            result_file_dir: str = RESULT_FILE_DIR
    ):
        self._ssd_reader = ssd_reader
        self._ssd_writer = ssd_writer
        self._data_file_dir = data_file_dir
        self._result_file_dir = result_file_dir
        self._max_block_size = 100
        self.initialize()

    def initialize(self):
        if not os.path.exists(self._data_file_dir):
            with open(self._data_file_dir, 'w') as data_file:
                for _ in range(self._max_block_size):
                    data_file.write(f'{INITIAL_DATA_VALUE}\n')

        if not os.path.exists(self._result_file_dir):
            with open(self._result_file_dir, 'w') as result_file:
                result_file.write('\n')

    def run(self, argv: List[str]):
        pass

if __name__ == '__main__':
    import sys

    ssd = SSD()
    ssd.run(sys.argv)
