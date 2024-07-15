from typing import List

from hardware.ssd_interface import ISSD
from hardware.ssd_reader_interface import ISSDReader
from hardware.ssd_writer_interface import ISSDWriter


class SSD(ISSD):
    _reader: ISSDReader
    _writer: ISSDWriter

if __name__ == '__main__':
    import sys
    ssd = SSD()
    ssd.run(sys.argv)
