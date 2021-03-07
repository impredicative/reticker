import re
import unittest

import reticker


class TestPattern(unittest.TestCase):
    def test_default_config(self):
        expected = re.compile("\\b(?<=\\$)[A-Z]{1,6}\\b|\\b(?<!\\$)[A-Z]{2,6}\\b|\\b(?<=\\$)[a-z]{1,6}\\b|\\b(?<=\\$)[A-Z]{1}[a-z]{2,5}\\b", re.ASCII)
        actual = reticker.TickerExtractor().pattern
        self.assertEqual(expected, actual)


class TestExtraction(unittest.TestCase):
    def test_default_config(self):
        text = "Comparing FNGU vs $SOXL- who wins? And what about $Fngu vs $webl? BTW, will the $w+$Z pair still grow?"
        expected = ["FNGU", "SOXL", "WEBL", "W", "Z"]
        extracted = reticker.TickerExtractor().extract(text)
        self.assertEqual(expected, extracted)
