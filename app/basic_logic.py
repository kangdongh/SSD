import textwrap
from typing import List

from app.system_call_handler import SystemCallHandler

HELP_DESC = textwrap.dedent("""
- write: Write value to SSD / usage: write <LBA> <VALUE>
- read: Read value from SSD / usage: read <LBA>
- exit: Exit program / usage exit
- help: Help command
- fullwrite: Write value at all LBAs / usage: fullwrite <VALUE>
- fullread: Read all LBAs / usage: fullread
""").strip()


class BasicLogic:
    _system_call_handler: SystemCallHandler

    def __init__(self, system_call_handler: SystemCallHandler):
        self._system_call_handler = system_call_handler

    def read(self, lba: str) -> str:
        self._system_call_handler.run(['R', lba])
        return self._system_call_handler.get_result()

    def write(self, lba: str, value: str) -> None:
        self._system_call_handler.run(['W', lba, value])

    def full_read(self) -> str:
        full_read_strs = []
        for lba in range(0, 100):
            full_read_strs.append(self.read(str(lba)))
        return '\n'.join(full_read_strs)

    def full_write(self, value: str) -> None:
        for lba in range(0, 100):
            self.write(str(lba), value)

    def help(self) -> str:
        return HELP_DESC

    def _system_call(self, system_call_arguments: List[str]):
        self._system_call_handler.run(system_call_arguments)

    def _read_result(self):
        return self._system_call_handler.get_result()
