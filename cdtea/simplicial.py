"""Module for Triangulation Specifications

References:
    [1] R. Loll, Quantum Gravity from Causal Dynamical Triangulations: A Review, Class. Quantum Grav. 37, 013002 (2020).
"""
from __future__ import annotations
import collections
from typing import Union
from collections.abc import Iterable


def simplex_key(basis: Union[int, Iterable]):
    """
    Generates a simplex key from an int or an iterable of ints
    """

    if isinstance(basis, int):
        return Dim0SimplexKey(basis)

    elif not isinstance(basis, Iterable):
        raise Exception("given basis must be iterable of ints or an int")

    fixed_basis = set()
    for b in basis:
        if isinstance(b, Dim0SimplexKey):
            fixed_basis.add(b)
        elif isinstance(b, int):
            fixed_basis.add(Dim0SimplexKey(b))
        else:
            raise Exception("given basis must be iterable of ints or an int")
    # if basis is an iterable with a single item
    if len(fixed_basis) == 1:
        return list(fixed_basis)[0]
    return DimDSimplexKey(fixed_basis)


class SimplexKey:
    """A reference to a simplex"""
    __slots__ = ('_basis', '_dim')

    def __init__(self, basis: Union[frozenset, set], dim: int = None):
        self._basis = frozenset(basis)
        self._dim = dim

    def __repr__(self):
        if self._dim == 0:
            return '<' + str(list(self._basis)[0]) + '>'
        return '<' + ' '.join(str(list(b._basis)[0]) for b in self._basis) + '>'

    def __eq__(self, other):
        if isinstance(other, SimplexKey):
            return self._basis == other._basis
        # print("Equality not defined between SimplexKey and " + str(isinstance(other,
        return False

    # to speed up set style interactions with simplex keys
    # to define union
    def __or__(self, other):
        self_basis = self._basis if isinstance(self, DimDSimplexKey) else {self}
        other_basis = other._basis if isinstance(other, DimDSimplexKey) else {other}

        new_basis = self_basis | other_basis

        if len(new_basis) == 1:
            return list(new_basis)[0]
        return DimDSimplexKey(new_basis)

    # to define intersection
    def __and__(self, other):
        self_basis = self._basis if isinstance(self, DimDSimplexKey) else {self}
        other_basis = other._basis if isinstance(other, DimDSimplexKey) else {other}

        new_basis = self_basis & other_basis
        if len(new_basis) == 1:
            return list(new_basis)[0]
        return DimDSimplexKey(new_basis)

    # set difference
    def __sub__(self, other):
        self_basis = self._basis if isinstance(self, DimDSimplexKey) else {self}
        other_basis = other._basis if isinstance(other, DimDSimplexKey) else {other}
        new_basis = self_basis - other_basis
        if len(new_basis) == 1:
            return list(new_basis)[0]
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

    def __init__(self, basis: Union[set[SimplexKey], frozenset[SimplexKey]]):
        super().__init__(basis=basis, dim=len(basis) - 1)


class Triangulation:
    """Triangulation Class Stub"""
    __slots__ = ('_simplices', '_simplex_meta', '_time_size', '_max_index')

    def __init__(self, time_size: int):
        self._simplices = collections.defaultdict(set)
        self._simplex_meta = collections.defaultdict(dict)
        self._time_size = time_size
        self._max_index = 0

    def add_simplex(self, key: SimplexKey, **meta):
        """adds a simplex to the triangulation"""
        if key.dim == 0:
            self._max_index += 1
        self._simplices[key.dim].add(key)
        self._simplex_meta[key] = meta

    def remove_simplex(self, key: SimplexKey):
        """removes a simplex from the triangulation"""
        self._simplices[key.dim].remove(key)
        del self._simplex_meta[key]

    def __eq__(self, other):
        if isinstance(other, Triangulation):
            same_simplices = self._simplices == other.simplices
            same_meta = self._simplex_meta == other.simplex_meta
            same_time_size = self.time_size == other.time_size
            same_triangulation = same_simplices and same_meta and same_time_size
            return same_triangulation
        return False

    # Safe access methods
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

    # quick semantic access to triangulation elements and properties
    @property
    def nodes(self):
        return self._simplices[0]

    @property
    def edges(self):
        return self._simplices[1]

    @property
    def faces(self):
        return self._simplices[2]
