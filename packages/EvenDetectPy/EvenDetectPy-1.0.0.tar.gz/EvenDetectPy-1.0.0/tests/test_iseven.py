import unittest
from evendetect import is_even

class TestIsEven(unittest.TestCase):
    def test_is_even(self):
        self.assertTrue(is_even(2))
        self.assertFalse(is_even(3))
        self.assertTrue(is_even(0))

    def test_is_even_with_string(self):
        self.assertTrue(is_even("2"))
        self.assertFalse(is_even("3"))
        self.assertTrue(is_even("0"))

    def test_is_even_with_float(self):
        self.assertFalse(is_even(3.0))
        self.assertFalse(is_even(1.0293029309203923020))

    def test_is_even_with_none(self):
        self.assertFalse(is_even(None))
    
    def test_is_even_with_bool(self):
        self.assertFalse(is_even(True))

    def test_is_even_with_tuple(self):
        self.assertFalse(is_even((2,)))
        self.assertFalse(is_even((3,)))
        self.assertFalse(is_even((0,)))
    
    def test_is_even_with_set(self):
        self.assertFalse(is_even({2}))
        self.assertFalse(is_even({3}))

    def test_is_even_with_complex(self):
        self.assertFalse(is_even(2+0j))
        self.assertFalse(is_even(3+0j))
