import sys

from app.shell_api import ShellAPI
from app.system_call_handler import SystemCallHandler

FULL_WRITE_VALUE = '0x00000004'
ERASE_VALUE = '0x00000000'


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
    system_call_handler = None
    if len(sys.argv) == 3:
        print("Initialize system call with given args")
        system_call_handler = SystemCallHandler(sys.argv[1], sys.argv[2])
    try:
        fullwrite_erase_read_compare(ShellAPI(system_call_handler))
    except Exception:
        print("FAIL")
        exit(-1)
    print("PASS")
