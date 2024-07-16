from unittest import TestCase
from unittest.mock import MagicMock

from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2
from app.test_shell import TestShell


class TestTestShell(TestCase):
    def setUp(self):
        self.mk_basic = MagicMock(BasicLogic("test"))
        self.mk_test_app_1 = MagicMock(TestApp1)
        self.mk_test_app_2 = MagicMock(TestApp2)
        self.sut = TestShell(self.mk_basic)
        self.sut.set_apps(self.mk_test_app_1, self.mk_test_app_2)

    def test_check_valid_cmd_length(self):
        valid_cmds = ["help", "HELP"]
        for cmd in valid_cmds:
            with self.subTest(cmd=cmd):
                self.assertEqual(True, self.sut.is_valid_command(cmd))

    def test_check_invalid_cmd_length(self):
        invalid_cmds = ["read", "write", "fullwrite", "fullread 3", "write 3 4 6", "help oh"]
        for cmd in invalid_cmds:
            with self.subTest(cmd=cmd):
                self.assertEqual(False, self.sut.is_valid_command(cmd))

    def test_check_valid_cmd(self):
        valid_cmds = ["read 1", "write 1 0xAAAAAAAA", "exit", "Help", "FullRead", "FullWrite 0xAAAAAAAA"]
        for cmd in valid_cmds:
            with self.subTest(cmd=cmd):
                self.assertEqual(True, self.sut.is_valid_command(cmd))

    def test_check_invalid_cmd(self):
        invalid_cmds = ["cmd1", "readwrite", "full_read", "full-write 1 0xAAAAAAA", "writing", "reading"]
        for cmd in invalid_cmds:
            with self.subTest(cmd=cmd):
                self.assertEqual(False, self.sut.is_valid_command(cmd))

    def test_check_valid_address(self):
        valid_addresses = ["read 0"]
        for cmd in valid_addresses:
            with self.subTest(cmd=cmd):
                self.assertEqual(True, self.sut.is_valid_command(cmd))

    def test_check_invalid_address(self):
        invalid_addresses = ["read 101", "read -2"]
        for cmd in invalid_addresses:
            with self.subTest(cmd=cmd):
                self.assertEqual(False, self.sut.is_valid_command(cmd))

    def test_check_valid_value(self):
        valid_values = ["write 3 0xAAAAAAAA", "write 3 0xA0AA1AAA", "fullwrite 0xAABBAAAA"]
        for cmd in valid_values:
            with self.subTest(cmd=cmd):
                self.assertEqual(True, self.sut.is_valid_command(cmd))

    def test_check_invalid_value(self):
        invalid_values = [
            "write 3 0xAAAAAAAZ", "fullwrite 3 0xNAAAAAAZ", "write 3 0xAA",
            "write 3 0xAA__", "write 3 0xAA1", "write 3 0xAA123243421"
        ]
        for cmd in invalid_values:
            with self.subTest(cmd=cmd):
                self.assertEqual(False, self.sut.is_valid_command(cmd))

    def test_run_exit(self):
        self.assertEqual(-1, self.sut.run('EXIT'))

    def test_run_help(self):
        self.mk_basic.help.return_value = 'ret'
        self.assertEqual(0, self.sut.run('HELP'))
        self.assertEqual(1, self.mk_basic.help.call_count)

    def test_run_read(self):
        self.mk_basic.read.return_value = 'return read value'
        self.sut.run('READ ADDR')
        self.assertEqual(1, self.mk_basic.read.call_count)

    def test_run_write(self):
        self.sut.run('WRITE ADDR VALUE')
        self.assertEqual(1, self.mk_basic.write.call_count)

    def test_run_fullread(self):
        self.mk_basic.full_read.return_value = 'full read'
        self.sut.run('FULLREAD')
        self.assertEqual(1, self.mk_basic.full_read.call_count)

    def test_run_fullwrite(self):
        self.sut.run('FULLWRITE VALUE')
        self.assertEqual(1, self.mk_basic.full_write.call_count)

    def test_run_testapp1(self):
        self.sut.run('TESTAPP1')
        self.assertEqual(1, self.mk_test_app_1.run.call_count)

    def test_run_testapp2(self):
        self.sut.run('TESTAPP2')
        self.assertEqual(1, self.mk_test_app_2.run.call_count)
