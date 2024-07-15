import sys

from hardware.ssd import SSD

if __name__ == '__main__':
    ssd = SSD()
    ssd.run(sys.argv)
