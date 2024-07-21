import logging
import os
from datetime import datetime
from threading import Lock

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
LOG_FILE_NAME = 'latest.log'
LOG_NAME = 'SSD'


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
        if os.path.getsize(self.log_file) > 10240:  # 10KB
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                last_log = lines[-1]
                last_log_time = last_log.split(' - ')[0]
                last_log_time = datetime.strptime(last_log_time, '%Y-%m-%d %H:%M:%S,%f')

            now = last_log_time.strftime("%Y%m%d_%H%M%S")
            new_log_file = os.path.join(LOG_DIR, f'{now}.log')
            self._close_handlers(logger)
            os.rename(self.log_file, new_log_file)

            previous_logs = [f for f in os.listdir(LOG_DIR) if
                             f.endswith('.log') and f != LOG_FILE_NAME and f != f'{now}.log']
            for old_log in previous_logs:
                old_log_path = os.path.join(LOG_DIR, old_log)
                zip_filename = os.path.splitext(old_log_path)[0] + '.zip'
                os.rename(old_log_path, zip_filename)

            self.logger = self._setup_logger(logger.name)

    def get_logger(self, cmd_name=None, class_name=None, func_name=None):
        name = class_name if class_name else 'default'
        self.logger = self._setup_logger(name)
        self._rotate_log(self.logger)
        return self.logger
