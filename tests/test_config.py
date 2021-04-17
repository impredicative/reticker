"""Test package config."""
# pylint: disable=missing-class-docstring,missing-function-docstring
import unittest

import reticker


class TestConfig(unittest.TestCase):
    def test_blacklist_contents(self):
        blacklist = reticker.config.BLACKLIST
        self.assertIsInstance(blacklist, set)
        self.assertTrue(blacklist)
        for entry in blacklist:
            self.assertIsInstance(entry, str)
            self.assertTrue(entry)
            self.assertEqual(entry.strip().upper(), entry)
