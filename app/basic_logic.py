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
        7. ** testapp1: After fullwrite, Check If fullread value is correct according to the written value / usage: testapp1
        8. ** testapp2: After overwrite, read the LBA value to make sure LBA value is correct according to overwritten value / usage: testapp2
        ****************************************
                """

        print(f'{help_str}')
        return help_str

    def exit(self) -> str:
        pass