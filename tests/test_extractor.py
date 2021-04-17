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

    def test_default_config_with_unseparated_tickers(self):
        text = "Comparing FNGU vs $WEBL vs SOXL- who wins? And what about $cldl vs $Skyu? BTW, will the $w+$Z pair still grow? IMHO, SOXL is king!"
        expected = ["FNGU", "WEBL", "SOXL", "CLDL", "SKYU", "W", "Z"]
        extracted = self.default_ticker_extractor.extract(text)
        self.assertEqual(expected, extracted)

    def test_default_config_with_separated_tickers(self):
        text = "Which of BTC-USD, $ETH-USD and $ada-usd is best? What about $Brk.a and $Brk.B? BRK-B is cheaper. Let's also pick between futures MGC=F and ALI=F."
        expected = ["BTC-USD", "ETH-USD", "ADA-USD", "BRK.A", "BRK.B", "BRK-B", "MGC=F", "ALI=F"]
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

    def test_blacklist(self):
        self.assertNotIn("BLCN", reticker.config.BLACKLIST)
        self.assertNotIn("BLOK", reticker.config.BLACKLIST)
        text = "BLCN, BLOK or DAPP?"
        self.assertEqual(self.default_ticker_extractor.extract(text), ["BLCN", "BLOK", "DAPP"])

        original_blacklist = reticker.config.BLACKLIST.copy()
        reticker.config.BLACKLIST.add("BLCN")
        reticker.config.BLACKLIST.add("BLOK")
        self.assertEqual(self.default_ticker_extractor.extract(text), ["DAPP"])

        reticker.config.BLACKLIST.remove("BLOK")
        self.assertEqual(self.default_ticker_extractor.extract(text), ["BLOK", "DAPP"])

        reticker.config.BLACKLIST.remove("BLCN")
        self.assertEqual(reticker.config.BLACKLIST, original_blacklist)

    def test_mapping(self):
        self.assertNotIn("BTC", reticker.config.MAPPING)
        text = "ADA BTC RIOT"
        self.assertEqual(self.default_ticker_extractor.extract(text), ["ADA", "BTC", "RIOT"])

        original_mapping = reticker.config.MAPPING.copy()
        reticker.config.MAPPING["ADA"] = "ADA-USD"
        reticker.config.MAPPING["BTC"] = "BTC-USD"
        self.assertEqual(self.default_ticker_extractor.extract(text), ["ADA-USD", "BTC-USD", "RIOT"])

        del reticker.config.MAPPING["ADA"]
        self.assertEqual(self.default_ticker_extractor.extract(text), ["ADA", "BTC-USD", "RIOT"])
        self.assertEqual(self.default_ticker_extractor.extract(f"{text} BTC-USD"), ["ADA", "BTC-USD", "RIOT"])

        del reticker.config.MAPPING["BTC"]
        self.assertEqual(reticker.config.MAPPING, original_mapping)


class TestCustomExtraction(unittest.TestCase):
    def test_prefixed_uppercase(self):
        self.assertEqual(reticker.TickerExtractor().extract("$ARKX"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("$ARKX"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_uppercase=True)).extract("$ARKX"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_uppercase=False)).extract("$ARKX"), [])

    def test_unprefixed_uppercase(self):
        self.assertEqual(reticker.TickerExtractor().extract("ARKX"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("ARKX"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(unprefixed_uppercase=True)).extract("ARKX"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(unprefixed_uppercase=False)).extract("ARKX"), [])

    def test_prefixed_lowercase(self):
        self.assertEqual(reticker.TickerExtractor().extract("$arkx"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("$arkx"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_lowercase=True)).extract("$arkx"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_lowercase=False)).extract("$arkx"), [])

    def test_prefixed_titlecase(self):
        self.assertEqual(reticker.TickerExtractor().extract("$Arkx"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("$Arkx"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_titlecase=True)).extract("$Arkx"), ["ARKX"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(prefixed_titlecase=False)).extract("$Arkx"), [])

    def test_separators(self):
        self.assertEqual(reticker.TickerExtractor().extract("BTC-USD"), ["BTC-USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig()).extract("BTC-USD"), ["BTC-USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators="-")).extract("BTC-USD"), ["BTC-USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators=".")).extract("BTC-USD"), ["BTC", "USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators="=")).extract("BTC-USD"), ["BTC", "USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators=None)).extract("BTC-USD"), ["BTC", "USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators="")).extract("BTC-USD"), ["BTC", "USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators=".-")).extract("BTC-USD"), ["BTC-USD"])
        self.assertEqual(reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators=".=")).extract("BTC-USD"), ["BTC", "USD"])
