import logging
import os
import sys
from datetime import datetime
import zipfile
class CommandLogger:
    def __init__(self):
        self.log_dir = 'logs'
        self.log_file = os.path.join(self.log_dir, 'latest.txt')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.logger = None

    def _setup_logger(self, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        if not logger.handlers:
            file_handler = logging.FileHandler(self.log_file)
            file_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(message)s')
            file_handler.setFormatter(formatter)

            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.DEBUG)
            stream_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

        return logger

    def _close_handlers(self, logger):
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

    def _rotate_log(self, logger):
        if os.path.getsize(self.log_file) > 1024:  # 10KB
            now = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_log_file = os.path.join(self.log_dir, f'{now}.txt')
            self._close_handlers(logger)
            os.rename(self.log_file, new_log_file)

            previous_logs = [f for f in os.listdir(self.log_dir) if f.endswith('.txt') and f != 'latest.txt' and f != f'{now}.txt']
            for old_log in previous_logs:
                old_log_path = os.path.join(self.log_dir, old_log)
                zip_filename = os.path.splitext(old_log_path)[0] + '.zip'
                with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(old_log_path, os.path.basename(old_log_path))
                os.remove(old_log_path)

            self.logger = self._setup_logger(logger.name)

    def get_logger(self, cmd_name=None, class_name=None, func_name=None):
        name = class_name if class_name else 'default'
        self.logger = self._setup_logger(name)
        self._rotate_log(self.logger)
        return self.logger