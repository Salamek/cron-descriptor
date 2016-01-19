# Cron Descriptor

Master: [![Master Build Status](https://api.travis-ci.org/Salamek/cron-descriptor.svg?branch=master)](https://travis-ci.org/Salamek/cron-descriptor) All: [![Build Status](https://api.travis-ci.org/Salamek/cron-descriptor.svg)](https://travis-ci.org/Salamek/cron-descriptor)

A Python library that converts cron expressions into human readable strings. Ported to Python from https://github.com/bradyholt/cron-expression-descriptor.

**Author**: Adam Schubert (https://www.salamek.cz)  
**Original Author & Credit**: Brady Holt (http://www.geekytidbits.com)  
**License**: [MIT](http://opensource.org/licenses/MIT)

## Features         
 * Supports all cron expression special characters including * / , - ? L W, #
 * Supports 5, 6 (w/ seconds or year), or 7 (w/ seconds and year) part cron expressions
 * Provides casing options (Sentence, Title, Lower, etc.)
 * Localization with support for 13 languages
 * Supports Python 2.7 - 3.4

## Installation
Using PIP
```bash
pip install cron-descriptor
```

## Usage example

```python
# Simple
from cron_descriptor import GetDescription, ExpressionDescriptor

print(GetDescription("* 2 3 * *"))

#OR

print(str(ExpressionDescriptor("* 2 3 * *")))
```

```python
# Advanced
# Consult Options.py/CasingTypeEnum.py/DescriptionTypeEnum.py for more info
from cron_descriptor import Options, CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor

descripter = ExpressionDescriptor("*/10 * * * *", ThrowExceptionOnParseError = True, CasingType = CasingTypeEnum.Sentence, Use24HourTimeFormat = True)
# GetDescription uses DescriptionTypeEnum.FULL by default:
print(descripter.GetDescription())
print("{}".format(descripter))

#or passing Options class as second argument:

options = Options()
options.ThrowExceptionOnParseError = True
options.CasingType = CasingTypeEnum.Sentence
options.Use24HourTimeFormat = True
descripter = ExpressionDescriptor("*/10 * * * *", options)
print(descripter.GetDescription(DescriptionTypeEnum.FULL))

```

## Languages Available
  * English ([Brady Holt](https://github.com/bradyholt))
  * Brazilian ([Renato Lima](https://github.com/natenho))
  * Spanish ([Ivan Santos](https://github.com/ivansg))
  * Norwegian ([Siarhei Khalipski](https://github.com/KhalipskiSiarhei))
  * Turkish ([Mustafa SADEDİL](https://github.com/sadedil))
  * Dutch ([TotalMace](https://github.com/TotalMace))
  * Chinese Simplified ([Star Peng](https://github.com/starpeng))
  * Russian ([LbISS](https://github.com/LbISS))
  * French ([Arnaud TAMAILLON](https://github.com/Greybird))
  * German ([Michael Schuler](https://github.com/mschuler))
  * Ukrainian ([Taras](https://github.com/tbudurovych))
  * Italian ([rinaldihno](https://github.com/rinaldihno))
  * Czech ([Adam Schubert](https://github.com/salamek))

<!-- SOON
## Demo



## Download

-->

## Original Source
 - .NET - [https://github.com/bradyholt/cron-expression-descriptor](https://github.com/bradyholt/cron-expression-descriptor)

## Ports
 - Java - [https://github.com/RedHogs/cron-parser](https://github.com/RedHogs/cron-parser)
 - Ruby - [https://github.com/alpinweis/cronex](https://github.com/alpinweis/cronex)

## Running Unit Tests

```bash
python setup.py test
```

## Translating
cron-descriptor is using [Gettext](https://www.gnu.org/software/gettext/) for translations
For creating new translations or editing existing ones, please install [Poedit](https://poedit.net/)

You can copy/rename and translate any file from `locale` directory:
```bash
mv ./locale/de_DE.po ./locale/YOUR_LOCALE_CODE.po
poedit ./locale/YOUR_LOCALE_CODE.po
```
or you can generate new empty *.po file from sources by running:
```bash
xgettext *.py
```
in `cron_descriptor` directory

## Developing

All suggescions and PR's are welcomed

Just clone this repository and register pre-commit hook by running:

```bash
ln -s ../../pre-commit.sh .git/hooks/pre-commit
```
