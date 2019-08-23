# TODO this is hacky and should be done in a better way
from sqlalchemy.sql.schema import ForeignKey

# prevents recursion
_init = ForeignKey.__init__


def _deferrable_init(*args, deferrable=True, **kwargs):
    """sets deferrable to true by default"""

    return _init(*args, deferrable=deferrable, **kwargs)


ForeignKey.__init__ = _deferrable_init
