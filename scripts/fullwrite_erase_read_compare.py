import sys

from app.api import write_ssd, read_ssd, erase_ssd
from app.system_call_handler import initialize_system_call_handler

FULL_WRITE_VALUE = '0x00000004'
ERASE_VALUE = '0x00000000'


def fullwrite_erase_read_compare():
    print("full write...")
    for lba in range(100):
        write_ssd(lba, FULL_WRITE_VALUE)
    print("partial erase...")
    erase_ssd(50, 45)
    print("check...")
    for lba in range(50):
        read_value = read_ssd(lba)
        if read_value != FULL_WRITE_VALUE:
            raise ValueError(f"Read[{lba}]: {read_value} vs Expected: {FULL_WRITE_VALUE}")
    for lba in range(50, 95):
        read_value = read_ssd(lba)
        if read_value != ERASE_VALUE:
            raise ValueError(f"Read[{lba}]: {read_value} vs Expected: {ERASE_VALUE}")
    for lba in range(95, 100):
        read_value = read_ssd(lba)
        if read_value != FULL_WRITE_VALUE:
            raise ValueError(f"Read[{lba}]: {read_value} vs Expected: {FULL_WRITE_VALUE}")


if __name__ == '__main__':
    if len(sys.argv) == 3:
        print("Initialize system call with given args")
        initialize_system_call_handler(sys.argv[1], sys.argv[2])
    try:
        fullwrite_erase_read_compare()
    except Exception:
        print("FAIL")
        exit(-1)
    print("PASS")
