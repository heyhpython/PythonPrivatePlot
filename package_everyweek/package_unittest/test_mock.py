# coding=utf-8
# builtins
import unittest
from unittest.mock import Mock
# third party package
# self built


class Count:
    def add(self, a, b):
        return a + b


class TestCount(unittest.TestCase):
    def test_add(self):
        count = Count()
        count.add = Mock(return_value=13, side_effect=count.add)
        result = count.add(8, 5)
        print(result)
        count.add.assert_called_with(8, 5)
        self.assertEqual(result, 13)


if __name__ == "__main__":
    unittest.main()