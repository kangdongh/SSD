import sys

from app.shell_api import ShellAPI
from app.system_call_handler import SystemCallHandler

FIRST_WRITE_VALUE = '0xAAAABBBB'
OVERWRITE_VALUE = '0x12345678'
PREDEFINED_LBA_HEAD = 0
PREDEFINED_LBA_TAIL = 6
PREDEFINED_LBA_RANGE = range(PREDEFINED_LBA_HEAD, PREDEFINED_LBA_TAIL)
DUPL_WRITE_COUNT = 10


def write_10times_overwrite_read_compare(api: ShellAPI):
    for _ in range(DUPL_WRITE_COUNT):
        for lba in PREDEFINED_LBA_RANGE:
            api.write(lba, FIRST_WRITE_VALUE)
    for lba in PREDEFINED_LBA_RANGE:
        api.write(lba, OVERWRITE_VALUE)
    for lba in PREDEFINED_LBA_RANGE:
        read_value = api.read(lba)
        if read_value != OVERWRITE_VALUE:
            raise ValueError(f"Read: {read_value} vs Expected: {OVERWRITE_VALUE}")


if __name__ == '__main__':
    system_call_handler = None
    if len(sys.argv) == 3:
        print("Initialize system call with given args")
        system_call_handler = SystemCallHandler(sys.argv[1], sys.argv[2])
    try:
        write_10times_overwrite_read_compare(ShellAPI(system_call_handler))
    except Exception:
        print("FAIL")
        exit(-1)
    print("PASS")
