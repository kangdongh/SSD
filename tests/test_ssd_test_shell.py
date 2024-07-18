import io
import sys
from unittest import TestCase
from unittest.mock import Mock

from app.return_code import ReturnCode
from app.shell_api import ShellAPI
from app.ssd_test_shell import SSDTestShell


class TestSSDTestShell(TestCase):
    def setUp(self):
        self.api = Mock(spec=ShellAPI)
        self.sut = SSDTestShell(self.api)

    def test_check_valid_cmd_length(self):
        valid_cmds = ["help", "HELP", "help 1234"]
        for cmd in valid_cmds:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.SUCCESS)

    def test_check_invalid_cmd_length(self):
        invalid_cmds = ["read", "write", "fullwrite", "fullread 3", "write 3 4 6"]
        for cmd in invalid_cmds:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.FAILURE)

    def test_check_valid_cmd(self):
        valid_cmds = ["read 1", "write 1 0xAAAAAAAA", "Help", "FullRead",
                      "FullWrite 0xAAAAAAAA"]
        for cmd in valid_cmds:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.SUCCESS)

    def test_check_invalid_cmd(self):
        invalid_cmds = ["cmd1", "readwrite", "full_read", "full-write 1 0xAAAAAAA", "writing",
                        "reading"]
        for cmd in invalid_cmds:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.FAILURE)

    def test_check_valid_address(self):
        valid_addresses = ["read 0"]
        for cmd in valid_addresses:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.SUCCESS)

    def test_check_invalid_address(self):
        invalid_addresses = ["read 101", "read -2"]
        for cmd in invalid_addresses:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.FAILURE)

    def test_check_valid_value(self):
        valid_values = ["write 3 0xAAAAAAAA", "write 3 0xA0AA1AAA", "fullwrite 0xAABBAAAA",
                        "fullwrite 0x00000000"]
        for cmd in valid_values:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.SUCCESS)

    def test_check_invalid_value(self):
        invalid_values = [
            "write 3 0xAAAAAAAZ", "fullwrite 3 0xNAAAAAAZ", "write 3 0xAA",
            "write 3 0xAA__", "write 3 0xAA1", "write 3 0xAA123243421"
        ]
        for cmd in invalid_values:
            with self.subTest(f"cmd={cmd}"):
                self.assertEqual(self.sut.run(cmd), ReturnCode.FAILURE)

    def test_run_exit(self):
        self.assertEqual(ReturnCode.EXIT, self.sut.run('EXIT'))

    def test_run_read(self):
        self.sut.run('READ 0')
        self.api.read.assert_called_once_with(0)

    def test_run_read_print(self):
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.api.read.return_value = 'ret'
        self.sut.run('READ 0')

        self.assertEqual(captured_output.getvalue().strip(), "ret")

    def test_run_write(self):
        self.sut.run('WRITE 0 0x00000000')
        self.api.write.assert_called_once_with(0, '0x00000000')

    def test_run_fullread(self):
        self.sut.run('FULLRead')
        self.assertEqual(self.api.read.call_count, 100)

    def test_run_fullwrite(self):
        self.api.read.return_value = ''
        self.sut.run('FULLWRITE 0x00000000')
        self.assertEqual(self.api.write.call_count, 100)