
from src.rest_playbook_micro.assertion import Assertion
from src.rest_playbook_micro._play import Play as P


class TestAssertion(Assertion):

    def __init__(self) -> None:
        pass

    def run_assert(self, play: P, variables) -> bool:

        match play.STEP:
            case '1':
                self.run_01(play, variables)
            case '2':
                self.run_02(play, variables)
            case _:
                pass

        return True

    def run_01(self, play: P, variables) -> bool:
        play.result.assert_test = True
        return True

    def run_02(self, play: P, variables) -> bool:
        play.result.assert_test = False
        return True
