# reticker
**reticker** uses Python 3.8 to extract snippets which could be US-style stock tickers from the given text extracted using a regular expression.
It does not however validate or use a whitelist of such tickers.

[![cicd badge](https://github.com/impredicative/reticker/workflows/cicd/badge.svg?branch=master)](https://github.com/impredicative/reticker/actions?query=workflow%3Acicd+branch%3Amaster)

## Example:
```python
>>> reticker.TickerExtractor().extract("Comparing FNGU vs $WEBL vs SOXL- who wins? And what about $cldl vs $Skyu? BTW, will the $w+$Z pair still grow? IMHO, SOXL is king!")
["FNGU", "WEBL", "SOXL", "CLDL", "SKYU", "W", "Z"]
```

## Features
* Optional matching of unprefixed uppercase, prefixed lowercase, and prefixed titlecase tickers is enabled by default, but can individually be disabled.
* The results are in the order they are first found.
* The results are deduplicated by default, although this can be disabled.
* A configurable blacklist is used.
* For lower level use, a compiled regular expression can be accessed.

## Links
* Code: https://github.com/impredicative/reticker/
* Release: https://pypi.org/project/reticker/
* Changelog: https://github.com/impredicative/reticker/releases

## Installation
Python ≥3.8 is required.

To install the package, run:

    pip install reticker

