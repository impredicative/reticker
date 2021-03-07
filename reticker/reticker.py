"""Package implementation."""
import functools
import re
from typing import List, Optional, Pattern, Set

from . import config


class TickerMatchConfig:
    """Ticker match configuration."""

    def __init__(self, *, unprefixed_uppercase: bool = True, prefixed_lowercase: bool = True, prefixed_titlecase: bool = True):
        """Return the ticker matching configuration.

        Note that a prefixed uppercase ticker, e.g. $SPY, is always matched.

        :param unprefixed_uppercase: Match SPY.
        :param prefixed_lowercase: Match $spy
        :param prefixed_titlecase: Match $Spy.
        """
        self.unprefixed_uppercase = unprefixed_uppercase
        self.prefixed_lowercase = prefixed_lowercase
        self.prefixed_titlecase = prefixed_titlecase


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
        patterns = [pos_prefix + r"[A-Z]{1,6}"]  # Match prefixed uppercase.

        if match_config.unprefixed_uppercase:
            patterns.append(neg_prefix + r"[A-Z]{2,6}")
        if match_config.prefixed_lowercase:
            patterns.append(pos_prefix + r"[a-z]{1,6}")
        if match_config.prefixed_titlecase:
            patterns.append(pos_prefix + r"[A-Z]{1}[a-z]{2,5}")

        patterns = [pattern_format.format(pattern=pattern) for pattern in patterns]
        pattern = re.compile("|".join(patterns), flags=re.ASCII)
        return pattern

    def extract(self, text: str) -> List[str]:
        """Return possible tickers extracted from the given text."""
        blacklist: Set[str] = config.BLACKLIST or set()
        matches = [match.upper() for match in self.pattern.findall(text)]
        if self.deduplicate:
            matches = list(dict.fromkeys(matches))
        matches = [match for match in matches if match not in blacklist]
        return matches
