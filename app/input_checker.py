import os
from os.path import dirname, abspath


def check_valid_address_int(address: int):
    if not isinstance(address, int):
        raise TypeError(f"Address {address} is not integer")
    if 0 > address or address >= 100:
        raise ValueError(f"Address {address} is not in range")
    pass


def _get_hex(value: str):
    try:
        return int(value, 16)
    except ValueError:
        return -1


def check_valid_value(value: str):
    if not isinstance(value, str):
        raise TypeError(f"Value {value} is not string!")
    if len(value) != 10:
        raise ValueError(f"Length condition violation for Value {value}")
    if value[:2] != '0x':
        raise ValueError(f"Prefix condition violation for Value {value}")
    if _get_hex(value[2:]) == -1:
        raise ValueError(f"Value {value} is not a hexadecimal value")


_script_dir_path = os.path.join(dirname(dirname(abspath(__file__))), "scripts")


def is_script_name(name: str):
    return os.path.exists(script_name_to_path(name))


def script_name_to_path(name: str):
    return os.path.join(_script_dir_path, name + '.py')


def get_script_dir_path():
    return _script_dir_path


def set_script_dir_path(dir_path: str):
    if os.path.isdir(dir_path):
        global _script_dir_path
        _script_dir_path = dir_path
    raise ValueError()

