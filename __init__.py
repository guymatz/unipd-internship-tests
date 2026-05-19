import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

class Test(unittest.TestCase):
    """Setup for tests."""

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#    def __init__(self, poop):
#        # Our global tolerance when checking floats
#        self.tolerance = 3

    # Source - https://stackoverflow.com/a/8312110
    # pylint: disable=invalid-name
    def assertListAlmostEqual(self, list1, list2, tol):
        """Check List of floats are equal within some tolerance"""

        self.assertEqual(len(list1), len(list2))
        for a, b in zip(list1, list2):
            self.assertAlmostEqual(a, b, tol)
