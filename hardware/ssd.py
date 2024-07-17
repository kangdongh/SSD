import copy
import os, sys
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from hardware.ssd_interface import ISSD
from hardware.ssd_reader import SSDReader
from hardware.ssd_writer import SSDWriter

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'nand.txt')
RESULT_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'result.txt')
BUFFER_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'buffer.txt')


class SSD(ISSD):
    CMD_FLUSH_LENGTH = 2
    CMD_READ_LENGTH = 3
    CMD_WRITE_LENGTH = CMD_ERASE_LENGTH = 4

    CMD_READ_TYPE = 'R'
    CMD_WRITE_TYPE = 'W'
    CMD_ERASE_TYPE = 'E'
    CMD_FLUSH_TYPE = 'F'

    INITIAL_DATA_VALUE = '0x00000000'
    DATA_LENGTH = 10

    MAX_ERASE_SIZE = 10
    MAX_DATA_LEN = 100
    MAX_RESULT_LEN = 1
    MAX_BUFFER_LEN = 10

    def __init__(
            self,
            data_file_dir: str = DATA_FILE_DIR,
            result_file_dir: str = RESULT_FILE_DIR,
            buffer_file_dir: str = BUFFER_FILE_DIR
    ):
        self._data_file_dir = data_file_dir
        self._data_reader = SSDReader(data_file_dir)
        self._data_writer = SSDWriter(data_file_dir, max_lba=SSD.MAX_DATA_LEN)

        self._result_file_dir = result_file_dir
        self._result_writer = SSDWriter(result_file_dir, max_lba=SSD.MAX_RESULT_LEN)

        self._buffer_file_dir = buffer_file_dir
        self._buffer_reader = SSDReader(buffer_file_dir)
        self._buffer_writer = SSDWriter(buffer_file_dir, max_lba=SSD.MAX_BUFFER_LEN)
        self._buffer = []

        self._buffer_optimizer = BufferOptimizer()

        self._command_list = [SSD.CMD_READ_TYPE, SSD.CMD_WRITE_TYPE, SSD.CMD_ERASE_TYPE, SSD.CMD_FLUSH_TYPE]

        self.initialize()

    def __del__(self):
        self._save_buffer_file()

    def _save_buffer_file(self):
        buf_size = len(self._buffer)
        with open(self._buffer_file_dir, 'w') as buffer_file:
            for i in range(buf_size):
                for item in self._buffer[i]:
                    buffer_file.write(item + ' ')
                buffer_file.write('\n')
            for _ in range(SSD.MAX_BUFFER_LEN - buf_size):
                buffer_file.write('None\n')

    def _load_buffer_file(self):
        with open(self._buffer_file_dir, 'r') as buffer_file:
            lines = [line.strip() for line in buffer_file.readlines()]
            for line in lines:
                if line == 'None':
                    break
                self._buffer.append(line.split())

    def initialize(self):
        if not os.path.exists(self._data_file_dir):
            with open(self._data_file_dir, 'w') as data_file:
                for _ in range(SSD.MAX_DATA_LEN):
                    data_file.write(f'{SSD.INITIAL_DATA_VALUE}\n')

        if not os.path.exists(self._result_file_dir):
            with open(self._result_file_dir, 'w') as result_file:
                result_file.write('\n')

        if os.path.exists(self._buffer_file_dir):
            self._load_buffer_file()
        else:
            with open(self._buffer_file_dir, 'w') as buffer_file:
                for _ in range(SSD.MAX_DATA_LEN):
                    buffer_file.write('None\n')

    def run(self, argv: List[str]):
        if not self._is_valid_cmd(argv):
            raise Exception('INVALID COMMAND')
        cmd_type = argv[1]
        if cmd_type == SSD.CMD_READ_TYPE:
            lba = int(argv[2])
            self._read(lba)
        elif cmd_type == SSD.CMD_WRITE_TYPE or cmd_type == SSD.CMD_ERASE_TYPE:
            self._edit_file(argv[1:])
        elif cmd_type == SSD.CMD_FLUSH_TYPE:
            self._flush()
        else:
            raise Exception('INVALID COMMAND')

    def _edit_file(self, argv: List[str]):
        if len(self._buffer) == SSD.MAX_BUFFER_LEN:
            self._flush()
        self._buffer.append(argv)
        self._buffer = self._buffer_optimizer.optimize_command_buffer(self._buffer)

    def _flush(self):
        for command in self._buffer:
            command_type = command[0]
            address = int(command[1])
            if command_type == SSD.CMD_WRITE_TYPE:
                self._write(address, command[2])
            elif command_type == SSD.CMD_ERASE_TYPE:
                self._erase(address, int(command[2]))
        self._buffer.clear()

    def _read(self, address):
        buffer_result = self._search_buffer(address)
        if buffer_result[0]:
            read_value = buffer_result[1]
        else:
            read_value = self._data_reader.read(address)
        self._result_writer.write(0, 1, read_value)

    def _search_buffer(self, address):
        ret_val = [False, None]
        for command in self._buffer:
            command_type = command[0]
            command_addr = int(command[1])
            if command_type == SSD.CMD_WRITE_TYPE and command_addr == address:
                ret_val = [True, command[2]]
            elif command_type == SSD.CMD_ERASE_TYPE:
                end_addr = command_addr + int(command[2])
                if command_addr <= address < end_addr:
                    ret_val = [True, SSD.INITIAL_DATA_VALUE]
        return ret_val

    def _write(self, address, data):
        self._data_writer.write(address, 1, data)

    def _erase(self, address, size):
        self._data_writer.write(address, size, SSD.INITIAL_DATA_VALUE)

    def _is_valid_cmd(self, argv: List[str]):
        if not self._check_cmd_syntax(argv):
            return False
        if not self._check_cmd_semantic(argv):
            return False
        return True

    def _check_cmd_syntax(self, argv: List[str]):
        if len(argv) < SSD.CMD_FLUSH_LENGTH:
            return False
        cmd_type = argv[1]
        if cmd_type not in self._command_list:
            return False
        if cmd_type == SSD.CMD_FLUSH_TYPE and len(argv) != SSD.CMD_FLUSH_LENGTH:
            return False
        elif cmd_type == SSD.CMD_READ_TYPE and (len(argv) != SSD.CMD_READ_LENGTH or not argv[2].isdigit()):
            return False
        elif cmd_type == SSD.CMD_WRITE_TYPE and (len(argv) != SSD.CMD_WRITE_LENGTH or not argv[2].isdigit()):
            return False
        elif cmd_type == SSD.CMD_ERASE_TYPE and (
                len(argv) != SSD.CMD_ERASE_LENGTH or not argv[2].isdigit() or not argv[3].isdigit()):
            return False

        return True

    def _check_cmd_semantic(self, argv: List[str]):
        cmd_type = argv[1]
        if cmd_type == SSD.CMD_FLUSH_TYPE:
            return True
        lba = int(argv[2])
        if lba >= SSD.MAX_DATA_LEN:
            return False
        if cmd_type == SSD.CMD_WRITE_TYPE:
            data = argv[3]
            if not self._is_valid_data(data):
                return False
        if cmd_type == SSD.CMD_ERASE_TYPE:
            size = int(argv[3])
            if not self._is_erasable(lba, size):
                return False
        return True

    def _is_erasable(self, lba: int, size: int):
        if size <= SSD.MAX_ERASE_SIZE and (lba + size) <= SSD.MAX_DATA_LEN:
            return True
        return False

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


class BufferOptimizer:
    CMD_WRITE_TYPE = 'W'
    CMD_ERASE_TYPE = 'E'

    def optimize_command_buffer(self, buffer: List[List[str]]):
        size = len(buffer)
        optimized_buffer = copy.copy(buffer)
        for i in range(size - 1):
            cmd = optimized_buffer[size - 1 - i]
            if cmd is None:
                continue
            optimized_buffer = self._optimize_if_prev_command_useless(cmd, size - 1 - i, optimized_buffer)
        optimized_buffer = [e for e in optimized_buffer if e is not None]
        return optimized_buffer

    def _optimize_if_prev_command_useless(self, cur_cmd, cur_idx, current_buffer):
        new_buffer = copy.copy(current_buffer)
        if cur_cmd[0] == 'W':
            cur_addr = int(cur_cmd[1])
            for i in range(cur_idx):
                prev_cmd = current_buffer[i]
                if prev_cmd is None:
                    continue
                if prev_cmd[0] == 'W' and int(prev_cmd[1]) == cur_addr:
                    new_buffer[i] = None

        elif cur_cmd[0] == 'E':
            start_addr = int(cur_cmd[1])
            end_addr = start_addr + int(cur_cmd[2])
            for i in range(cur_idx):
                prev_cmd = current_buffer[i]
                if prev_cmd is None:
                    continue
                if prev_cmd[0] == 'W' and start_addr <= int(prev_cmd[1]) < end_addr:
                    new_buffer[i] = None
                elif prev_cmd[0] == 'E':
                    prev_start_addr = int(prev_cmd[1])
                    prev_end_addr = prev_start_addr + int(prev_cmd[2])
                    if start_addr <= prev_start_addr and prev_end_addr <= end_addr:
                        new_buffer[i] = None
        return new_buffer


def main():
    import sys

    try:
        ssd = SSD()
        ssd.run(sys.argv)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
