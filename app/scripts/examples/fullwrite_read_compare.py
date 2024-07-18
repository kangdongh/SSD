import sys

from app.scripts.script_utils import run_script
from app.shell_api import ShellAPI

FULL_WRITE_VALUE = '0x00000001'


def fullwrite_read_compare(api: ShellAPI):
    for lba in range(100):
        api.write(lba, FULL_WRITE_VALUE)
    for lba in range(100):
        read_value = api.read(lba)
        if read_value != FULL_WRITE_VALUE:
            raise ValueError(f"Read: {read_value} vs Expected: {FULL_WRITE_VALUE}")


if __name__ == '__main__':
    ret = run_script(fullwrite_read_compare, sys.argv)
    exit(ret)
