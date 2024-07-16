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
