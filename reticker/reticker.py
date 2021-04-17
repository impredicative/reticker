"""Package implementation."""
import functools
import re
from typing import List, Optional, Pattern

from . import config


class TickerMatchConfig:
    """Ticker match configuration."""

    def __init__(
        self,
        *,
        prefixed_uppercase: bool = True,
        unprefixed_uppercase: bool = True,
        prefixed_lowercase: bool = True,
        prefixed_titlecase: bool = True,
        separators: Optional[str] = ".-="
    ):
        """Return configuration for matching tickers.

        :param prefixed_uppercase: Match prefixed uppercase, e.g. $SPY
        :param unprefixed_uppercase: Match unprefixed uppercase, e.g. SPY
        :param prefixed_lowercase: Match prefixed lowercase, e.g. $spy
        :param prefixed_titlecase: Match prefixed titlecase, e.g. $Spy
        :param separators: Match two parts separated by one of the separators, e.g. BRK.A, BRK-B, MGC=F
        """
        assert any([prefixed_uppercase, unprefixed_uppercase, prefixed_lowercase, prefixed_titlecase])
        self.prefixed_uppercase = prefixed_uppercase
        self.unprefixed_uppercase = unprefixed_uppercase
        self.prefixed_lowercase = prefixed_lowercase
        self.prefixed_titlecase = prefixed_titlecase

        separators = separators or ""
        assert " " not in separators
        assert "$" not in separators
        assert len(separators) == len(set(separators))
        self.separators = separators


class TickerExtractor:
    """Ticker extractor."""

    def __init__(self, *, deduplicate: bool = True, match_config: Optional[TickerMatchConfig] = None) -> None:
        """Return the ticker extractor.

        :param deduplicate: Deduplicate the results.
        :param match_config: Optional match configuration.
        """
        self.deduplicate = deduplicate
        self.match_config = match_config or TickerMatchConfig()

    @functools.cached_property
    def pattern(self) -> Pattern:
        """Return the regular expression pattern to find possible tickers.

        This does not use the blacklist.
        """
        match_config = self.match_config
        pattern_format = r"\b{pattern}\b"
        pos_prefix, neg_prefix = r"(?<=\$)", r"(?<!\$)"
        separable = bool(match_config.separators)
        separator = "[" + re.escape(match_config.separators) + "]"
        # separator = "(?:" + "|".join(map(re.escape, match_config.separators)) + ")"  # Alt technique.
        patterns = []

        def append_patterns(part1: str, part2: str) -> None:
            if separable:
                patterns.append(part1 + separator + part2)
            patterns.append(part1)

        if match_config.prefixed_uppercase:
            append_patterns(pos_prefix + r"[A-Z]{1,6}", r"[A-Z]{1,3}")
        if match_config.unprefixed_uppercase:
            append_patterns(neg_prefix + r"[A-Z]{2,6}", r"[A-Z]{1,3}")
        if match_config.prefixed_lowercase:
            append_patterns(pos_prefix + r"[a-z]{1,6}", r"[a-z]{1,3}")
        if match_config.prefixed_titlecase:
            append_patterns(pos_prefix + r"[A-Z]{1}[a-z]{2,5}", r"[A-Za-z]{1}[a-z]{0,2}")

        # Join patterns
        patterns = [pattern_format.format(pattern=pattern) for pattern in patterns]
        pattern = re.compile("|".join(patterns), flags=re.ASCII)
        return pattern

    def extract(self, text: str) -> List[str]:
        """Return possible tickers extracted from the given text."""
        matches = [match.upper() for match in self.pattern.findall(text)]
        matches = [match for match in matches if match not in config.BLACKLIST]  # Is done _before_ 'mapping'.
        matches = [config.MAPPING.get(match, match) for match in matches]
        if self.deduplicate:
            matches = list(dict.fromkeys(matches))  # Is done _after_ 'mapping'.
        return matches
