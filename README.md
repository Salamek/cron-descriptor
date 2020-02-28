# Cron Descriptor

Master: [![Master Build Status](https://api.travis-ci.org/Salamek/cron-descriptor.svg?branch=master)](https://travis-ci.org/Salamek/cron-descriptor) All: [![Build Status](https://api.travis-ci.org/Salamek/cron-descriptor.svg)](https://travis-ci.org/Salamek/cron-descriptor)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/salamek)

A Python library that converts cron expressions into human readable strings. Ported to Python from https://github.com/bradyholt/cron-expression-descriptor.

**Author**: Adam Schubert (https://www.salamek.cz)  
**Original Author & Credit**: Brady Holt (http://www.geekytidbits.com)  
**License**: [MIT](http://opensource.org/licenses/MIT)

## Features         
 * Supports all cron expression special characters including * / , - ? L W, #
 * Supports 5, 6 (w/ seconds or year), or 7 (w/ seconds and year) part cron expressions
 * Provides casing options (Sentence, Title, Lower, etc.)
 * Localization with support for 14 languages
 * Supports Python 2.7 - 3.7

## Installation
Using PIP
```bash
pip install cron-descriptor
```

## Usage example

```python
# Simple
from cron_descriptor import get_description, ExpressionDescriptor

print(get_description("* 2 3 * *"))

#OR

print(str(ExpressionDescriptor("* 2 3 * *")))
```

```python
# Advanced
# Consult Options.py/CasingTypeEnum.py/DescriptionTypeEnum.py for more info
from cron_descriptor import Options, CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor

descripter = ExpressionDescriptor("*/10 * * * *", throw_exception_on_parse_error = True, casing_type = CasingTypeEnum.Sentence, use_24hour_time_format = True)
# GetDescription uses DescriptionTypeEnum.FULL by default:
print(descripter.get_description())
print("{}".format(descripter))

#or passing Options class as second argument:

options = Options()
options.throw_exception_on_parse_error = True
options.casing_type = CasingTypeEnum.Sentence
options.use_24hour_time_format = True
descripter = ExpressionDescriptor("*/10 * * * *", options)
print(descripter.get_description(DescriptionTypeEnum.FULL))

```

## Languages Available

|Language| locale_code | contributor |
|--------|-------------|-------------|
|English |en|[Brady Holt](https://github.com/bradyholt)|
|Brazilian |pt_PT|[Renato Lima](https://github.com/natenho)|
|Chinese Simplified | zh_CN |[Star Peng](https://github.com/starpeng)|
|Spanish |es_ES|[Ivan Santos](https://github.com/ivansg)|
|Norwegian |nb_NO|[Siarhei Khalipski](https://github.com/KhalipskiSiarhei)|
|Turkish |tr_TR|[Mustafa SADEDİL](https://github.com/sadedil)|
|Dutch |nl_NL|[TotalMace](https://github.com/TotalMace)|
|Russian |ru_RU|[LbISS](https://github.com/LbISS)|
|French |fr_FR|[Arnaud TAMAILLON](https://github.com/Greybird)|
|German |de_DE|[Michael Schuler](https://github.com/mschuler)|
|Ukrainian |uk_UA|[Taras](https://github.com/tbudurovych)|
|Italian |it_IT|[rinaldihno](https://github.com/rinaldihno)|
|Czech |cs_CZ|[Adam Schubert](https://github.com/salamek)|
|Swedish |sv_SE|[Åke Engelbrektson](https://github.com/eson57)|

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
cron-descriptor is using [Gettext](https://www.gnu.org/software/gettext/) for translations.

> To create new translation or edit existing one, i suggest using [Poedit](https://poedit.net/).

You can copy/rename and translate any file from `locale` directory:
```bash
cp ./cron_descriptor/locale/de_DE.po ./cron_descriptor/locale/YOUR_LOCALE_CODE.po
poedit ./cron_descriptor/locale/YOUR_LOCALE_CODE.po
```
or you can generate new untranslated *.po file from sources by running in `cron_descriptor` directory:
```bash
cd cron_descriptor
xgettext *.py -o locale/YOUR_LOCALE_CODE.po
```

Generating *.mo file from *.po file. In root directory run command:
```bash
msgfmt -o cron_descriptor/locale/YOUR_LOCALE_CODE.mo cron_descriptor/locale/YOUR_LOCALE_CODE.po
```

## Developing

All suggescions and PR's are welcomed

Just clone this repository and register pre-commit hook by running:

```bash
ln -s ../../pre-commit.sh .git/hooks/pre-commit
```

Then install dev requirements:

```bash
pip install pep8
pip install flake8
pip install pep8-naming
```
