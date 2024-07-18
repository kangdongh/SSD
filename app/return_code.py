from enum import Enum, auto


class ReturnCode(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    EXIT = auto()
