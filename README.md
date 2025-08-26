# Cron Descriptor

[![Python tests](https://github.com/Salamek/cron-descriptor/actions/workflows/python-test.yml/badge.svg)](https://github.com/Salamek/cron-descriptor/actions/workflows/python-test.yml)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/salamek)

A Python library that converts cron expressions into human readable strings. Ported to Python from https://github.com/bradyholt/cron-expression-descriptor.

**Author**: Adam Schubert (https://www.salamek.cz)  
**Original Author & Credit**: Brady Holt (http://www.geekytidbits.com)  
**License**: [MIT](http://opensource.org/licenses/MIT)

## Features         
 * Supports all cron expression special characters including * / , - ? L W, #
 * Supports 5, 6 (w/ seconds or year), or 7 (w/ seconds and year) part cron expressions
 * Provides casing options (Sentence, Title, Lower, etc.)
 * Localization with support for ~31 languages
 * Supports Python 3.9 - 3.13

## Installation
Using PIP
```bash
pip install cron-descriptor
```

## Usage example

### Simple
```python
from cron_descriptor import get_description, ExpressionDescriptor

print(get_description("* 2 3 * *"))

#OR

print(str(ExpressionDescriptor("* 2 3 * *")))
```

### Advanced
```python
# Consult Options.py/CasingTypeEnum.py/DescriptionTypeEnum.py for more info
from cron_descriptor import Options, CasingTypeEnum, DescriptionTypeEnum, ExpressionDescriptor

descriptor = ExpressionDescriptor(
    expression = "*/10 * * * *",
    casing_type = CasingTypeEnum.Sentence,
    use_24hour_time_format = True
)

# GetDescription uses DescriptionTypeEnum.FULL by default:
print(descriptor.get_description())
print(f"{descriptor = }")

# Or passing Options class as second argument:

options = Options()
options.casing_type = CasingTypeEnum.Sentence
options.use_24hour_time_format = True
descriptor = ExpressionDescriptor("*/10 * * * *", options)
print(descriptor.get_description(DescriptionTypeEnum.FULL))
```

## Languages Available

| Language            | Locale Code | Contributor                                             |
|---------------------|-------------|---------------------------------------------------------|
| English             | en          | [Brady Holt](https://github.com/bradyholt)              |
| Chinese Simplified  | zh_CN       | [Star Peng](https://github.com/starpeng)                |
| Chinese Traditional | zh_TW       | [Ricky Chiang](https://github.com/metavige)             |
| Czech               | cs_CZ       | [Adam Schubert](https://github.com/salamek)             |
| Danish              | da_DK       | [Rasmus Melchior Jacobsen](https://github.com/rmja)     |
| Dutch               | nl_NL       | [TotalMace](https://github.com/TotalMace)               |
| Finnish             | fi_FI       | [Mikael Rosenberg](https://github.com/MR77FI)           |
| French              | fr_FR       | [Arnaud TAMAILLON](https://github.com/Greybird)         |
| German              | de_DE       | [Michael Schuler](https://github.com/mschuler)          |
| Hebrew              | he_IL       | [Ariel Deil](https://github.com/arieldeil)              |
| Hungarian           | hu_HU       | [Varga Miklós](https://github.com/Micky2149)            |
| Italian             | it_IT       | [rinaldihno](https://github.com/rinaldihno)             |
| Japanese            | ja_JP       | [Tho Nguyen](https://github.com/tho-asterist)           |
| Korean              | ko_KR       | [KyuJoo Han](https://github.com/hanqyu)                 |
| Norwegian           | nb_NO       | [Siarhei Khalipski](https://github.com/KhalipskiSiarhei)|
| Persian             | fa_IR       | [A. Bahrami](https://github.com/alirezakoo)             |
| Polish              | pl_PL       | [foka](https://github.com/foka)                         |
| Portuguese          | pt_PT       | [Renato Lima](https://github.com/natenho)               |
| Portuguese (Brazil) | pt_BR       | [Renato Lima](https://github.com/natenho)               |
| Romanian            | ro_RO       | [Illegitimis](https://github.com/illegitimis)           |
| Russian             | ru_RU       | [LbISS](https://github.com/LbISS)                       |
| Slovenian           | sl_SI       | [Jani Bevk](https://github.com/jenzy)                   |
| Spanish             | es_ES       | [Ivan Santos](https://github.com/ivansg)                |
| Spanish (Mexico)    | es_MX       | [Ion Mincu](https://github.com/ionmincu)                |
| Swedish             | sv_SE       | [Åke Engelbrektson](https://github.com/eson57)          |
| Vietnamese          | vi_VN       | [Nguyen Duc Son](https://github.com/ali33)              |
| Turkish             | tr_TR       | [Mustafa SADEDİL](https://github.com/sadedil)           |
| Tamil               | ta_IN       | [Sankar Hari](https://github.com/sankarhari)            |
| Ukrainian           | uk_UA       | [Taras](https://github.com/tbudurovych)                 |
| Greek               | el_GR       | [hardra1n](https://github.com/Hardra1n)                 |
| Kazakh              | kk_KZ       | [hardra1n](https://github.com/Hardra1n)                 |
















<!-- SOON
## Demo



## Download

-->

## Original Source
 - .NET - [https://github.com/bradyholt/cron-expression-descriptor](https://github.com/bradyholt/cron-expression-descriptor)

## Ports
 - Java     - [https://github.com/RedHogs/cron-parser](https://github.com/RedHogs/cron-parser)
 - Ruby     - [https://github.com/alpinweis/cronex](https://github.com/alpinweis/cronex)
 - Golang   - [https://github.com/jsuar/go-cron-descriptor](https://github.com/jsuar/go-cron-descriptor)

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

All suggestions and PR's are welcomed

Just clone this repository and register pre-commit hook by running:

```bash
ln -s ../../code-check.sh .git/hooks/pre-commit
```

Then install dev requirements:

```bash
pip install .[dev,test]
```
