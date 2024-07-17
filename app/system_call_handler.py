import subprocess
from typing import List


class SystemCallHandler:
    _instance = None
    _ssd_path: str
    _result_file_path: str

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, ssd_path=None, result_file_path=None):
        self._ssd_path = ssd_path
        self._result_file_path = result_file_path

    def run(self, system_call_arguments: List[str]):
        subprocess.run(['python', self._ssd_path] + system_call_arguments)

    def get_result(self) -> str:
        with open(self._result_file_path, 'r') as f:
            ret = f.readline().strip()
        return ret
