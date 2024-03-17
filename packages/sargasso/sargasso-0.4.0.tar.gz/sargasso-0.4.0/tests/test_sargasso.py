import numpy as np
from unittest import TestCase
from sargasso import add, sdot

class TestAdd(TestCase):
    def test_add(self):
        assert add(1, 2) == 3

class TestSDot(TestCase):
    def test_sdot_non_1d(self):
        x = np.arange(6).reshape((3, 2))
        y = np.array([4, 5, 6, 7])
        with self.assertRaises(RuntimeError):
            result = sdot(x, y)

    def test_sdot_incompatible_sizes(self):
        x = np.array([1., 2., 3.])
        y = np.array([4, 5, 6, 7])
        with self.assertRaises(RuntimeError):
            result = sdot(x, y)
            
    def test_sdot(self):
        x = np.array([1., 2., 3.])
        y = np.array([4, 5, 6])
        result = sdot(x, y)
        assert abs(result - np.dot(x, y)) < 1e-6
   
