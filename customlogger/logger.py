import logging
import os
from datetime import datetime
from threading import Lock


class CloseFileHandler(logging.FileHandler):
    def emit(self, record):
        super().emit(record)
        self.close()
        self._rotate_log()

    def _rotate_log(self):
        log_file = self.baseFilename
        if os.path.getsize(log_file) > 10240:
            with open(log_file, 'r') as f:
                last_time = datetime.strptime((f.readlines()[-1][1:24]),
                                          '%Y.%m.%d %H:%M:%S.%f').strftime(
                '%y%m%d_%Hh_%Mm_%S.%f')[:-3]
            new_log_file = log_file.replace('latest', f'until_{last_time}s')

            self.close()

            os.rename(log_file, new_log_file)
            previous_logs = [f for f in os.listdir(os.path.dirname(log_file)) if
                             f.endswith('.txt') and 'latest' not in f and f != f'until_{last_time}s.txt']
            for old_log in previous_logs:
                old_log_path = os.path.join(os.path.dirname(log_file), old_log)
                zip_filename = os.path.splitext(old_log_path)[0] + '.zip'

                os.rename(old_log_path, zip_filename)

            self.stream = self._open()


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
        self.log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../logs')
        self.log_file = os.path.join(self.log_dir, 'latest.txt')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = self._setup_logger('command_logger')
        self._initialized = True

    def _setup_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            file_handler = CloseFileHandler(self.log_file)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(module)-15s %(funcName)-25s: %(message)s',
                datefmt='%Y.%m.%d %H:%M:%S')
            file_handler.setFormatter(formatter)

            logger.addHandler(file_handler)

        return logger

    def get_logger(self):
        return self.logger
