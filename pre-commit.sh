#!/bin/bash
set -e
find cron_descriptor -name '*.py' -exec autopep8 --in-place '{}' \;
pep8 cron_descriptor

python setup.py test
