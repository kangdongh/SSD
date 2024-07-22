import sys

from app.scripts.script_utils import run_script
from app.shell_api import ShellAPI
from customlogger.logger import CommandLogger

FULL_WRITE_VALUE = '0x00000004'
ERASE_VALUE = '0x00000000'

logger = CommandLogger().get_logger()


def fullwrite_erase_read_compare(api: ShellAPI):
    print("full write...")
    for lba in range(100):
        api.write(lba, FULL_WRITE_VALUE)
    print("partial erase...")
    api.erase(50, 45)
    print("check...")
    for lba in range(50):
        read_value = api.read(lba)
        if read_value != FULL_WRITE_VALUE:
            raise ValueError(f"Read[{lba}]: {read_value} vs Expected: {FULL_WRITE_VALUE}")
    for lba in range(50, 95):
        read_value = api.read(lba)
        if read_value != ERASE_VALUE:
            raise ValueError(f"Read[{lba}]: {read_value} vs Expected: {ERASE_VALUE}")
    for lba in range(95, 100):
        read_value = api.read(lba)
        if read_value != FULL_WRITE_VALUE:
            raise ValueError(f"Read[{lba}]: {read_value} vs Expected: {FULL_WRITE_VALUE}")


if __name__ == '__main__':
    ret = run_script(fullwrite_erase_read_compare, sys.argv)
    exit(ret)
