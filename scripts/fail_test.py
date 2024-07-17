import sys

from app.api import write_ssd, read_ssd
from app.system_call_handler import initialize_system_call_handler

FIRST_WRITE_VALUE = '0xAAAABBBB'
OVERWRITE_VALUE = '0x12345678'
PREDEFINED_LBA_HEAD = 0
PREDEFINED_LBA_TAIL = 6
PREDEFINED_LBA_RANGE = range(PREDEFINED_LBA_HEAD, PREDEFINED_LBA_TAIL)
DUPL_WRITE_COUNT = 10


def fail_test():
    raise ValueError(f"This test must fail")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print("Initialize system call with given args")
        initialize_system_call_handler(sys.argv[1], sys.argv[2])
    try:
        fail_test()
    except Exception:
        print("FAIL")
        exit(-1)
    print("PASS")
