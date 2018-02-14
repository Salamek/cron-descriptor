# Copyright (C) 2016 Adam Schubert <adam.schubert@sg1-game.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import setuptools
import sys

version = "1.2.10+se"


if __name__ == "__main__":
    if sys.version_info >= (3,0):
        long_description = open('README.md', encoding='utf-8').read()
    else:
        long_description = open('README.md').read()
    
    setuptools.setup(
        name="cron_descriptor",
        version=version,
        description="A Python library that converts cron expressions "
                    "into human readable strings.",
        author="Adam Schubert",
        author_email="adam.schubert@sg1-game.net",
        url="https://github.com/Salamek/cron-descriptor",
        long_description=long_description,
        packages=setuptools.find_packages(),
        package_data={
            'cron_descriptor': [
                'locale/*.mo',
            ],
        },
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Environment :: Web Environment",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 2.5",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Topic :: Software Development",
        ],
        test_suite="tests"
    )
