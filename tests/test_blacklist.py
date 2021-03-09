"""Test blacklist."""
# pylint: disable=missing-class-docstring,missing-function-docstring
import unittest

import reticker


class TestBlacklist(unittest.TestCase):
    def test_blacklist(self):
        blacklist = reticker.BLACKLIST
        self.assertIsInstance(blacklist, set)
        self.assertTrue(blacklist)
        for entry in blacklist:
            self.assertIsInstance(entry, str)
            self.assertTrue(entry)
            self.assertEqual(entry.strip().upper(), entry)
