===============
sortableclasses
===============

Makes classes sortable by precedence and priority. The order of precedence
of classes and their priority is defined per class and at runtime.

Copyright 2016, 2017, 2018, 2019 Odin Kroeger



Use case
========

*sortableclasses* makes classes sortable by precedence and priority. This is
useful if you want to take some input, apply a set of transformations, and
output the result (i.e., if you're writing what on UNIX-ish systems is called
a 'filter'). Ordinarily, you would chain those transformations as function
calls (i.e., ``return transform_1(...(transform_n(input)))``), but the larger
the number of transformation grows, the more difficult this is to maintain.

*sortableclasses* enables you to define each of those transformations as a
class, assign each of them a list of predecessor and successor classes or a
numerical priority, and then simply sort them using ``sort`` or ``sorted``.
Simply put, it enables you to write classes that are similar to plugins
in how they function.

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

You use *sortableclasses* **at your own risk.**
You have been warned.

*sortableclasses* requires Python 3.

If you have Python's `setuptools <https://pypi.org/project/setuptools/>`_,
simply say::

    pip3 install sortableclasses

Otherwise, download the most recent stable release (`v0.9.4
<https://github.com/odkr/sortableclasses.py/archive/v0.9.4.tar.gz>`_),
unzip it and copy the directory `sortableclasses` into a directory in
your Python's `sys.path`.

You can do all of the above by::

    # Download and unpack *sortableclasses* to the current directory.
    curl -f https://codeload.github.com/odkr/sortableclasses.py/tar.gz/v0.9.4 | 
        tar -xz
    # The command below guesses a directory to install *sortableclasses* to.
    PYPATH=$(python3 -c 'import sys; print("\n".join(sys.path))' | 
        grep -v '.zip' | grep -E "(${HOME?}|/local/)" | head -n1)
    # If the command below errors, no suitable directory was found.
    # Otherwise, it will show you where *sortableclasses* will be installed to.
    echo "${PYPATH:?'Did not find a suitable directory.'}" >&2
    # Copy the directory "sortableclasses" into that directory.
    [ -d "${PYPATH:?}" ] && {
        PACKAGE=sortableclasses.py-0.9.4/sortableclasses
        cp -r "$PACKAGE" "$PYPATH" || sudo cp -r "$PACKAGE" "$PYPATH"    
    }
    # Remove the downloaded files, if you want to.
    rm -rf sortableclasses.py-0.9.4


Documentation
=============

You can view the reference documentation at `Read the Docs
<https://sortableclassespy.readthedocs.io/en/latest/>`_ or,
once you installed *sortableclasses*, by::

    pydoc sortableclasses


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

Read the docs:
    <https://sortableclassespy.readthedocs.io/en/latest/>
