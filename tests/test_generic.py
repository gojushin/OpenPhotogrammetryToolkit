import unittest

class SimpleTest(unittest.TestCase):
    def test(self):
        self.assertEqual("success", "success")  # Will always pass. Just a baseline.

# Running the test case
unittest.main(argv=[''], exit=False)