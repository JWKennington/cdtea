"""Tests for EquivDict utility"""
import collections
import pytest
from cdtea.util import equivdict


class TestEquivDict:
    """Tests for EquivDict class"""

    def test_create(self):
        d = {'a': 1, 'b': 1, 'c': 2}
        e = equivdict.EquivDict(d)
        assert isinstance(e, equivdict.EquivDict)
        assert isinstance(e.dictionary, dict)
        assert isinstance(e.equiv_dict, collections.defaultdict)

    def test_equiv_class(self):
        d = {'a': 1, 'b': 1, 'c': 2}
        e = equivdict.EquivDict(d)
        assert e.equiv_dict[1] == {'a', 'b'}
        assert e.equiv_dict[2] == {'c'}

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

    def test_setitem(self):
        dict1, dict2 = {'a': 1, 'b': 1, 'c': 2}, {'a': 1, 'b': 1, 'c': 2, 'd': 3}
        e = equivdict.EquivDict(dict1)
        e['d'] = 3

        assert e == equivdict.EquivDict(dict2)

        with pytest.raises(Exception):
            dualequiv_dict = e.dual
            dualequiv_dict[3] = 'd'

    def test_del_item(self):
        dict1, dict2 = {'a': 1, 'b': 1, 'c': 2}, {'a': 1, 'b': 1, 'c': 2, 'd': 3}
        e1, e2 = equivdict.EquivDict(dict1), equivdict.EquivDict(dict2)

        del e2['d']

        assert e1 == e2
