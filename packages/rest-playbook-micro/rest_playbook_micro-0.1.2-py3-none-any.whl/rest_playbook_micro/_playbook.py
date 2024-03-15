
import sys

from itertools import groupby
from ._utils import utils
from ._play import Play as P
from ._result import Result as R
from ._scenarios import Scenarios as S
from ._variables import Variables as V
from .assertion import Assertion as A


class Playbook():
    """Parent playbook class, manages each of the steps provided
    """

    plays: list[P]
    u: utils = utils()
    assertion = None

    def __init__(self, playbook_file: str = None) -> None:
        self._parse_playbook_file(playbook_file)
        self.step = None

    def _parse_playbook_file(self, file: str):
        self.plays = self._parse_play_list(file)

    def _parse_play_list(self, file: str):
        playbook_blocks = self._split_playbook_file(file)
        return list(map(self._parse_block, playbook_blocks))

    def _split_playbook_file(self, file: str) -> list:
        raw_data = self.u.load_file(file)
        split_scenarios = [list(g) for k, g in groupby(
            raw_data, key=lambda x: x != "----") if k]
        return split_scenarios

    def _parse_block(self, entry: list):

        props = self.u.set_properties(entry)
        if props.get('NAME', None) is None:
            raise ValueError("Play is missing NAME")
        p = P(
            name=props.get('NAME'),
            wait=int(props.get('WAIT', 30)),
            step=props.get('STEP'),
            assert_exec=props.get('ASSERT'),
            next_step=props.get('NEXT_STEP', None),
            valid_status=str(props.get('VALID_STATUS', '')).split(',')
        )
        return p

    def run(self, scenarios: S, variables: V, assertion: A) -> list[R]:
        ret_val: list[R] = []
        iterator = 0
        for p in self.plays:
            ret_val.append(p.run(scenarios, variables))
            if not p.valid_status:
                return ret_val
            if assertion and not assertion.run_assert(play=p, variables=variables):
                return ret_val
            iterator += 1
            if iterator > 500:
                return ret_val
        return ret_val
