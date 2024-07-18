import os
import sys
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from customlogger.logger import CommandLogger
from hardware.ssd_interface import ISSD
from hardware.ssd_reader import SSDReader
from hardware.ssd_writer import SSDWriter
from hardware.buffer_optimizer import BufferOptimizer
from hardware.ssd_common_data import CMD_READ_TYPE, CMD_WRITE_TYPE, CMD_ERASE_TYPE, CMD_FLUSH_TYPE, MAX_ERASE_SIZE, \
    INITIAL_DATA_VALUE, MAX_DATA_LEN, MAX_RESULT_LEN, MAX_BUFFER_LEN

CURRENT_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'nand.txt')
RESULT_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'result.txt')
BUFFER_FILE_DIR = os.path.join(CURRENT_FILE_PATH, 'buffer.txt')

logger = CommandLogger().get_logger()
DEFAULT_SPACER = '               '


class SSD(ISSD):
    CMD_READ_LENGTH = 3
    CMD_WRITE_LENGTH = 4
    CMD_ERASE_LENGTH = 4
    CMD_FLUSH_LENGTH = 2
    DATA_LENGTH = 10

    def __init__(
            self,
            data_file_dir: str = DATA_FILE_DIR,
            result_file_dir: str = RESULT_FILE_DIR,
            buffer_file_dir: str = BUFFER_FILE_DIR
    ):
        self._data_file_dir = data_file_dir
        self._data_reader = SSDReader(data_file_dir)
        self._data_writer = SSDWriter(data_file_dir, max_lba=MAX_DATA_LEN)

        self._result_file_dir = result_file_dir
        self._result_writer = SSDWriter(result_file_dir, max_lba=MAX_RESULT_LEN)

        self._buffer_file_dir = buffer_file_dir
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
            for _ in range(MAX_BUFFER_LEN - buf_size):
                buffer_file.write('None\n')

    def _load_buffer_file(self):
        with open(self._buffer_file_dir, 'r') as buffer_file:
            lines = [line.strip() for line in buffer_file.readlines()]
            for line in lines:
                if line == 'None':
                    break
                self._buffer.append(line.split())

    def initialize(self):
        logger.debug('[ START ] initialize files')
        if not os.path.exists(self._data_file_dir):
            with open(self._data_file_dir, 'w') as data_file:
                for _ in range(MAX_DATA_LEN):
                    data_file.write(f'{INITIAL_DATA_VALUE}\n')

        if not os.path.exists(self._result_file_dir):
            with open(self._result_file_dir, 'w') as result_file:
                result_file.write('\n')

        if os.path.exists(self._buffer_file_dir):
            self._load_buffer_file()
        else:
            with open(self._buffer_file_dir, 'w') as buffer_file:
                for _ in range(MAX_BUFFER_LEN):
                    buffer_file.write('None\n')
        logger.debug('[SUCCESS] initialize files')

    def run(self, argv: List[str]):
        if not self._is_valid_cmd(argv):
            logger.debug('[ ERROR ] invalid input arguments: ' + str(argv))
            raise Exception('INVALID COMMAND')
        logger.debug(f'[ START ] SSD: {self._create_log_message(argv)}')
        cmd_type = argv[1]
        if cmd_type == CMD_READ_TYPE:
            lba = int(argv[2])
            self._read(lba)
        elif cmd_type == CMD_WRITE_TYPE or cmd_type == CMD_ERASE_TYPE:
            self._edit_data(argv[1:])
        elif cmd_type == CMD_FLUSH_TYPE:
            self._flush()
        else:
            logger.debug('[ ERROR ] invalid command type')
            raise Exception('INVALID COMMAND')
        logger.debug('[SUCCESS] SSD')

    def _create_log_message(self, argv: List[str]):
        if argv[1] == CMD_FLUSH_TYPE:
            return 'flush'
        elif argv[1] == CMD_READ_TYPE:
            return f'read lba={argv[2]}'
        elif argv[1] == CMD_WRITE_TYPE:
            return f'write: data={argv[3]} to lba={argv[2]}'
        elif argv[1] == CMD_ERASE_TYPE:
            return f'erase from lba={argv[2]} to lba={int(argv[2]) + int(argv[3]) - 1}'

    def _edit_data(self, argv: List[str]):
        if len(self._buffer) == MAX_BUFFER_LEN:
            logger.debug(f'{DEFAULT_SPACER}buffer is full')
            self._flush()
        logger.debug(f'{DEFAULT_SPACER}append command to buffer')
        self._buffer.append(argv)
        logger.debug(f'{DEFAULT_SPACER}optimizing buffer ...')
        self._buffer = self._buffer_optimizer.optimize_command_buffer(self._buffer)
        logger.debug(f'{DEFAULT_SPACER}optimizing complete')

    def _flush(self):
        logger.debug(f'{DEFAULT_SPACER}flushing ...')
        for command in self._buffer:
            command_type = command[0]
            address = int(command[1])
            if command_type == CMD_WRITE_TYPE:
                self._write(address, command[2])
            elif command_type == CMD_ERASE_TYPE:
                self._erase(address, int(command[2]))
        self._buffer.clear()
        logger.debug(f'{DEFAULT_SPACER}flushing complete')

    def _read(self, address):
        logger.debug(f'{DEFAULT_SPACER}read ...')
        logger.debug(f'{DEFAULT_SPACER}searching in the buffer ...')
        buffer_result = self._search_buffer(address)
        if buffer_result[0]:
            logger.debug(f'{DEFAULT_SPACER}success to find data in the buffer ...')
            read_value = buffer_result[1]
        else:
            logger.debug(f'{DEFAULT_SPACER}fail to find data in the buffer ...')
            logger.debug(f'{DEFAULT_SPACER}start to full read ...')
            read_value = self._data_reader.read(address)
        self._result_writer.write(0, 1, read_value)
        logger.debug(f'{DEFAULT_SPACER}read complete')

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
                    ret_val = [True, INITIAL_DATA_VALUE]
        return ret_val

    def _write(self, address, data):
        logger.debug(f'{DEFAULT_SPACER}write ...')
        self._data_writer.write(address, 1, data)
        logger.debug(f'{DEFAULT_SPACER}write complete')

    def _erase(self, address, size):
        logger.debug(f'{DEFAULT_SPACER}erase ...')
        self._data_writer.write(address, size, INITIAL_DATA_VALUE)
        logger.debug(f'{DEFAULT_SPACER}erase complete')

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
        if lba >= MAX_DATA_LEN:
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
        if size <= MAX_ERASE_SIZE and (lba + size) <= MAX_DATA_LEN:
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


def main():
    import sys

    try:
        ssd = SSD()
        ssd.run(sys.argv)
    except Exception as e:
        logger.debug('[  FAIL ] SSD')
        print(e)


if __name__ == '__main__':
    main()
