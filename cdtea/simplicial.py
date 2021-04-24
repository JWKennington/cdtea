"""Module for Triangulation Specifications

References:
    [1] R. Loll, Quantum Gravity from Causal Dynamical Triangulations: A Review, Class. Quantum Grav. 37, 013002 (2020).
"""
import collections
from typing import Union, FrozenSet, Set
from cdtea.util import equivdict


class SimplexKey:
    """A reference to a simplex"""
    __slots__ = ('_basis', '_dim')

    def __init__(self, basis: Union[FrozenSet, set], dim: int = None):
        self._basis = frozenset(basis)
        self._dim = dim

    def __repr__(self):
        if self._dim == 0:
            return str(list(self._basis)[0])
        return '{' + ','.join(str(b) for b in self._basis) + '}'

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

    def __init__(self):
        self._simplices = collections.defaultdict(set)
        self._simplex_meta = collections.defaultdict(dict)

    def add_simplex(self, key: SimplexKey, **meta):
        self._simplices[key.dim].add(key)
        self._simplex_meta[key] = meta
