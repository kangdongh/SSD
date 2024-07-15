import os

class BasicLogic:
    _ssd_path: str

    def __init__(self, ssd_path):
        self._ssd_path = ssd_path

    def read(self, args):
        # Arg 1 : LBA 정보
        arg1 = 2
        result = 0x9988FFFF  # LBA 2의 정보 출력
        print(f'Read Value from LBA {arg1}')

        if os.path.exists(self._ssd_path):
            os.remove(self._ssd_path)
        with open('result.txt', 'w') as file:  # _ssd_path = result.txt
            file.write('\n')

    def write(self, *args):
        # Arg 1 : LBA 정보
        # Arg 2 : 저장할 값
        arg1 = 3
        arg2 = 0x9988FFFF
        print(f'Write Value {arg2} to LBA {arg1}')

    def full_read(self):
        for lba in range(0, 99 + 1):
            self.read(lba)

    def full_write(self):
        print(f'Start to write value at all LBAs')
        value = 0x00000000
        for lba in range(0, 99 + 1):
            self.write(lba, value)

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

    def exit(self) -> bool:
        print(f'Exit SSD Program')
        return True
