from reticker.config import BLACKLIST, BLACKLIST_PATH

BLACKLIST_PATH.write_text("\n".join(sorted(set(map(str.upper, BLACKLIST)))))
