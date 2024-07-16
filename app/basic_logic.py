class BasicLogic:
    _ssd_path: str

    def __init__(self, ssd_path):
        self._ssd_path = ssd_path

    def read(self, lba: str) -> str:
        pass

    def write(self, lba: str, value: str) -> None:
        pass

    def full_read(self) -> str:
        pass

    def full_write(self, value: str) -> None:
        pass

    def help(self) -> str:
        pass
