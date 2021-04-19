"""Package-level information"""
__MAJOR__ = 0
__MINOR__ = 0
__MICRO__ = 2
__VERSION__ = (__MAJOR__, __MINOR__, __MICRO__)
__version__ = '.'.join(str(n) for n in __VERSION__)
__github_url__ = 'https://github.com/JWKennington/cdtea'

from cdtea.tests import run_tests  # top level function for running test suite, analogous to scipy.test()
