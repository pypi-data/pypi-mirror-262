"""
Run dynamic and ordered REST transactions
"""

from .rest_playbook import RESTPlaybook
from .assertion import Assertion
from ._play import Play

VERSION = (0, 1, 2)

VERSION_STRING = ".".join(map(str, VERSION))

RESTPlaybook

Assertion

Play
