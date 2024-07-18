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

CMD_READ_TYPE = 'R'
CMD_WRITE_TYPE = 'W'
CMD_ERASE_TYPE = 'E'
CMD_FLUSH_TYPE = 'F'

MAX_ERASE_SIZE = 10


class SSD(ISSD):
    CMD_FLUSH_LENGTH = 2
    CMD_READ_LENGTH = 3
    CMD_WRITE_LENGTH = CMD_ERASE_LENGTH = 4

    INITIAL_DATA_VALUE = '0x00000000'
    DATA_LENGTH = 10

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

        self._command_list = [CMD_READ_TYPE, CMD_WRITE_TYPE, CMD_ERASE_TYPE, CMD_FLUSH_TYPE]

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
        if cmd_type == CMD_READ_TYPE:
            lba = int(argv[2])
            self._read(lba)
        elif cmd_type == CMD_WRITE_TYPE or cmd_type == CMD_ERASE_TYPE:
            self._edit_file(argv[1:])
        elif cmd_type == CMD_FLUSH_TYPE:
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
            if command_type == CMD_WRITE_TYPE:
                self._write(address, command[2])
            elif command_type == CMD_ERASE_TYPE:
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
            if command_type == CMD_WRITE_TYPE and command_addr == address:
                ret_val = [True, command[2]]
            elif command_type == CMD_ERASE_TYPE:
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
        if cmd_type == CMD_FLUSH_TYPE and len(argv) != SSD.CMD_FLUSH_LENGTH:
            return False
        elif cmd_type == CMD_READ_TYPE and (len(argv) != SSD.CMD_READ_LENGTH or not argv[2].isdigit()):
            return False
        elif cmd_type == CMD_WRITE_TYPE and (len(argv) != SSD.CMD_WRITE_LENGTH or not argv[2].isdigit()):
            return False
        elif cmd_type == CMD_ERASE_TYPE and (
                len(argv) != SSD.CMD_ERASE_LENGTH or not argv[2].isdigit() or not argv[3].isdigit()):
            return False

        return True

    def _check_cmd_semantic(self, argv: List[str]):
        cmd_type = argv[1]
        if cmd_type == CMD_FLUSH_TYPE:
            return True
        lba = int(argv[2])
        if lba >= SSD.MAX_DATA_LEN:
            return False
        if cmd_type == CMD_WRITE_TYPE:
            data = argv[3]
            if not self._is_valid_data(data):
                return False
        if cmd_type == CMD_ERASE_TYPE:
            size = int(argv[3])
            if not self._is_erasable(lba, size):
                return False
        return True

    def _is_erasable(self, lba: int, size: int):
        if size <= MAX_ERASE_SIZE and (lba + size) <= SSD.MAX_DATA_LEN:
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
    def optimize_command_buffer(self, buffer: List[List[str]]):
        size = len(buffer)
        optimized_buffer = copy.copy(buffer)
        for i in range(size - 1):
            cmd = optimized_buffer[size - 1 - i]
            if cmd is None:
                continue
            self._optimize_if_prev_command_mergable(cmd, size - 1 - i, optimized_buffer)
        for i in range(size - 1):
            cmd = optimized_buffer[size - 1 - i]
            if cmd is None:
                continue
            self._optimize_if_prev_command_useless(cmd, size - 1 - i, optimized_buffer)
        optimized_buffer = [e for e in optimized_buffer if e is not None]
        return optimized_buffer

    def _optimize_if_prev_command_mergable(self, cur_cmd: List[str], cur_idx: int, command_buffer: List):
        prev_cmd = command_buffer[cur_idx - 1]
        if prev_cmd is None:
            return
        cur_cmd_type = cur_cmd[0]
        prev_cmd_type = prev_cmd[0]
        if cur_cmd_type != CMD_ERASE_TYPE or prev_cmd_type != CMD_ERASE_TYPE:
            return
        cur_start_addr = int(cur_cmd[1])
        cur_end_addr = cur_start_addr + int(cur_cmd[2])
        prev_start_addr = int(prev_cmd[1])
        prev_end_addr = prev_start_addr + int(prev_cmd[2])

        if prev_end_addr == cur_start_addr and (cur_end_addr - prev_start_addr) <= MAX_ERASE_SIZE:
            command_buffer[cur_idx - 1] = ['E', str(prev_start_addr), str(cur_end_addr - prev_start_addr)]
            command_buffer[cur_idx] = None
        elif cur_end_addr == prev_start_addr and (prev_end_addr - cur_start_addr) <= MAX_ERASE_SIZE:
            command_buffer[cur_idx - 1] = ['E', str(cur_start_addr), str(prev_end_addr - cur_start_addr)]
            command_buffer[cur_idx] = None

    def _optimize_if_prev_command_useless(self, cur_cmd: List[str], cur_idx: int, command_buffer: List):
        for i in range(cur_idx):
            prev_cmd = command_buffer[i]
            if prev_cmd is None:
                continue
            if self._check_erasable(cur_cmd, prev_cmd):
                command_buffer[i] = None

    def _check_erasable(self, cur_cmd: List[str], prev_cmd: List[str]):
        cur_cmd_type = cur_cmd[0]
        cur_cmd_addr = int(cur_cmd[1])
        prev_cmd_type = prev_cmd[0]
        prev_cmd_addr = int(prev_cmd[1])
        if cur_cmd_type == CMD_WRITE_TYPE and prev_cmd_type == CMD_WRITE_TYPE:
            if self._check_erasable_when_both_write(cur_cmd_addr, prev_cmd_addr):
                return True
        elif cur_cmd_type == CMD_WRITE_TYPE and prev_cmd_type == CMD_ERASE_TYPE:
            if self._check_erasable_when_cur_write_prev_erase(cur_cmd_addr, prev_cmd_addr, int(prev_cmd[2])):
                return True
        elif cur_cmd_type == CMD_ERASE_TYPE and prev_cmd_type == CMD_WRITE_TYPE:
            if self._check_erasable_when_cur_erase_prev_write(cur_cmd_addr, int(cur_cmd[2]), prev_cmd_addr):
                return True
        elif cur_cmd_type == CMD_ERASE_TYPE and prev_cmd_type == CMD_ERASE_TYPE:
            if self._check_erasable_when_both_erase(cur_cmd_addr, int(cur_cmd[2]), prev_cmd_addr, int(prev_cmd[2])):
                return True
        return False

    def _check_erasable_when_both_write(self, cur_cmd_addr, prev_cmd_addr):
        return prev_cmd_addr == cur_cmd_addr

    def _check_erasable_when_cur_write_prev_erase(self, cur_cmd_addr, prev_cmd_addr, prev_erase_size):
        return cur_cmd_addr <= prev_cmd_addr and prev_erase_size == 1

    def _check_erasable_when_cur_erase_prev_write(self, cur_cmd_addr, cur_erase_size, prev_cmd_addr):
        return cur_cmd_addr <= prev_cmd_addr < cur_cmd_addr + cur_erase_size

    def _check_erasable_when_both_erase(self, cur_cmd_addr, cur_erase_size, prev_cmd_addr, prev_erase_size):
        cur_end_addr = cur_cmd_addr + cur_erase_size
        prev_end_addr = prev_cmd_addr + prev_erase_size
        return cur_cmd_addr <= prev_cmd_addr and prev_end_addr <= cur_end_addr


def main():
    import sys

    try:
        ssd = SSD()
        ssd.run(sys.argv)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
