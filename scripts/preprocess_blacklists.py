"""Uppercase, deduplicate, and sort the blacklist."""
from reticker.config import BLACKLIST_PATHS

for path in BLACKLIST_PATHS:
    blacklist = path.read_text().strip().split("\n")
    blacklist = [stripped_term.upper() for term in blacklist if (stripped_term := term.strip())]  # pylint: disable=used-before-assignment
    blacklist = sorted(set(blacklist))
    path.write_text("\n".join(blacklist))
