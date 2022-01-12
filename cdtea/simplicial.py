"""Module for Triangulation Specifications

References:
    [1] R. Loll, Quantum Gravity from Causal Dynamical Triangulations: A Review, Class. Quantum Grav. 37, 013002 (2020).
"""
from __future__ import annotations

import collections
from itertools import combinations
from typing import Union, Iterable

from cdtea.util import equivdict


def simplex_key(basis: Union[int, Iterable]):
    """
    Generates a simplex key from an int or an iterable of ints
    """

    if isinstance(basis, int):
        return Dim0SimplexKey(basis)

    if not isinstance(basis, Iterable):
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
    _COUNTS = collections.defaultdict(int)
    __slots__ = ('_basis', '_dim', '_sub_keys', '_count_id')

    def __init__(self, basis: Union[frozenset, set], dim: int = None, multi: bool = False, count_id: int = None):
        """Create a Simplex Key

        Args:
            basis:
                frozenset or set, the basis 0simplices
            dim:
                int, default None, the dimension of the new simplex
            multi:
                bool, default False, if True create a new copy of the simplex corresponding to the given basis. Example
                usage is creating a multi edge, for the second edge set "multi=True".
            count_id:
                int, default None, used to distinguish multisimplices. Must be passed if creating a reference to a multi
                simplex (at which point the "multi" argument will be True)
        """
        self._basis = frozenset(basis)
        self._dim = dim
        self._sub_keys = None

        if multi:
            self._COUNTS[self._basis] += 1
            self._count_id = self._COUNTS[self._basis]
        else:
            if self._COUNTS[self._basis] > 0 and count_id is None:
                raise ValueError('Cannot create reference to multi simplex without a count_id.')
            self._count_id = count_id

    def __repr__(self):
        # TODO make easier access to int in Dim0 Simplex Key
        if self._dim == 0:
            return '<' + str(list(self._basis)[0]) + '>'
        return '<' + ' '.join(sorted(str(list(b._basis)[0]) for b in self._basis)) + '>'

    def __hash__(self):
        return hash((self._count_id, self._basis))

    def __eq__(self, other):
        if isinstance(other, SimplexKey):
            return self._basis == other._basis and self._count_id == other._count_id
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

    @property
    def basis(self):
        return self._basis

    @property
    def basis_list(self):
        return list(self._basis)

    @property
    def dim(self):
        return self._dim

    @classmethod
    def flush_counts(cls):
        """Flush Counts"""
        cls._COUNTS = collections.defaultdict(int)

    @property
    def sub_keys(self):
        """get all sub-simplices of self. (excluding self)"""
        if self._sub_keys is None:
            self._sub_keys = set({})
            for d in range(1, self.dim + 1):
                combs = {simplex_key(x) for x in combinations(self.basis, d)}
                self._sub_keys = self._sub_keys.union(combs)
        return self._sub_keys


class Dim0SimplexKey(SimplexKey):
    """A zero dimensional simplex key - reference to a node"""

    def __init__(self, key: int):
        super().__init__(basis={key}, dim=0)


class DimDSimplexKey(SimplexKey):
    """A D dimensional simplex key"""

    def __init__(self, basis: Union[set[SimplexKey], frozenset[SimplexKey]], multi: bool = False, count_id: int = None):
        super().__init__(basis=basis, dim=len(basis) - 1, multi=multi, count_id=count_id)


class Triangulation:
    """Triangulation Class, can represent simplicial manifolds."""
    __slots__ = ('_simplices', '_simplex_meta', '_time_size', '_max_index')

    def __init__(self, time_size: int):
        self._simplices = collections.defaultdict(set)
        self._simplex_meta = collections.defaultdict(equivdict.EquivDict)
        self._time_size = time_size
        self._max_index = 0

    def add_simplex(self, key: SimplexKey, **meta):
        """adds a simplex to the triangulation"""
        if key.dim == 0:
            self._max_index += 1

        # if the key is not a node make sure all subkeys are already in the triangulation
        if key.dim != 0:
            for sub_key in key.sub_keys:
                assert sub_key in self._simplices[sub_key.dim], f"Tried to add {key}, but {sub_key} was not yet added to the triangulation"

        self._simplices[key.dim].add(key)

        if key.dim != 0:
            meta['contains'] = key.sub_keys

        # if a new edge is being added, update the order of all attached nodes.
        if key.dim == 1 and key not in self._simplices[key.dim]:
            for sub_key in key:
                meta['order'][sub_key] += 1

        for k, v in meta.items():
            self._simplex_meta[k][key] = v

    def remove_simplex(self, key: SimplexKey):
        """removes a simplex from the triangulation"""
        self._simplices[key.dim].remove(key)
        for _, meta_k in self._simplex_meta.items():
            if key in meta_k.keys:
                del meta_k[key]
        # TODO remove the given key as a valid dict VALUE as well

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

    @property
    def spatial_edges(self):
        return self._simplex_meta["s_type"].dual[(2, 0)]

    @property
    def rank_4_nodes(self):
        return self._simplex_meta["order"].dual[4]

    def contains(self, simplex: SimplexKey, dim: int):
        """

        Args:
            simplex:
            dim:

        Returns:

        """
        if dim == simplex.dim:
            # TODO this assumes simplex belongs to triangulation
            return simplex
        elif dim < simplex.dim:
            return filter_simplices(self.simplex_meta['contains'][simplex], dim=dim)
        else:  # dim > simplex.dim
            dual_contains = self.simplex_meta['contains'].dual[simplex]
            return filter_simplices(dual_contains, dim=dim)

    def flatten(self, simplices: Iterable[SimplexKey]):
        res = set()
        for s in simplices:
            res = res.union(self.contains(s, dim=0))
        return res


def filter_simplices(simplices, dim: int = None):
    return set([s for s in simplices if s.dim == dim])
