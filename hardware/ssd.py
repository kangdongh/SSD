import os, sys
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hardware.ssd_interface import ISSD
from hardware.ssd_reader import SSDReader
from hardware.ssd_writer import SSDWriter

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'nand.txt')
RESULT_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'result.txt')


class SSD(ISSD):
    CMD_READ_LENGTH = 3
    CMD_WRITE_LENGTH = 4
    CMD_READ_TYPE = 'R'
    CMD_WRITE_TYPE = 'W'
    INITIAL_DATA_VALUE = '0x00000000'
    DATA_LENGTH = 10

    MAX_DATA_LEN = 100
    MAX_RESULT_LEN = 1

    def __init__(
            self,
            data_file_dir: str = DATA_FILE_DIR,
            result_file_dir: str = RESULT_FILE_DIR
    ):
        self._data_file_dir = data_file_dir
        self._data_reader = SSDReader(data_file_dir)
        self._data_writer = SSDWriter(data_file_dir, max_lba=100)

        self._result_file_dir = result_file_dir
        self._result_writer = SSDWriter(result_file_dir, max_lba=1)

        self.initialize()

    def initialize(self):
        if not os.path.exists(self._data_file_dir):
            with open(self._data_file_dir, 'w') as data_file:
                for _ in range(SSD.MAX_DATA_LEN):
                    data_file.write(f'{SSD.INITIAL_DATA_VALUE}\n')

        if not os.path.exists(self._result_file_dir):
            with open(self._result_file_dir, 'w') as result_file:
                result_file.write('\n')

    def run(self, argv: List[str]):
        if not self._is_valid_cmd(argv):
            raise Exception('INVALID COMMAND')
        cmd_type = argv[1]
        lba = int(argv[2])
        if cmd_type == SSD.CMD_READ_TYPE:
            self._read(lba)
        elif cmd_type == SSD.CMD_WRITE_TYPE:
            data = argv[3]
            self._write(lba, data)

    def _read(self, address):
        read_value = self._data_reader.read(address)
        self._result_writer.write(0, 1, read_value)

    def _write(self, address, data):
        return self._data_writer.write(address, 1, data)

    def _is_valid_cmd(self, argv: List[str]):
        if not self._check_cmd_syntax(argv):
            return False
        if not self._check_cmd_semantic(argv):
            return False
        return True

    def _check_cmd_syntax(self, argv: List[str]):
        # syntax check
        if len(argv) < SSD.CMD_READ_LENGTH:
            return False
        cmd_type = argv[1]
        lba = argv[2]

        if not lba.isdigit():
            return False

        if not (cmd_type == SSD.CMD_READ_TYPE or cmd_type == SSD.CMD_WRITE_TYPE):
            return False
        elif cmd_type == SSD.CMD_READ_TYPE and len(argv) != SSD.CMD_READ_LENGTH:
            return False
        elif cmd_type == SSD.CMD_WRITE_TYPE and len(argv) != SSD.CMD_WRITE_LENGTH:
            return False

        return True

    def _check_cmd_semantic(self, argv: List[str]):
        cmd_type = argv[1]
        lba = argv[2]
        if int(lba) >= SSD.MAX_DATA_LEN:
            return False
        if cmd_type == SSD.CMD_WRITE_TYPE:
            data = argv[3]
            if not self._is_valid_data(data):
                return False
        return True

    def _is_valid_data(self, data):
        if len(data) != SSD.DATA_LENGTH:
            return False

        if not data.startswith('0x'):
            return False

        hex_digits = set('0123456789abcdefABCDEF')
        for char in data[2:]:
            if char not in hex_digits:
                return False
        return True


def main():
    import sys

    try:
        ssd = SSD()
        ssd.run(sys.argv)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
