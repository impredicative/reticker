# reticker
**reticker** uses Python 3.8 to extract what look like US-style stock tickers from the given text. It uses a configurably created regular expression.
It does not however validate or use a whitelist of tickers.

[![cicd badge](https://github.com/impredicative/reticker/workflows/cicd/badge.svg?branch=master)](https://github.com/impredicative/reticker/actions?query=workflow%3Acicd+branch%3Amaster)

## Example
```python
>>> import reticker
>>> reticker.TickerExtractor().extract("Comparing FNGU vs $WEBL vs SOXL- who wins? And what about $cldl vs $Skyu? IMHO, SOXL is king!\nBTW, will the $w+$Z pair still grow?")
["FNGU", "WEBL", "SOXL", "CLDL", "SKYU", "W", "Z"]
```

## Features
* Optional matching of unprefixed uppercase, prefixed lowercase, and prefixed titlecase tickers is enabled by default, but can individually be disabled.
* The results are in the order they are first found.
* By default, the results are deduplicated, although this can be disabled.
* A configurable blacklist of common false-positives is used.
* For lower level use, a configurably created compiled regular expression can be accessed.

## Links
| Caption   | Link                                               |
|-----------|----------------------------------------------------|
| Code      | https://github.com/impredicative/reticker/         |
| Changelog | https://github.com/impredicative/reticker/releases |
| Release   | https://pypi.org/project/reticker/                 |

## Installation
Python ≥3.8 is required. To install, run:

    pip install reticker

## Usage

### Default usage
```python
>>> import reticker
>>> extractor = reticker.TickerExtractor()

>>> type(extractor.pattern)
<class 're.Pattern'>

>>> extractor.extract("Has $GLD/IAU bottomed yet? What's the prospect for gold miners like $nugt?")
['GLD', 'IAU', 'NUGT']
```

### Customized usage
```python
>>> import reticker
>>> reticker.BLACKLIST.add("DOGE")
>>> reticker.BLACKLIST.remove("CNN")
>>> ticker_match_config = reticker.TickerMatchConfig(unprefixed_uppercase=False, prefixed_lowercase=False, prefixed_titlecase=False)
>>> extractor = reticker.TickerExtractor(deduplicate=False, match_config=ticker_match_config)

>>> type(extractor.pattern)
<class 're.Pattern'>

>>> extractor.extract("The ARKs, e.g. $ARKG/$ARKK/$ARKQ had been struggling but I feel they will all rise again, especially $ARKK.")
['ARKG', 'ARKK', 'ARKQ', 'ARKK']
```
