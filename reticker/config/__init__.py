"""Package config."""
from pathlib import Path
from typing import Final, Set

_CONFIG_PATH: Final[Path] = Path(__file__).parent
BLACKLIST_PATH: Final[Path] = _CONFIG_PATH / "blacklist.txt"
BLACKLIST: Set[str] = set(BLACKLIST_PATH.read_text().strip().split("\n"))
