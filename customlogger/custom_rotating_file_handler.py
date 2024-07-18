import logging
import os
from datetime import datetime
from fnmatch import fnmatch
from logging import handlers

LOG_FILE_NAME = 'latest.log'


class CustomRotatingFileHandler(handlers.RotatingFileHandler):
    def __init__(self, alias, basedir, mode='a', max_bytes=10000, backup_count=1, encoding=None,
                 delay=0):
        self.alias_ = alias
        self.basedir_ = basedir

        self.baseFilename = self.getBaseFilename()

        handlers.RotatingFileHandler.__init__(self, self.baseFilename, mode, max_bytes,
                                              backup_count, encoding, delay)

        self.setFormatter(
            logging.Formatter(
                fmt='[%(asctime)s.%(msecs)03d] %(module)-15s %(funcName)-25s: %(message)s',
                datefmt='%y.%m.%d %H:%M:%S'))

    def getBaseFilename(self):
        return os.path.join(self.basedir_, LOG_FILE_NAME)

    def doRollover(self):
        super().doRollover()
        os.chdir(self.basedir_)
        if os.path.exists(f'{LOG_FILE_NAME}.1'):
            self._do_zip()
            os.rename(f'{LOG_FILE_NAME}.1', self._get_rotating_filename())

    def _get_rotating_filename(self) -> str:
        os.chdir(self.basedir_)
        with open(f'{LOG_FILE_NAME}.1', 'r') as f:
            last_time = datetime.strptime((f.readlines()[-1][1:22]),
                                          '%y.%m.%d %H:%M:%S.%f').strftime(
                '%y%m%d_%Hh_%Mm_%S.%f')[:-3]
            return f'until_{last_time}s.log'

    def _do_zip(self) -> None:
        os.chdir(self.basedir_)
        for file_name in os.listdir(os.getcwd()):
            if fnmatch(file_name, 'until_*.log'):
                os.rename(file_name, f'{file_name[:-3]}zip')
