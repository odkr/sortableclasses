#!/usr/bin/python
#
# setup.py - Setup for the *sortablecls* package.
# (c) 2016 Odin Kroeger
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
from setuptools import setup

import os
import sys


# Functions
# =========

def reqpyvers(version, name):
    if sys.version_info >= version:
        return
    errfmt = "{prog}: {name} requires at least Python v{version}.\n"
    prog = os.path.basename(sys.argv[0])
    version_str = ".".join(map(str, version))
    errmsg = errfmt.format(prog=prog, name=name, version=version_str)
    sys.stderr.write(errmsg)
    sys.exit(69)


def readme(readme_fname="README.rst"):
    """Returns the README.rst from the path."""
    readme_path = os.path.join(os.path.dirname(__file__), readme_fname)
    with open(readme_path) as readme_handle:
        return readme_handle.read()


# Metadata
# ========

# Name of this package.
NAME = "sortableclass" 

# Python version that sortablecls requires.
REQPYVERSION=(3,)

# All other metadata.
METADATA = {
    "name":             NAME,
    "version":          '0.9.4b',
    "description":      """Retrieve all classes derived from a class and
                        sort them by a given priority and order, making it
                        easy to draw up and use plugin-like classes.""",
    "long_description": readme(),
    "keywords":         "plugin",
    "classifiers": [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    "url":          "https://github.com/odkr/sortableclasses/",
    "author":       "Odin Kroeger",
    "author_email": "tba",
    "license":      "GPL",
    "packages":     ["sortableclasses"],
    "zip_safe":     False
}


# Boilerplate
# ===========

if "__main__" == __name__:
    reqpyvers(REQPYVERSION, NAME)
    setup(**METADATA)
