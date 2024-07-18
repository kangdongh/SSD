import logging
import os
import sys
from datetime import datetime
from threading import Lock

from customlogger.custom_rotating_file_handler import CustomRotatingFileHandler

LOG_DIR = '../logs'
LOG_FILE_NAME = 'latest.log'
LOG_NAME = 'SSD'


class CommandLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(CommandLogger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        if not os.path.exists(LOG_DIR):
            os.makedirs(LOG_DIR)
        self.logger = None
        self._initialized = True

    def get_logger(self) -> logging.Logger:
        self.logger = logging.getLogger(LOG_NAME)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(CustomRotatingFileHandler(alias="alias", basedir=LOG_DIR))

        return self.logger
