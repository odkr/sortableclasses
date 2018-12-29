===============
sortableclasses
===============

Makes classes sortable by precedence and priority. The order of precedence
of classes and their priority is defined de-centrally and at runtime.

Copyright 2016, 2017, 2018 Odin Kroeger



Use case
========

*sortableclasses* makes classes sortable. This is useful if all you want to do
is take some input, apply a set of transformations, and output the result
(i.e., are writing what on UNIX-ish systems is called a 'filter'). 
Of course, you may just write, e.g., ``return t1(t2(t3(...(tn(input))))))``
but the more transformations you need to add, the harder this is to maintain.
*sortableclasses* allows you to turn the transformations into classes, assign
each of them a priority (or a list of predecessors and successors) and then
sort them using ``sort`` ``sorted``.


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

*sortableclasses* works only in Python 3.

If you have Python's `setuptools <https://pypi.org/project/setuptools/>`, just say::

    pip3 install sortableclasses

Otherwise, clone this repository and run `python3 setup.py install`.


Documentation
=============

See <https://sortableclassespy.readthedocs.io/en/latest/> for reference.

You can also view the inline documentation, by::

    pydoc sortableclasses


Contact
=======

If there's something wrong with *sortableclasses*, please open an issue at:
    <https://github.com/odkr/sortableclasses.py/issues>


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
