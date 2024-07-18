import sys

from app.scripts.script_utils import run_script


def fail_test(api):
    raise ValueError(f"This test must fail")


if __name__ == '__main__':
    ret = run_script(fail_test, sys.argv)
    exit(ret)
