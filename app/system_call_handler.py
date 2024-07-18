import os.path
import subprocess
from typing import List

PREDEFINED_SSD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../hardware/ssd.py')
PREDEFINED_RESULT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../hardware/result.txt')


class SystemCallHandler:
    _instance = None
    _ssd_path: str
    _result_file_path: str
    _initialized: bool

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    @classmethod
    def reset_instance(cls):
        if cls._instance is not None:
            del cls._instance
        cls._instance = None

    def __init__(self, ssd_path=PREDEFINED_SSD_PATH, result_file_path=PREDEFINED_RESULT_PATH):
        if self._initialized:
            return
        self._ssd_path = ssd_path
        self._result_file_path = result_file_path
        self._initialized = True

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


def initialize_system_call_handler(a, b):
    SystemCallHandler.reset_instance()
    SystemCallHandler(a, b)
