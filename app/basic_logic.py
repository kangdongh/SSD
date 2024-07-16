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
        help_str = """
        ****************************************
        ********** COMMAND HELP **********
        ****************************************
        1. ** write: Write value to SSD / usage: write <LBA> <VALUE>
        2. ** read: Read value from SSD / usage: read <LBA>
        3. ** exit: Exit program / usage exit
        4. ** help: Help command
        5. ** fullwrite: Write value at all LBAs / usage: fullwrite <VALUE>
        6. ** fullread: Read all LBAs / usage: fullread
        ****************************************
                """

        print(f'{help_str}')
        return help_str
