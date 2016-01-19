#!/bin/bash
set -e
find cron_descriptor -name '*.py' -exec autopep8 --in-place --max-line-length=120 '{}' \;
pep8 --max-line-length=120 cron_descriptor

python setup.py test
python3 setup.py test
