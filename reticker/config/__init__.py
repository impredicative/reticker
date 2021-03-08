"""Package config."""
from pathlib import Path
from typing import Final, Set

_CONFIG_PATH: Final[Path] = Path(__file__).parent
BLACKLIST_PATHS: Final[list[Path]] = list((_CONFIG_PATH / "blacklist").glob("*.txt"))
BLACKLIST: Set[str] = set(term for path in BLACKLIST_PATHS for term in path.read_text().strip().split("\n"))
