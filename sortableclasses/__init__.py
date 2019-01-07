# Copyright 2016, 2018, 2019 Odin Kroeger
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>
"""Makes classes sortable by priority and precedence."""

import abc


# Exceptions
# ==========

class Error(Exception):
    """Base class for exceptions of this module."""

    def __init__(self, **kwargs):
        """Initialise the error."""
        super().__init__()
        self.__dict__.update(kwargs)

    # pylint: disable=E1101
    def __str__(self):
        """Return the formatted error message."""
        return self.template.format(**vars(self))


class CyclicalOrderError(Error):
    """Declared order is cyclical."""

    template = '{cls} and {other} pre- *and* succeed each other.'


# Sorting
# =======

class SortableMeta(type):
    """Classes of this type can be :func:`sorted`.

    Caveat:
        On a 1,4 GHz Intel Core i5 with a load average of 1.7, sorting
        a list of plugins into an order that, one, is defined using
        :attr:`priority` for one half of the plugins and :attr:`predecessorof`
        for the other and where, two, swapping any two plugins will
        undo that order will take, approximately:

        ============   ==========  =============
        Plugin count         Initial order
        ------------   -------------------------
             -         non-random  pseudo-random
        ============   ==========  =============
                 256        0.01s          0.04s
                1024        0.09s          0.93s
                4096        1.68s         18.41s
        ============   ==========  =============

        That said, the order sketched out above is rather demanding:

         1. It's, in part, defined via a *long* chain of precedence
            (up to 2048 elements).

         2. It requires every plugin to be at a definite position.

        Also, in the 'real world', sequences of plugins shouldn't be
        in pseudo-random order.

        On the same hardware, sorting a list of plugins into an
        order that is only defined using :attr:`SortableMeta.priority`
        will take approximately:

        ============  =====
        Plugin count   Time
        ============  =====
              65,536  0.22s
             638,899  4.50s
        ============  =====

        (The above tests were done with a non-random initial order.)

        That being so, you should be fine as long as:

         1. You sort no more than about 8,192 plugins.

         2. No chain of succession or precedence
            is longer than about 128 plugins.

         3. Your order doesn't require every plugin
            to be at a definite position.

    .. automethod:: __lt__
    """

    predecessorof = ()
    """Sequence of classes used by :meth:`inpredecessorsof`."""
    successorof = ()
    """Sequence of classes used by :meth:`insuccessorsof`."""
    priority = 0  # type: float
    """Number used by :meth:`__lt__`."""

    def insuccessorsof(cls, other: 'SortableMeta') -> bool:
        """Check if *cls* is in the chain of succession of *other*.

        :param SortableMeta other: Class to compare *cls* to.
        :return: Whether *other* is a member of the :attr:`successorof`\
            attribute of *cls*, the classes *cls* is a successor of,\
            the classes these classes are successors of, and so on.
        :rtype: bool

        A class is in the chain of succession of another class
        if it, or one of its predecessors, declares itself to
        be a :attr:`successorof` that class.

        For example:

            >>> class sortableclass(Pluggable):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     pass
            ...
            >>> class B(sortableclass):
            ...     successorof = (A,)
            ...
            >>> class C(sortableclass):
            ...     successorof = (B,)
            ...
            >>> C.insuccessorsof(A)
            True

        However, different to :meth:`succeeds`:

            >>> class B(sortableclass):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     predecessorof = (B,)
            ...
            >>> B.insuccessorsof(A)
            False

        """
        chain = list(cls.successorof)  # type: list
        i = 0
        while i < len(chain):
            if other == chain[i]:
                return True
            chain.extend(chain[i].successorof)
            i += 1
        return False

    def inpredecessorsof(cls, other: 'SortableMeta') -> bool:
        """Check if *cls* is in the chain of precedence of *other*.

        :param SortableMeta other: Class to compare *cls* to.
        :return: Whether *other* is a member of the :attr:`predecessorof`\
            attribute of *cls*, the classes *cls* is a predecessor of,\
            the classes these classes are predecessors of, and so on.
        :rtype: bool

        A class is in the chain of precedence of another class
        if it, or one of its successors, declares itself to
        be a :attr:`predecessorof` that class.

        For example:

            >>> class sortableclass(Pluggable):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     pass
            ...
            >>> class B(sortableclass):
            ...     predecessorof = (A,)
            ...
            >>> class C(sortableclass):
            ...     predecessorof = (B,)
            ...
            >>> C.inpredecessorsof(A)
            True

        However, different to :meth:`precedes`:

            >>> class B(sortableclass):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     successorof = (B,)
            ...
            >>> B.inpredecessorsof(A)
            False

        """
        chain = list(cls.predecessorof)  # type: list
        i = 0
        while i < len(chain):
            if other == chain[i]:
                return True
            chain.extend(chain[i].predecessorof)
            i += 1
        return False

    # pylint: disable=E1120
    def succeeds(cls, other: 'SortableMeta') -> bool:
        """Check if *cls* succeeds *other*.

        :param SortableMeta other: Class to compare *cls* to.
        :return: Whether *cls* succeeds *other*.
        :rtype: bool

        Doesn't take priority into account.

        Caveat:
            Doesn't check whether the declared order is consistent.
            That is, will return `True` even if *other* also
            succeeds *cls*.

        For example:

            >>> class sortableclass(Pluggable):
            ...     pass
            ...
            >>> class B(sortableclass):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     successorof = (B,)
            ...
            >>> A.succeeds(B)
            True

        Also, different to :meth:`insuccessorsof`:

            >>> class A(sortableclass):
            ...     pass
            ...
            >>> class B(sortableclass):
            ...     predecessorof = (A,)
            ...
            >>> A.succeeds(B)
            True

        """
        return cls.insuccessorsof(other) or other.inpredecessorsof(cls)

    # pylint: disable=E1120
    def precedes(cls, other: 'SortableMeta') -> bool:
        """Check if *cls* precedes *other*.

        :param SortableMeta other: Class to compare *cls* to.
        :return: Whether *cls* precedes *other*.
        :rtype: bool

        Doesn't take priority into account.

        Caveat:
            Doesn't check whether the declared order is consistent.
            That is, returns `True` even if *other* also precedes *cls*.

        For example:

            >>> class sortableclass(Pluggable):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     pass
            ...
            >>> class B(sortableclass):
            ...     predecessorof = (A,)
            ...
            >>> B.precedes(A)
            True

        Also, different to :meth:`inpredecessorsof`:

            >>> class B(sortableclass):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     successorof = (B,)
            ...
            >>> B.precedes(A)
            True

        """
        return cls.inpredecessorsof(other) or other.insuccessorsof(cls)

    def __lt__(cls, other: 'SortableMeta') -> bool:
        """Check if *cls* class precedes *other*.

        :param SortableMeta other: Class to compare *cls* to.
        :return: Whether *cls* precedes *other*.
        :rtype: bool
        :raises CyclicalOrderError: If, according to the order defined by\
            the :attr:`successorof` and :attr:`predecessorof` attributes,\
            two plugin-like classes would have to precede *and* \
            succeed each other.

        Whether a plugin-like class precedes another one is
        governed by their sorting attributes:

        * :attr:`successorof` -- A sequence of plugin-like classes that
          should precede *cls* (defaults to an empty tuple).
        * :attr:`predecessorof` -- A sequence of plugin-like classes that
          should succeed *cls* (defaults to an empty tuple).
        * :attr:`priority` -- A number that expresses the priority of *cls*,
          where lower numbers express a higher priorit (defaults to 0).

        *successorof* and *predecessorof* take precedence over *priority*.

        For example:

            >>> class sortableclass(Pluggable):
            ...     pass
            ...
            >>> class A(sortableclass):
            ...     # Default priority is 0.
            ...     pass
            ...
            >>> class B(sortableclass):
            ...     priority = -1
            ...
            >>> class C(sortableclass):
            ...     predecessorof = (B,)
            ...     successorof = (A,)
            ...
            >>> B < A
            True
            >>> B < C
            True
            >>> A < B
            False
            >>> A < C
            True
            >>> C < B
            True
            >>> C < A
            False

        """
        if cls.precedes(other):
            if other.precedes(cls):
                raise CyclicalOrderError(cls=cls, other=other)
            return True
        return cls.priority < other.priority


# Utility class
# =============

class SortableABCMeta(abc.ABCMeta, SortableMeta):
    """A metaclass for abstract base classes that should be sortable."""


# Class "Pluggable"
# =================

# pylint: disable=R0903
class Pluggable(metaclass=SortableABCMeta):
    """Base class for simple plugin-like architectures.

    To use :class:`Pluggable`:

     1. Derive a class from :class:`Pluggable`, call it `PBC`
        (Plugin Base Class) for the purposes of this documentation.

     2. Define an interface that plugin-like
        classes have to implement in `PBC`.

     3. Derrive classes from `PBC`.

    *Nota bene*: Classes derived from :class:`Pluggable` are eo ipso
    abstract base classes (i.e., have a metaclass derived from
    :class:`abc.ABCMeta`).

    You can now get a list of all plugin-like classes, that is, all
    classes derived from `PBC`, by calling `PBC.getderived()`.
    Moreover, plugin-like classes can be sorted using :func:`sorted`.
    See :class:`SortableMeta` for details.

    If you have multiple types of plugins, that is, multiple plugin
    base classes, I recommend that, rather than deriving them from
    :class:`Pluggable` directly, you define a common plugin base class
    that does and from which you derive your remaining plugin
    base classes.
    """

    @classmethod
    def getderived(cls):
        """Get derived classes, including indirectly derived ones.

        Returns:
            All classes derived from *cls*
            (as iterator over :class:`type` instances).

        For example:

            >>> class PluginBaseClass(Pluggable):
            ...     pass
            ...
            >>> class A(PluginBaseClass):
            ...     pass
            ...
            >>> class APrime(A):
            ...     pass
            ...
            >>> list(PluginBaseClass.getderived())
            [<class 'sortableclasses.A'>, <class 'sortableclasses.APrime'>]

        You can sort classes returned by :meth:`getderived`.
        See :class:`SortableMeta` for details.

        For example:

            >>> class PluginBaseClass(Pluggable):
            ...     pass
            ...
            >>> class A(PluginBaseClass):
            ...     # Default priority is 0.
            ...     pass
            ...
            >>> class B(PluginBaseClass):
            ...     priority = -1
            ...
            >>> list(PluginBaseClass.getderived())
            [<class 'sortableclasses.A'>, <class 'sortableclasses.B'>]
            >>> sorted(PluginBaseClass.getderived())
            [<class 'sortableclasses.B'>, <class 'sortableclasses.A'>]

        """
        for subclass in cls.__subclasses__():
            yield subclass
            # ``yield from`` would be cooler,
            # but let's stick with Python 3.0.
            for derivedclass in subclass.getderived():
                yield derivedclass
