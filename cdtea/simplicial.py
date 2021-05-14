"""Module for Triangulation Specifications

References:
    [1] R. Loll, Quantum Gravity from Causal Dynamical Triangulations: A Review, Class. Quantum Grav. 37, 013002 (2020).
"""
import collections
import typing
from typing import Union, FrozenSet, Set, Iterable
from cdtea.util import equivdict
from collections.abc import Iterable


def simplex_key(basis: typing.Union[int, Iterable]):
    if type(basis) == int:
        return Dim0SimplexKey(basis)
    elif isinstance(basis, Iterable):
        fixed_basis = set()
        for b in basis:
            if type(b) == Dim0SimplexKey:
                fixed_basis.add(b)
            else:
                fixed_basis.add(Dim0SimplexKey(b))
        if len(fixed_basis) == 1:
            return list(fixed_basis)[0]
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

    # to speed up set style interactions with simplex keys
    # to define union
    def __or__(self, other):
        self_basis = self._basis if type(self) == DimDSimplexKey else {self}
        other_basis = other._basis if type(other) == DimDSimplexKey else {other}

        new_basis = self_basis | other_basis

        if len(new_basis) == 1:
            return list(new_basis)[0]
        else:
            return DimDSimplexKey(new_basis)

    # to define intersection
    def __and__(self, other):
        self_basis = self._basis if type(self) == DimDSimplexKey else {self}
        other_basis = other._basis if type(other) == DimDSimplexKey else {other}

        new_basis = self_basis & other_basis
        if len(new_basis) == 1:
            return list(new_basis)[0]
        else:
            return DimDSimplexKey(new_basis)

    # set difference
    def __sub__(self, other):
        self_basis = self._basis if type(self) == DimDSimplexKey else {self}
        other_basis = other._basis if type(other) == DimDSimplexKey else {other}
        new_basis = self_basis - other_basis
        if len(new_basis) == 1:
            return list(new_basis)[0]
        else:
            return DimDSimplexKey(new_basis)

    # ------- end set operations-------

    def __iter__(self):
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
    __slots__ = ('_simplices', '_simplex_meta', '_time_size','_max_index')

    def __init__(self, time_size: int):
        self._simplices = collections.defaultdict(set)
        self._simplex_meta = collections.defaultdict(dict)
        self._time_size = time_size
        self._max_index = 0

    def add_simplex(self, key: SimplexKey, **meta):
        if key.dim == 0:
            self._max_index += 1
        self._simplices[key.dim].add(key)
        self._simplex_meta[key] = meta

    def remove_simplex(self, key: SimplexKey):
        self._simplices[key.dim].remove(key)
        del self._simplex_meta[key]

    def __eq__(self, other):
        if type(other) == Triangulation:
            return (self._simplices == other._simplices) and (self._simplex_meta == other._simplex_meta) and (self._time_size == other._time_size)
        return False

    @property
    def simplices(self):
        return self._simplices

    @property
    def max_index(self):
        return self._max_index

    @property
    def simplex_meta(self):
        return self._simplex_meta

    @property
    def time_size(self):
        return self._time_size
