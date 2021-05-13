"""Module for Triangulation Specifications

References:
    [1] R. Loll, Quantum Gravity from Causal Dynamical Triangulations: A Review, Class. Quantum Grav. 37, 013002 (2020).
"""
import collections
from typing import Union, FrozenSet, Set
from cdtea.util import equivdict
from collections.abc import Iterable


def simplex_key(basis):
    if type(basis) == int:
        return Dim0SimplexKey(basis)
    elif isinstance(basis, Iterable):
        fixed_basis = set()
        for b in basis:
            if type(b) == Dim0SimplexKey:
                fixed_basis.add(b)
            else:
                fixed_basis.add(Dim0SimplexKey(b))
        return DimDSimplexKey(fixed_basis)
    else:
        raise Exception("given basis must be iterable or an int")


class SimplexKey:
    """A reference to a simplex"""
    __slots__ = ('_basis', '_dim')

    def __init__(self, basis: Union[FrozenSet, set], dim: int = None):
        self._basis = frozenset(basis)
        self._dim = dim

    def __repr__(self):
        # the zero d case was causing me some debug confusion so i removed it.
        # if self._dim == 0:
        #     return str(list(self._basis)[0])
        return 'basis {' + ','.join(str(b) for b in self._basis) + '}'

    def __eq__(self, other):
        if isinstance(other, SimplexKey):
            return self._basis == other._basis
        else:
            print("Equality not defined between SimplexKey and " + str(type(other)))
            return False

    # this feels really dangerous, i'm just trying it out
    # to define union
    def __or__(self, other):
        new_basis = self._basis | other._basis
        if len(new_basis) == 1:
            return Dim0SimplexKey(new_basis)
        else:
            return DimDSimplexKey(new_basis)

    # to define intersection
    def __and__(self, other):
        new_basis = self._basis & other._basis
        if len(new_basis) == 1:
            return Dim0SimplexKey(new_basis)
        else:
            return DimDSimplexKey(new_basis)

    def __iter__(self):  # we can return self here, because __next__ is implemented
        return iter(self._basis)

    def __hash__(self):
        return hash(self._basis)

    @property
    def basis(self):
        return self._basis

    @property
    def basis_list(self):
        return list(self._basis)

    @property
    def dim(self):
        return self._dim


class Dim0SimplexKey(SimplexKey):
    """A zero dimensional simplex key - reference to a node"""

    def __init__(self, key: int):
        super().__init__(basis={key}, dim=0)


class DimDSimplexKey(SimplexKey):
    """A D dimensional simplex key"""

    def __init__(self, basis: Union[Set[SimplexKey], FrozenSet[SimplexKey]]):
        super().__init__(basis=basis, dim=len(basis) - 1)


class Triangulation:
    """Triangulation Class Stub"""
    __slots__ = ('_simplices', '_simplex_meta', '_time_size')

    def __init__(self, time_size: int):
        self._simplices = collections.defaultdict(set)
        self._simplex_meta = collections.defaultdict(dict)
        self._time_size = time_size

    def add_simplex(self, key: SimplexKey, **meta):
        self._simplices[key.dim].add(key)
        self._simplex_meta[key] = meta

    def remove_simplex(self, key: SimplexKey):
        del self._simplices[key.dim][key]
        del self._simplex_meta[key]

    @property
    def simplices(self):
        return self._simplices

    @property
    def simplex_meta(self):
        return self._simplex_meta

    @property
    def time_size(self):
        return self._time_size
