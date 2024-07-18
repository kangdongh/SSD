import textwrap
from typing import List

from app.system_call_handler import SystemCallHandler
from logger import CommandLogger

HELP_DESC = textwrap.dedent("""
- write: Write value to SSD / usage: write <LBA> <VALUE>
- read: Read value from SSD / usage: read <LBA>
- exit: Exit program / usage exit
- help: Help command
- fullwrite: Write value at all LBAs / usage: fullwrite <VALUE>
- fullread: Read all LBAs / usage: fullread
- erase : Erase value of SIZE from LBA on SSD / usage : erase <LBA> <SIZE>
- erase_range : Erase value from startLBA to endLBA on SSD / usage : erase_range <Start LBA>  <End LBA> 
- flush: Execute 10 commands in the Command Buffer to make the empty Buffer. / usage: flush
""").strip()


class BasicLogic:
    _system_call_handler: SystemCallHandler
    _logger: CommandLogger

    def __init__(self, system_call_handler: SystemCallHandler, logger: CommandLogger):
        self._system_call_handler = system_call_handler
        self._logger = logger

    def read(self, lba: str) -> str:
        self._logger.get_logger('READ', self.__class__.__name__, 'read').info(f'Reading from LBA {lba}')
        self._system_call(['R', lba])
        return self._read_result()

    def write(self, lba: str, value: str) -> None:
        self._logger.get_logger('WRITE', self.__class__.__name__, 'write').info(f'Writing {value} to LBA {lba}')
        self._system_call(['W', lba, value])

    def full_read(self) -> str:
        self._logger.get_logger('FULLREAD', self.__class__.__name__, 'full_read').info('Performing full read')
        full_read_strs = []
        for lba in range(0, 100):
            full_read_strs.append(self.read(str(lba)))
        return '\n'.join(full_read_strs)

    def full_write(self, value: str) -> None:
        self._logger.get_logger('FULLWRITE', self.__class__.__name__, 'full_write').info(
            f'Performing full write with value {value}')
        for lba in range(0, 100):
            self.write(str(lba), value)

    def help(self) -> str:
        self._logger.get_logger('HELP', self.__class__.__name__, 'help').info('Showing help')
        return HELP_DESC

    def erase(self, lba: str, size: str) -> None:
        lba = int(lba)
        size = int(size)

        while size > 0:
            current_size = min(size, 10)
            self._system_call(['E', str(lba), str(current_size)])
            size -= current_size
            lba += 10

    def erase_range(self, start_lba: str, end_lba: str) -> None:
        start_lba = int(start_lba)
        size = int(end_lba) - int(start_lba)
        self.erase(str(start_lba), str(size))

    def _system_call(self, system_call_arguments: List[str]):
        self._system_call_handler.run(system_call_arguments)

    def _read_result(self):
        return self._system_call_handler.get_result()
