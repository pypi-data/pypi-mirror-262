import time
from ._result import Result as R
from ._scenarios import Scenarios as S
from ._variables import Variables as V


class Play():
    """
    Invidual step in a playbook, does not have direct knowledge of the
    scenario it relates to, but instead a unique reference to a name.
    Manages parsing of the response and time to the next step
    """

    NAME: str
    WAIT: int
    ASSERT: str
    STEP: str
    # For testing purposes we can have the outbound body
    # put back into the play object
    RETURN_BODY: bool
    NEXT_STEP: str
    VALID_STATUS: list
    result: R
    scenario: S

    def __init__(self,
                 name: str,
                 step: str,
                 assert_exec: str,
                 valid_status: list[str],
                 next_step: str = None,
                 wait: int = 30,
                 return_body: bool = False) -> None:
        if name:
            self.NAME = name
        if step:
            self.STEP = step
        if assert_exec:
            self.ASSERT = assert_exec
        if valid_status:
            self.VALID_STATUS = valid_status
        else:
            self.VALID_STATUS = []
        self.NEXT_STEP = next_step
        self.WAIT = wait
        self.RETURN_BODY = return_body

    def run(self, scenarios: S, variables: V) -> R:
        self.result = scenarios.run_scenario(
            self.NAME, variables, return_body=self.RETURN_BODY)
        self.valid_status()
        time.sleep(self.WAIT)
        return self.result

    def valid_status(self) -> None:
        if str(self.result.status) in self.VALID_STATUS:
            self.result.valid = True
        return self.result.valid
