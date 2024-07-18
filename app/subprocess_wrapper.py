import os
import subprocess
import sys


def _run_with_env(*args, **kwargs):
    current_sys_path = os.pathsep.join(sys.path)
    kwargs['env'] = {**os.environ, 'PYTHONPATH': current_sys_path}
    return subprocess.run(*args, **kwargs)


def subprocess_run(args):
    return _run_with_env(args)


def subprocess_run_ignore_stdout(args):
    return _run_with_env(args, capture_output=True, text=True)
