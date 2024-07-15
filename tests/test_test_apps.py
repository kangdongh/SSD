from unittest import TestCase
from unittest.mock import MagicMock

from app.basic_logic import BasicLogic
from app.test_app.test_app_1 import TestApp1
from app.test_app.test_app_2 import TestApp2


class TestTestApps(TestCase):
    def test_testapp1_is_called(self):
        mock_basic_logic = MagicMock(spec=BasicLogic)
        mock_basic_logic.full_read.return_value = "0xABCDFFFF"
        test_app = TestApp1()
        test_app.run(mock_basic_logic)
        mock_basic_logic.full_read.assert_called_once()
        mock_basic_logic.full_write.assert_called_once()

    def test_testapp1_is_correct(self):
        mock_basic_logic = MagicMock(spec=BasicLogic)
        mock_basic_logic.full_read.return_value = "0xABCDFFFF"
        test_app = TestApp1()
        self.assertEqual(test_app.run(mock_basic_logic), True)

    def test_testapp2_is_called(self):
        mock_basic_logic = MagicMock(spec=BasicLogic)
        mock_basic_logic.write.return_value = [0xAAAABBBB] * 150 + [0x12345678] * 5
        mock_basic_logic.read.return_value = "0x12345678"
        test_app = TestApp2()
        test_app.run(mock_basic_logic)
        self.assertEqual(mock_basic_logic.read.call_count, 5)
        self.assertEqual(mock_basic_logic.write.call_count, 155)

    def test_testapp2_is_correct(self):
        mock_basic_logic = MagicMock(spec=BasicLogic)
        mock_basic_logic.read.return_value = "0x12345678"
        test_app = TestApp2()
        self.assertEqual(test_app.run(mock_basic_logic), True)

