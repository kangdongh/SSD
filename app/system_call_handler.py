import subprocess
from typing import List


class SystemCallHandler:
    _ssd_path: str
    _result_file_path: str

    def __init__(self, ssd_path, result_file_path):
        self._ssd_path = ssd_path
        self._result_file_path = result_file_path

    def run(self, system_call_arguments: List[str]):
        subprocess.run(['python', self._ssd_path] + system_call_arguments)

    def get_result(self) -> str:
        with open(self._result_file_path, 'r') as f:
            ret = f.readline().strip()
        return ret
