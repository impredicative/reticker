# reticker
**reticker** uses Python 3.8 to extract what look like stock tickers from the given text. It uses a configurably created regular expression.
It does not however validate or use a whitelist of tickers.

[![cicd badge](https://github.com/impredicative/reticker/workflows/cicd/badge.svg?branch=master)](https://github.com/impredicative/reticker/actions?query=workflow%3Acicd+branch%3Amaster)

## Examples
```python
>>> import reticker

>>> reticker.TickerExtractor().extract("Comparing FNGU vs $WEBL vs SOXL- who wins? And what about $cldl vs $Skyu? IMHO, SOXL is king!\nBTW, will the $w+$Z pair still grow?")
['FNGU', 'WEBL', 'SOXL', 'CLDL', 'SKYU', 'W', 'Z']

>>> reticker.TickerExtractor().extract("Which of BTC-USD, $ETH-USD and $ada-usd is best?\nWhat about $Brk.a and $Brk.B? Compare futures MGC=F and SIL=F.")
['BTC-USD', 'ETH-USD', 'ADA-USD', 'BRK.A', 'BRK.B', 'MGC=F', 'SIL=F']
```

## Features
* Optional matching of prefixed uppercase, unprefixed uppercase, prefixed lowercase, and prefixed titlecase tickers is enabled by default, but can individually be disabled.
  At least one of the four must be enabled.
* Two-part tickers are also matched using a customizable set of separator characters.  
* The results are in the order they are first found.
* By default, the results are deduplicated, although this can be disabled.
* A configurable blacklist of common false-positives is used.
* A configurable remapping of specific tickers is supported.
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

>>> extractor.extract("Has $GLD/IAU bottomed yet? What's the prospect for gold miners like $nugt? Maybe check gold futures MGC=F!")
['GLD', 'IAU', 'NUGT', 'MGC=F']
```

### Customized usage
```python
>>> import reticker

# Custom config:
>>> ticker_match_config = reticker.TickerMatchConfig(prefixed_uppercase=True, unprefixed_uppercase=False, prefixed_lowercase=False, prefixed_titlecase=False)
>>> extractor = reticker.TickerExtractor(deduplicate=False, match_config=ticker_match_config)
>>> extractor.extract("Which is better - $BTC or $ADA? I'm not a fan of $doge, and ETH is not competitive.")
['BTC', 'ADA']

# Separators:
>>> reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators="-=")).extract("BTC-USD")
['BTC-USD']
>>> reticker.TickerExtractor(match_config=reticker.TickerMatchConfig(separators="")).extract("BTC-USD")
['BTC', 'USD']

# Blacklist:
>>> reticker.config.BLACKLIST.add("EUR")
>>> reticker.TickerExtractor().extract("EUR isn't a ticker, but URE is one.")
['URE']

# Mapping:
>>> reticker.config.MAPPING["BTC"] = "BTC-USD"
>>> reticker.TickerExtractor().extract("What is the Yahoo Finance symbol for BTC?")
['BTC-USD']
```
