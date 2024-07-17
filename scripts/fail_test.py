import sys

from app.system_call_handler import initialize_system_call_handler


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
