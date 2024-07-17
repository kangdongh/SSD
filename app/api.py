from app.system_call_handler import SystemCallHandler


def _check_valid_lba(lba: int):
    if 0 <= lba < 100:
        return
    raise ValueError(f"Invalid lba Error: {lba}")


def _check_valid_value(value: str):
    pass


def read_ssd(lba: int):
    _check_valid_lba(lba)
    s = SystemCallHandler()
    s.run(['R', str(lba)])
    return s.get_result()


def write_ssd(lba: int, value: str):
    _check_valid_lba(lba)
    _check_valid_value(value)
    s = SystemCallHandler()
    s.run(['W', str(lba), value])


def erase_ssd(start_lba: int, size: int):
    _check_valid_lba(start_lba)
    _check_valid_lba(start_lba + size)
    s = SystemCallHandler()
    while size > 0:
        erase_size = min(size, 10)
        s.run(['E', str(start_lba), str(erase_size)])
        size -= erase_size
        start_lba += erase_size


def flush_ssd():
    s = SystemCallHandler()
    s.run(['F'])
