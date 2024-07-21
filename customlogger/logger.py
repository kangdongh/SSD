import logging
import os
from datetime import datetime
from threading import Lock

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
LOG_FILE_NAME = 'latest.log'
LOG_NAME = 'SSD'
LOG_SIZE = 10 * 1024


class CloseFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.close()


class CommandLogger:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                cls._instance = super(CommandLogger, cls).__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        os.makedirs(LOG_DIR, exist_ok=True)
        self.log_file = os.path.join(LOG_DIR, LOG_FILE_NAME)
        self.logger = None
        self._initialized = True

    def _setup_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            file_handler = CloseFileHandler(self.log_file)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                fmt='[%(asctime)s.%(msecs)03d] %(module)-15s %(funcName)-25s: %(message)s',
                datefmt='%y.%m.%d %H:%M:%S')
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger

    def _close_handlers(self, logger):
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def _rotate_log(self, logger):
        if os.path.getsize(self.log_file) > LOG_SIZE:
            self._do_zip()
            new_log_file = self._rename_prev_log()
            self._close_handlers(logger)
            os.rename(self.log_file, os.path.join(LOG_DIR, new_log_file))

            self.logger = self._setup_logger(logger.name)

    def _rename_prev_log(self):
        os.chdir(LOG_DIR)
        with open(self.log_file, 'r') as f:
            last_time = datetime.strptime((f.readlines()[-1][1:22]),
                                          '%y.%m.%d %H:%M:%S.%f').strftime(
                '%y%m%d_%Hh_%Mm_%S.%f')[:-3]
            new_log_file = f'until_{last_time}s.log'
        return new_log_file

    def _do_zip(self) -> None:
        os.chdir(LOG_DIR)
        log_files = [f for f in os.listdir(LOG_DIR) if f.endswith('.log') and f.startswith('until')]
        for file in log_files:
            os.rename(file, file.replace('.log', '.zip'))

    def get_logger(self):
        self.logger = self._setup_logger(LOG_NAME)
        self._rotate_log(self.logger)
        return self.logger
