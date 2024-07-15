class BasicLogic:
    _ssd_path: str

    def __init__(self, ssd_path):
        self._ssd_path = ssd_path

    def read(self, args):
        pass

    def write(self, args):
        pass

    def full_read(self):
        pass

    def full_write(self):
        pass

    def help(self) -> str:
        pass

    def exit(self) -> str:
        pass
