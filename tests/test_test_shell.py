from unittest import TestCase

from app.test_shell import TestShell


class TestTestShell(TestCase):
    def setUp(self):
        self.sut = TestShell("test")

    def test_check_valid_cmd_length(self):
        self.assertEqual(True, self.sut.is_valid_command("help"))
        self.assertEqual(True, self.sut.is_valid_command("HELP"))

    def test_check_invalid_cmd_length(self):
        self.assertEqual(False, self.sut.is_valid_command("read"))
        self.assertEqual(False, self.sut.is_valid_command("write"))
        self.assertEqual(False, self.sut.is_valid_command("fullwrite"))
        self.assertEqual(False, self.sut.is_valid_command("fullread 3"))
        self.assertEqual(False, self.sut.is_valid_command("write 3 4 6"))
        self.assertEqual(False, self.sut.is_valid_command("help oh"))

    def test_check_valid_cmd(self):
        self.assertEqual(True, self.sut.is_valid_command("read 1"))
        self.assertEqual(True, self.sut.is_valid_command("write 1 0xAAAAAAAA"))
        self.assertEqual(True, self.sut.is_valid_command("exit"))
        self.assertEqual(True, self.sut.is_valid_command("Help"))
        self.assertEqual(True, self.sut.is_valid_command("FullRead"))
        self.assertEqual(True, self.sut.is_valid_command("FullWrite 0xAAAAAAAA"))

    def test_check_invalid_cmd(self):
        self.assertEqual(False, self.sut.is_valid_command("cmd1"))
        self.assertEqual(False, self.sut.is_valid_command("readwrite"))
        self.assertEqual(False, self.sut.is_valid_command("full_read"))
        self.assertEqual(False, self.sut.is_valid_command("full-write 1 0xAAAAAAA"))
        self.assertEqual(False, self.sut.is_valid_command("writing"))
        self.assertEqual(False, self.sut.is_valid_command("reading"))

    def test_check_valid_address(self):
        self.assertEqual(True, self.sut.is_valid_command("read 0"))

    def test_check_invalid_address(self):
        self.assertEqual(False, self.sut.is_valid_command("read 101"))
        self.assertEqual(False, self.sut.is_valid_command("read -2"))

    def test_check_valid_value(self):
        self.assertEqual(True, self.sut.is_valid_command("write 3 0xAAAAAAAA"))
        self.assertEqual(True, self.sut.is_valid_command("write 3 0xA0AA1AAA"))
        self.assertEqual(True, self.sut.is_valid_command("fullwrite 0xAABBAAAA"))

    def test_check_invalid_value(self):
        self.assertEqual(False, self.sut.is_valid_command("write 3 0xAAAAAAAZ"))
        self.assertEqual(False, self.sut.is_valid_command("fullwrite 3 0xNAAAAAAZ"))
        self.assertEqual(False, self.sut.is_valid_command("write 3 0xAA"))
        self.assertEqual(False, self.sut.is_valid_command("write 3 0xAA__"))
        self.assertEqual(False, self.sut.is_valid_command("write 3 0xAA1"))
        self.assertEqual(False, self.sut.is_valid_command("write 3 0xAA123243421"))
