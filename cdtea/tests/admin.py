"""Test harness utilities
"""
import functools

from cdtea import simplicial


def _clean_scope():
    """Utility for cleaning test scope"""
    simplicial.SimplexKey.flush_counts()


def clean_scope(f):
    """Decorator for cleaning test scope"""

    @functools.wraps(f)
    def new(*args, **kwargs):
        """New function"""
        _clean_scope()
        return f(*args, **kwargs)

    return new


class CleanScope:
    """Clean scope class"""

    def setup_method(self):
        """please work"""
        _clean_scope()
