===============
sortableclasses
===============

Makes classes sortable by precedence and priority. The order of precedence
of classes and their priority is defined per class and at runtime.

Copyright 2016, 2017, 2018, 2019 Odin Kroeger


Use case
========

*sortableclasses* makes classes sortable by precedence and priority. This is
useful if you want to apply a set of transformations to some data (i.e., if
you're writing what on UNIX-ish systems is called a 'filter'). You could chain
function calls (i.e., ``return transform1(transform2(transform3(...)))``),
but the larger the number of transformation gets, the more difficult this is
to maintain.

*sortableclasses* enables you to define each of those transformations as a
class, assign to each of them a list of predecessors and successors classes
and/or a numerical priority, and then simply sort them using :func:`sorted`.

Simply put, it enables you to write classes that behave similarly to plugins.

For example::

    >>> import sortableclasses
    >>> import abc
    >>> import functools
    >>>
    >>> class Transform(sortableclasses.Pluggable):
    ...     @staticmethod
    ...     @abc.abstractmethod
    ...     def transform(input):
    ...         pass
    ...
    >>> class MakeContent(Transform):
    ...     @staticmethod
    ...     def transform(input):
    ...         if input == ':-(':
    ...             return ':-|'
    ...         return input
    ...
    >>> class MakeHappy(Transform):
    ...     successorof = (MakeContent,)
    ...     @staticmethod
    ...     def transform(input):
    ...         if input == ':-|':
    ...             return ':-)'
    ...         return input
    ...
    >>> class MakeVeryHappy(Transform):
    ...     successorof = (MakeHappy,)
    ...     @staticmethod
    ...     def transform(input):
    ...         if input == ':-)':
    ...             return ':-D'
    ...         return input
    ...
    >>> transforms = sorted(Transform.getderived())
    >>> transforms
    [<class 'MakeContent'>, <class 'MakeHappy'>, <class 'MakeVeryHappy'>]
    >>> input = ':-('
    >>> functools.reduce(lambda k, s: s.transform(k), transforms, input)
    ':-D'


Installation
============

You use *sortableclasses* **at your own risk.** You have been warned.

*sortableclasses* requires Python 3.

If you have Python's `pip <https://pypi.org/project/pip/>`_, simply say::

    pip3 install sortableclasses

Otherwise, download the most recent stable release (`v0.9.4
<https://github.com/odkr/sortableclasses.py/archive/v0.9.4.tar.gz>`_),
unzip it and copy the directory :file:`sortableclasses` into a directory in
your Python's `sys.path`.

You can do all of the above by::

    # Download and unpack *sortableclasses* to the current directory.
    curl -f https://codeload.github.com/odkr/sortableclasses.py/tar.gz/v0.9.4 |
        tar -xz
    # The command below *guesses* a directory to install *sortableclasses* to.
    PYPATH=$(python3 -c 'import sys; print("\n".join(sys.path))' |
        grep -v '.zip' | grep -E "(${HOME?}|/local/)" | head -n1)
    # If the command below errors, no suitable directory was found.
    # Otherwise, it will show you where *sortableclasses* will be installed.
    echo "${PYPATH:?'Did not find a suitable directory.'}"
    # Copy the directory "sortableclasses" into that directory.
    [ -d "${PYPATH:?}" ] && {
        PACKAGE=sortableclasses.py-0.9.4/sortableclasses
        cp -r "$PACKAGE" "$PYPATH" || sudo cp -r "$PACKAGE" "$PYPATH"
    }


Documentation
=============

You can view the reference documentation at `Read the Docs
<https://sortableclassespy.readthedocs.io/en/stable/>`_ or,
once you installed *sortableclasses*, by::

    pydoc3 sortableclasses


Contact
=======

If there's something wrong with *sortableclasses*, please `open an issue
<https://github.com/odkr/sortableclasses.py/issues>`_.


Licence
=======

This programme is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This programme is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Further Information
===================

GitHub:
    <https://github.com/odkr/sortableclasses.py>

PyPI:
    <https://pypi.org/project/sortableclasses/>

Read the docs:
    <https://sortableclassespy.readthedocs.io/en/stable/>
