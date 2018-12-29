# pylint: disable=E1101,R0903
"""Test Suite for sortableclasses.

Copyright 2016, 2018 Odin Kroeger

This programme is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This programme is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

import doctest
import unittest
import random
import sys

from os.path import join, dirname, realpath, abspath

PACKAGE_DIR = realpath(abspath(join(dirname(__file__), *('..',)*2)))
sys.path.insert(0, PACKAGE_DIR)

# pylint: disable=C0413
import sortableclasses


# Constants
# =========

# How many plugins to create in tests where a small number of plugins suffices.
TEST_COUNT_SMALL = 128

# How many plugins to create in tests where a large number of plugins is
# needed. This should always be larger than the recursion limit.
TEST_COUNT_BIG = sys.getrecursionlimit() + 1


# Plugins for Testing
# ===================

class PluginBase(sortableclasses.Pluggable):
    """Base class for test plugins."""

class AutoRetrievalTestPluginBase(PluginBase):
    """Base class for automatic plugin retrieval tests."""

class AutoSortingTestPluginBase(PluginBase):
    """Base class for automatic plugin sorting tests."""

class ManualTestPluginBase(PluginBase):
    """Base class for manual tests."""

class NoPluginsPluginBase(PluginBase):
    """Class for testing against an empty list of plugins."""

class TestPluginA(ManualTestPluginBase):
    """A class for manual tests."""
    priority = 1

class TestPluginB(ManualTestPluginBase):
    """A class for manual tests."""

class TestPluginC(ManualTestPluginBase):
    """A class for manual tests."""
    predecessorof = (TestPluginB,)

class TestPluginSubA1(TestPluginA):
    """A class for manual tests."""
    priority = 1000

class TestPluginSubA2(TestPluginA):
    """A class for manual tests."""
    priority = 100

class TestPluginSubA3(TestPluginA):
    """A class for manual tests."""
    priority = 10

class CyclicalTestBase(PluginBase):
    """Base for cyclically ordered plugins."""

class TestCyclicalA(CyclicalTestBase):
    """A plugin to be put in cyclical order."""

class TestCyclicalB(CyclicalTestBase):
    """A plugin to be put in cyclical order."""
    successorof = (TestCyclicalA,)
    predecessorof = (TestCyclicalA,)


# Setting up Plugins for Test Suites
# ==================================

def make_plugs(num, plugtype, populator=lambda i, acc: dict(index=i)):
    """Create ``num`` plugins of ``plugtype`` and return them.

    Arguments:
        num (``int``):
            How many plugins to create.
        plugtype (subclass of ``sortableclasses``):
            Type of plugins to create.
        populator (callable):
            A function that takes an index (``int``) and the list
            of plugins that have been created up to its being
            called (as ``plugtype`` sequence), as positional
            arguments and returns a mapping of attributes for
            the next plugin to be created. Optional, defaults
            to ``lambda i, acc: dict(index=i)``

    Returns (``list`` of instances of ``plugtype``):
        The plugins created.
    """
    plugins = []
    for i in range(num):
        # Use the previous class as base half the time
        # and the actual base supplied the other half of the time.
        base = plugins[i-1] if i > 0 and i % 2 else plugtype
        name = base.__name__ + "N" + str(i)
        attrs = populator(i, plugins)
        plugins.append(type(name, (base,), attrs))
    return plugins


# Test Suites
# ===========

# Plugin Retrieval
# ----------------

class TestPluginRetrievalManually(unittest.TestCase):
    """Manual tests for ``sortableclasses.getderived()``."""
    def test_empty_type(self):
        """Test if ``getderived()`` returns right type."""
        try:
            list(NoPluginsPluginBase.getderived())
        except TypeError:
            self.fail()

    def test_empty_elements(self):
        """Test if ``getderived()`` returns empty
            for unimplemented interfaces."""
        should = ()
        is_ = list(NoPluginsPluginBase.getderived())
        self.assertCountEqual(should, is_)

    def test_elements(self):
        """Test if ``getderived`` works."""
        should = (TestPluginA, TestPluginB, TestPluginC,
                  TestPluginSubA1, TestPluginSubA2, TestPluginSubA3)
        is_ = list(ManualTestPluginBase.getderived())
        self.assertCountEqual(should, is_)


class TestPluginRetrievalAuto(unittest.TestCase):
    """Automatic tests for ``getderived()``."""
    proto = AutoRetrievalTestPluginBase
    plugins = make_plugs(TEST_COUNT_SMALL, proto)

    def test_bycounting(self):
        """Test if ``getderived()`` works by counting."""
        should = len(self.plugins)
        is_ = len(list(self.proto.getderived()))
        self.assertEqual(should, is_)

    def test_byevaluatingresult(self):
        """Test if ``getderived()`` works by evaluating its result."""
        should = self.plugins
        is_ = list(self.proto.getderived())
        self.assertCountEqual(should, is_)


# Sorting
# -------

class TestSortingManually(unittest.TestCase):
    """Manual sorting tests."""
    def test_chainofsucession(self):
        """Test if ``insuccessorsof`` works for simple setups (1)."""
        self.assertTrue(TestPluginC.inpredecessorsof(TestPluginB))

    def test_chainofprecedence(self):
        """Test if ``inpredecessorsof`` works for simple setups (1)."""
        self.assertFalse(TestPluginB.insuccessorsof(TestPluginC))

    def test_chainofsucession_reverse(self):
        """Test if ``insuccessorsof`` works for simple setups (2)."""
        self.assertFalse(TestPluginC.insuccessorsof(TestPluginB))

    def test_chainofprecedence_reverse(self):
        """Test if ``inpredecessorsof`` works for simple setups (2)."""
        self.assertFalse(TestPluginB.inpredecessorsof(TestPluginC))

    def test_sucession(self):
        """Test if ``succeeds`` works for simple setups (1)."""
        self.assertTrue(TestPluginB.succeeds(TestPluginC))

    def test_precedence(self):
        """Test if ``precedes`` works for simple setups (2)."""
        self.assertTrue(TestPluginC.precedes(TestPluginB))

    def test_sucession_reverse(self):
        """Test if ``succeeds`` works for simple setups (1)."""
        self.assertFalse(TestPluginC.succeeds(TestPluginB))

    def test_precedence_reverse(self):
        """Test if ``precedes`` works for simple setups (2)."""
        self.assertFalse(TestPluginB.precedes(TestPluginA))

    def test_lt(self):
        """Test if ``__lt__`` works for simple setups (1)."""
        self.assertTrue(TestPluginB < TestPluginA)

    def test_lt_reverse(self):
        """Test if ``__lt__`` works for simple setups (2)."""
        self.assertFalse(TestPluginA < TestPluginB)

    def test_sort(self):
        """Test if sorting works for a simple setup."""
        unsorted = ManualTestPluginBase.getderived()
        should = (TestPluginC, TestPluginB, TestPluginA,
                  TestPluginSubA3, TestPluginSubA2, TestPluginSubA1)
        is_ = tuple(sorted(unsorted))
        self.assertEqual(should, is_)

    def test_cyclical(self):
        """Test if cyclical orderings raise an exception."""
        unsorted = CyclicalTestBase.getderived()
        with self.assertRaises(sortableclasses.CyclicalOrderError):
            sorted(unsorted)


class TestSortingAuto(unittest.TestCase):
    """Automatic sorting tests."""
    proto = AutoSortingTestPluginBase
    plugins = make_plugs(TEST_COUNT_BIG, proto, lambda i, acc: dict(
        index=i,
        priority=-i,
        random=random.randint(0, TEST_COUNT_BIG),
        predecessorof=(acc[i-1],) if i > 0 and i > i/TEST_COUNT_BIG else ()
    ))

    def test_simple_sort(self):
        """Test if sorting a large non-random sequence works."""
        should = tuple(reversed(self.plugins))
        is_ = tuple(sorted(self.plugins))
        self.assertEqual(should, is_)

    def test_harder_sort(self):
        """Test if sorting a large pseudo-random sequence works."""
        random_ = sorted(self.plugins, key=lambda x: x.random)
        should = tuple(reversed(self.plugins))
        is_ = tuple(sorted(random_))
        self.assertEqual(should, is_)


# Test Code Examples
# ------------------

# pylint: disable=W0613
def load_tests(loader, tests, ignore):
    """Test code examples."""
    tests.addTests(doctest.DocTestSuite(sortableclasses))
    tests.addTests(doctest.DocFileSuite(join(PACKAGE_DIR, "README.rst"),
                                        module_relative=False))
    return tests


# Boilerplate
# -----------

if __name__ == "__main__":
    unittest.main()
