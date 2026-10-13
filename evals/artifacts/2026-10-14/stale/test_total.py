import unittest
from total import total
class TotalTests(unittest.TestCase):
    def test_total(self): self.assertEqual(total([2, 3]), 5)
