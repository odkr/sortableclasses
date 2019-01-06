#!/usr/bin/python
# Copyright 2016, 2019 Odin Kroeger
#
# This programme is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This programme is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""Setup for the *sortablecls* package."""

from os import path
from setuptools import setup


# Functions
# =========

def readme(readme_fname: str = "README.rst") -> str:
    """Returns the contents of README.rst."""
    readme_path = path.join(path.dirname(__file__), readme_fname)
    with open(readme_path) as readme_handle:
        return readme_handle.read()


# Metadata
# ========

# Name of this package.
NAME = 'sortableclasses'

# Version of this package.
VERSION = '0.9.4rc30'

# All other metadata.
METADATA = {
    'name':             NAME,
    'version':          VERSION,
    'description':      """Retrieve all classes derived from a class and
        sort them by a given priority and order, making it
        easy to draw up and use plugin-like classes.""",
    'long_description': readme(),
    'keywords':         'plugin',
    'classifiers':      [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    'url':              'https://github.com/odkr/sortableclasses/',
    'author':           'Odin Kroeger',
    'author_email':     'xacuml@maskr.me',
    'license':          'GPL',
    'python_requires':  '>=3, <4',
    'packages':         ['sortableclasses']
}


# Boilerplate
# ===========

if __name__ == '__main__':
    setup(**METADATA)
