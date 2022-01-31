"""Utility for a dictionary that keeps track of value-equivalence-classes

"""
import collections
from collections.abc import Iterable


class EquivDict:
    """An EquivDict is a combination of two mappings, the original dictionary and
    a second mapping from value equivalence classes to elements of the equivalence classes
    """

    def __init__(self, d: dict = None):
        self._dict = {} if d is None else d.copy()
        self._equiv_dict = None
        self._update_equiv_dict()

    def __eq__(self, other):
        return isinstance(other, EquivDict) and (self._dict == other._dict and self._equiv_dict == other._equiv_dict)

    def __getitem__(self, item):
        """Pass thru to dict"""
        return self._dict.__getitem__(item)

    def __setitem__(self, key, value):
        """Pass thru to dict and update equiv dict"""

        if key in self._dict:
            del self[key]

        if isinstance(value, set):
            for v in value:
                self._equiv_dict[v].add(key)
        else:
            self._equiv_dict[value].add(key)

        return self._dict.__setitem__(key, value)

    def __delitem__(self, instance):
        """Pass thru to dict and update equiv dict"""
        value = self._dict.get(instance)

        if isinstance(value, set):
            for v in value:
                self._equiv_dict[v].discard(instance)
                if self._equiv_dict[v] == set():
                    del self._equiv_dict[v]
        else:
            self._equiv_dict[value].discard(instance)
            if self._equiv_dict[value] == set():
                del self._equiv_dict[value]

        self._dict.pop(instance)

    def _update_equiv_dict(self):
        self._equiv_dict = collections.defaultdict(set)
        for k, v in self._dict.items():
            self._equiv_dict[v].add(k)

    @property
    def dictionary(self):
        return self._dict

    @property
    def equiv_dict(self):
        return self._equiv_dict

    @property
    def dual(self):
        """Return dual mapping"""
        return EquivDictDual(self)

    @property
    def keys(self):
        """Return dual mapping"""
        return list(self._dict)


class EquivDictDual:
    """An equivdict with the dict interface reversed, getitem refers to the equiv dict"""

    def __init__(self, edict: EquivDict):
        self._edict = edict

    def __getitem__(self, item):
        return self._edict._equiv_dict.__getitem__(item)

    def __setitem__(self, key, value):
        raise ValueError('Cannot set values on an equivalence dict wrapper')

    @property
    def dual(self):
        """return the dual map"""
        return self._edict
