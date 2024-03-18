import numpy as np
from unittest import TestCase
from sargasso import add, sdot, get_eigvals


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
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([4, 5, 6, 7])
        with self.assertRaises(RuntimeError):
            result = sdot(x, y)

    def test_sdot(self):
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([4, 5, 6])
        result = sdot(x, y)
        assert abs(result - np.dot(x, y)) < 1e-6


class TestSsyev(TestCase):
    def test_get_eigvals(self):
        x = np.array(
            [
                [2.0, -1.0, 0.5],
                [-1.0, 1.5, -0.5],
                [0.5, -0.5, 3.0],
            ]
        ).astype(np.float32)
        eigvals = get_eigvals(x.copy())
        eigvals.sort()
        expected = np.linalg.eig(x)[0]
        expected.sort()
        np.testing.assert_allclose(eigvals, expected, atol=1e-4, rtol=1e-4)
