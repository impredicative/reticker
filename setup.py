"""Package installation setup."""
import os
import re
from pathlib import Path
from typing import Match, cast

from setuptools import find_packages, setup

_DIR = Path(__file__).parent
_PACKAGE_NAME = "reticker"

setup(
    name=_PACKAGE_NAME,
    author="Ouroboros Chrysopoeia",
    author_email="impredicative@users.noreply.github.com",
    version=cast(Match, re.fullmatch(r"refs/tags/v?(?P<ver>\S+)", os.environ["GITHUB_REF"]))["ver"],  # Ex: GITHUB_REF="refs/tags/1.2.3"; version="1.2.3"
    description="Use a regular expression to extract US style stock tickers from text",
    keywords="regex regexp stock text ticker",
    long_description=(_DIR / "README.md").read_text().strip(),
    long_description_content_type="text/markdown",
    url="https://github.com/impredicative/reticker/",
    packages=find_packages(exclude=["scripts"]),
    package_data={_PACKAGE_NAME: ["config/blacklist/*.txt"]},
    python_requires=">=3.8",
    classifiers=[  # https://pypi.org/classifiers/
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
    ],
)
