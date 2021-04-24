"""Tests for EquivDict utility"""
import collections

from cdtea.util import equivdict


class TestEquivDict:
    """Tests for EquivDict class"""

    def test_create(self):
        d = {'a': 1, 'b': 1, 'c': 2}
        e = equivdict.EquivDict(d)
        assert isinstance(e, equivdict.EquivDict)
        assert isinstance(e._dict, dict)
        assert isinstance(e._equiv_dict, collections.defaultdict)

    def test_equiv_class(self):
        d = {'a': 1, 'b': 1, 'c': 2}
        e = equivdict.EquivDict(d)
        assert e._equiv_dict[1] == {'a', 'b'}
        assert e._equiv_dict[2] == {'c'}

    def test_equivalence(self):
        d = {'a': 1, 'b': 1, 'c': 2}
        e1 = equivdict.EquivDict(d)
        e2 = equivdict.EquivDict(d)

        assert id(e1) != id(e2)
        assert e1 == e2

    def test_dual_interface(self):
        d = {'a': 1, 'b': 1, 'c': 2}
        e = equivdict.EquivDict(d)

        assert e.dual.dual == e

        assert e['a'] == 1
        assert e.dual[1] == {'a', 'b'}
