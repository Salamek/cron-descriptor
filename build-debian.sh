#!/bin/bash
rm -rf "./deb_dist"
python setup.py --command-packages=stdeb.command bdist_deb
