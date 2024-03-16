# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105


"objects library"


from .decoder import loads
from .default import Default
from .encoder import dumps
from .objects import *


"interface"


def __dir__():
    return (
        'Default',
        'Object',
        'construct',
        'dumps',
        'edit',
        'fmt',
        'fqn',
        'ident',
        'items',
        'keys',
        'loads',
        'search',
        'update',
        'values'
    )
