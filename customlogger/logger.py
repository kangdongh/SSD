import logging
import os
from threading import Lock

from customlogger.custom_rotating_file_handler import CustomRotatingFileHandler

LOG_DIR = '../logs'
LOG_FILE_NAME = 'latest.log'
LOG_NAME = 'SSD'


class CommandLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        self.logger = None
        self.set_logger()
        self._initialized = True

    def set_logger(self):
        self.logger = logging.getLogger(LOG_NAME)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(CustomRotatingFileHandler(alias="alias", basedir=LOG_DIR))

    def get_logger(self) -> logging.Logger:
        return self.logger


if __name__ == '__main__':
    CommandLogger().get_logger().debug('test kkkkkk')