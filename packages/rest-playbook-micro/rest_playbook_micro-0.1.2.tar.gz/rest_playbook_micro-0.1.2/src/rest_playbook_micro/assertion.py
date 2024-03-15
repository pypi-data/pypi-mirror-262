from ._variables import Variables as V
from ._play import Play as P


class Assertion():

    def __init__(self) -> None:
        pass

    def run_assert(self, play: P, variables: V) -> bool:

        match play.STEP:
            case _:
                return self.run_01(play, variables)

    def get_variable(self, variables: V, var_name: str):
        pass

    def run_01(self, play: P, variables: V) -> bool:
        return True
