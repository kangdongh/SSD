import sys

from app.scripts.script_utils import run_script
from app.shell_api import ShellAPI

FIRST_WRITE_VALUE = '0xAAAABBBB'
OVERWRITE_VALUE = '0x12345678'
PREDEFINED_LBA_HEAD = 0
PREDEFINED_LBA_TAIL = 6
PREDEFINED_LBA_RANGE = range(PREDEFINED_LBA_HEAD, PREDEFINED_LBA_TAIL)
DUPL_WRITE_COUNT = 10


def write_10times_overwrite_read_compare(api: ShellAPI):
    print("dupl write...")
    for _ in range(DUPL_WRITE_COUNT):
        for lba in PREDEFINED_LBA_RANGE:
            api.write(lba, FIRST_WRITE_VALUE)
    print("overwrite...")
    for lba in PREDEFINED_LBA_RANGE:
        api.write(lba, OVERWRITE_VALUE)
    print("read and compare...")
    for lba in PREDEFINED_LBA_RANGE:
        read_value = api.read(lba)
        if read_value != OVERWRITE_VALUE:
            raise ValueError(f"Read: {read_value} vs Expected: {OVERWRITE_VALUE}")


if __name__ == '__main__':
    ret = run_script(write_10times_overwrite_read_compare, sys.argv)
    exit(ret)
