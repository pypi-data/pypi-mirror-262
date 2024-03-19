"""KDB.AI Client for Python."""

from importlib.metadata import PackageNotFoundError, version

from .api import _set_version, KDBAIException, MAX_DATETIME, MIN_DATETIME, Session, Table  # noqa


try:
    __version__ = version('kdbai_client')
    if "dev" in __version__:
        __version__ = 'dev'
except PackageNotFoundError:  # pragma: no cover
    __version__ = 'dev'
_set_version(__version__)


__all__ = sorted(['__version__', 'KDBAIException', 'MIN_DATETIME', 'MAX_DATETIME', 'Session', 'Table'])


def __dir__():
    return __all__
