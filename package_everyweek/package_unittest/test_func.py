# coding=utf-8
# builtins
import unittest
from unittest.mock import Mock, patch
# third party package
# self built
from package_everyweek.package_unittest.function import add_and_multiply


class TestFun(unittest.TestCase):

    def test_add_and_multi(self):
        x = 3
        y = 5
        addition, multiple = add_and_multiply(x, y)
        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)

    @patch('package_everyweek.package_unittest.function.multiply')
    def test_add_and_multi_2(self, mock_multiply):
        # mock掉依赖的问题
        x = 3
        y = 5
        mock_multiply.return_value = 15
        addition, multiple = add_and_multiply(x, y)

        mock_multiply.assert_called_once_with(3, 5)
        self.assertEqual(8, addition)
        self.assertEqual(15, multiple)


if __name__ == "__main__":
    unittest.main()