import os.path
import subprocess
from typing import List

PREDEFINED_SSD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../hardware/ssd.py')
PREDEFINED_RESULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../hardware/result.txt')


class SystemCallHandler:
    _ssd_path: str
    _result_file_path: str

    def __init__(self, ssd_path=PREDEFINED_SSD_PATH, result_file_path=PREDEFINED_RESULT_PATH):
        self._ssd_path = os.path.abspath(ssd_path)
        self._result_file_path = os.path.abspath(result_file_path)

    def run(self, system_call_arguments: List[str]):
        if not os.path.exists(self._ssd_path):
            raise RuntimeError(f"Invalid system call path: {self._ssd_path}")
        subprocess.run(['python', self._ssd_path] + system_call_arguments)

    def get_result(self) -> str:
        if not os.path.exists(self._result_file_path):
            raise RuntimeError(f"Invalid system call path: {self._result_file_path}")
        with open(self._result_file_path, 'r') as f:
            ret = f.readline().strip()
        return ret

    def get_ssd_path(self):
        return os.path.abspath(self._ssd_path)

    def get_result_file_path(self):
        return os.path.abspath(self._result_file_path)

