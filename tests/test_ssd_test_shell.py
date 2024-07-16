import io
import sys
from unittest import TestCase
from unittest.mock import MagicMock

from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2
from app.ssd_test_shell import SSDTestShell, CommandValidator


class TestSSDTestShell(TestCase):
    def setUp(self):
        self.mk_basic = MagicMock(BasicLogic)
        self.mk_test_app_1 = MagicMock(TestApp1)
        self.mk_test_app_2 = MagicMock(TestApp2)
        self.validator = CommandValidator()
        self.sut = SSDTestShell(self.mk_basic, self.validator)
        self.sut.set_apps(self.mk_test_app_1, self.mk_test_app_2)

    def test_check_valid_cmd_length(self):
        valid_cmds = ["help", "HELP"]
        for cmd in valid_cmds:
            with self.subTest(cmd=cmd):
                self.assertTrue(self.validator.is_valid_command(cmd))

    def test_check_invalid_cmd_length(self):
        invalid_cmds = ["read", "write", "fullwrite", "fullread 3", "write 3 4 6", "help oh"]
        for cmd in invalid_cmds:
            with self.subTest(cmd=cmd):
                self.assertFalse(self.validator.is_valid_command(cmd))

    def test_check_valid_cmd(self):
        valid_cmds = ["read 1", "write 1 0xAAAAAAAA", "exit", "Help", "FullRead",
                      "FullWrite 0xAAAAAAAA"]
        for cmd in valid_cmds:
            with self.subTest(cmd=cmd):
                self.assertTrue(self.validator.is_valid_command(cmd))

    def test_check_invalid_cmd(self):
        invalid_cmds = ["cmd1", "readwrite", "full_read", "full-write 1 0xAAAAAAA", "writing",
                        "reading"]
        for cmd in invalid_cmds:
            with self.subTest(cmd=cmd):
                self.assertFalse(self.validator.is_valid_command(cmd))

    def test_check_valid_address(self):
        valid_addresses = ["read 0"]
        for cmd in valid_addresses:
            with self.subTest(cmd=cmd):
                self.assertTrue(self.validator.is_valid_command(cmd))

    def test_check_invalid_address(self):
        invalid_addresses = ["read 101", "read -2"]
        for cmd in invalid_addresses:
            with self.subTest(cmd=cmd):
                self.assertFalse(self.validator.is_valid_command(cmd))

    def test_check_valid_value(self):
        valid_values = ["write 3 0xAAAAAAAA", "write 3 0xA0AA1AAA", "fullwrite 0xAABBAAAA",
                        "fullwrite 0x00000000"]
        for cmd in valid_values:
            with self.subTest(cmd=cmd):
                self.assertTrue(self.validator.is_valid_command(cmd))

    def test_check_invalid_value(self):
        invalid_values = [
            "write 3 0xAAAAAAAZ", "fullwrite 3 0xNAAAAAAZ", "write 3 0xAA",
            "write 3 0xAA__", "write 3 0xAA1", "write 3 0xAA123243421"
        ]
        for cmd in invalid_values:
            with self.subTest(cmd=cmd):
                self.assertFalse(self.validator.is_valid_command(cmd))

    def test_run_exit(self):
        self.assertEqual(-1, self.sut.run('EXIT'))

    def test_run_help(self):
        self.mk_basic.help.return_value = 'ret'
        self.assertEqual(0, self.sut.run('HELP'))
        self.mk_basic.help.assert_called_once()

    def test_run_help_print(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.mk_basic.help.return_value = 'ret'
        self.sut.run('HELP')

        self.assertEqual(captured_output.getvalue().strip(), "ret")

    def test_run_read(self):
        self.mk_basic.read.return_value = 'return read value'
        self.sut.run('READ ADDR')
        self.mk_basic.read.assert_called_once_with('ADDR')

    def test_run_read_print(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.mk_basic.read.return_value = 'ret'
        self.sut.run('READ ADDR')

        self.assertEqual(captured_output.getvalue().strip(), "ret")

    def test_run_write(self):
        self.sut.run('WRITE ADDR VALUE')
        self.mk_basic.write.assert_called_once_with('ADDR', 'VALUE')

    def test_run_fullread(self):
        self.mk_basic.full_read.return_value = 'full read'
        self.sut.run('FULLREAD')
        self.mk_basic.full_read.assert_called_once()

    def test_run_full_read_print(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.mk_basic.full_read.return_value = 'ret'
        self.sut.run('FULLREAD')

        self.assertEqual(captured_output.getvalue().strip(), "ret")

    def test_run_fullwrite(self):
        self.sut.run('FULLWRITE VALUE')
        self.mk_basic.full_write.assert_called_once_with('VALUE')

    def test_run_testapp1(self):
        self.sut.run('TESTAPP1')
        self.mk_test_app_1.run.assert_called_once_with(self.mk_basic)

    def test_run_testapp2(self):
        self.sut.run('TESTAPP2')
        self.mk_test_app_2.run.assert_called_once_with(self.mk_basic)
