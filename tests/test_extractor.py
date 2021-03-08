"""Test extractor."""
# pylint: disable=missing-class-docstring,missing-function-docstring
import re
import unittest

import reticker


class TestExtraction(unittest.TestCase):
    def setUp(self) -> None:
        self.default_ticker_extractor = reticker.TickerExtractor()

    def test_pattern_type(self):
        self.assertIsInstance(self.default_ticker_extractor.pattern, re.Pattern)

    def test_default_config(self):
        text = "Comparing FNGU vs $WEBL vs SOXL- who wins? And what about $cldl vs $Skyu? BTW, will the $w+$Z pair still grow? IMHO, SOXL is king!"
        expected = ["FNGU", "WEBL", "SOXL", "CLDL", "SKYU", "W", "Z"]
        extracted = self.default_ticker_extractor.extract(text)
        self.assertEqual(expected, extracted)

    def test_no_matches(self):
        self.assertEqual(self.default_ticker_extractor.extract("Test text"), [])
        self.assertEqual(self.default_ticker_extractor.extract(""), [])

    def test_deduplicate(self):
        text = "SPY is not QQQ. It is SPY."
        self.assertEqual(reticker.TickerExtractor().extract(text), ["SPY", "QQQ"])
        self.assertEqual(reticker.TickerExtractor(deduplicate=True).extract(text), ["SPY", "QQQ"])
        self.assertEqual(reticker.TickerExtractor(deduplicate=False).extract(text), ["SPY", "QQQ", "SPY"])

    def test_custom_config(self):
        assert "WEBL" not in reticker.BLACKLIST
        assert "TECL" not in reticker.BLACKLIST

        self.assertEqual(reticker.TickerExtractor().extract("WEBL $TECL"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(unprefixed_uppercase=True)).extract("WEBL $TECL"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(unprefixed_uppercase=False)).extract("WEBL $TECL"), ["TECL"])

        self.assertEqual(reticker.TickerExtractor().extract("WEBL $tecl"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("WEBL $tecl"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_lowercase=True)).extract("WEBL $tecl"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_lowercase=False)).extract("WEBL $tecl"), ["WEBL"])

        self.assertEqual(reticker.TickerExtractor().extract("WEBL $Tecl"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("WEBL $Tecl"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_titlecase=True)).extract("WEBL $Tecl"), ["WEBL", "TECL"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_titlecase=False)).extract("WEBL $Tecl"), ["WEBL"])
