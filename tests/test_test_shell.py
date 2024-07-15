from unittest import TestCase

from app.test_shell import TestShell


class TestTestShell(TestCase):
    def setUp(self):
        self.sut = TestShell("test")

    def test_check_valid_cmd_length(self):
        self.assertEqual(1, self.sut.is_valid_command("help"))

    def test_check_invalid_cmd_length(self):
        self.assertEqual("INVALID COMMAND", self.sut.is_valid_command("read"))

    def test_check_valid_cmd(self):
        self.assertEqual(1, self.sut.is_valid_command("read 1"))

    def test_check_invalid_cmd(self):
        self.assertEqual("INVALID COMMAND", self.sut.is_valid_command("cmd1"))

    def test_check_valid_address(self):
        self.assertEqual(1, self.sut.is_valid_command("read 0"))

    def test_check_invalid_address(self):
        self.assertEqual("INVALID COMMAND", self.sut.is_valid_command("read 101"))

    def test_check_valid_value(self):
        self.assertEqual(1, self.sut.is_valid_command("write 3 0xAAAAAAAA"))

    def test_check_invalid_value(self):
        self.assertEqual("INVALID COMMAND", self.sut.is_valid_command("write 3 0xAAAAAAAZ"))
