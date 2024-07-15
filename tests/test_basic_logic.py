import unittest
from unittest import TestCase, skip

from app.basic_logic import BasicLogic


class TestBasicLogic(TestCase):

    def setUp(self):
        self.sut = BasicLogic("test_basic_logic")

    def test_read(self):
        pass

    def test_write(self):
        pass

    def test_full_read(self):
        pass

    def test_full_write(self):
        pass

    def test_exit(self):
        self.assertEqual(self.sut.exit(), True)

    def test_help(self):
        self.assertIsNotNone(self.sut.help())

    @skip
    def test_test_app1(self):
        pass

    @skip
    def test_test_app2(self):
        pass


if __name__ == '__main__':
    unittest.main()
