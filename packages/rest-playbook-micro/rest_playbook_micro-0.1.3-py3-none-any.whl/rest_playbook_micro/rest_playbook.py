"""
Module providing RESTClient class
"""
import os

from pathlib import Path
from ._scenarios import Scenarios as S
from ._variables import Variables as V
from ._playbook import Playbook as P
from ._result import Result as R
from .assertion import Assertion as A


class RESTPlaybook():
    """Top level class for running playbooks, manages the orchestration
    of each file
    """
    app_name: str = 'rest_playbook_micro'
    config_dir: str = os.path.join(
        str(Path.home()),
        ".config/",
        app_name
    )

    scenario_file: str = ''
    var_file: str = ''
    playbook_file: str = ''

    scenarios: S
    variables: V
    playbook: P
    assertion: A

    def __init__(self,
                 p_file: str = "env.playbook",
                 s_file: str = "env.scenario",
                 v_file: str = "env.vars",
                 auth_file: str = None,
                 assertion: A = None
                 ) -> None:
        """Create a new Playbook object

        :param p_file: File path + name for playbook file
        :param s_file: File path + name for playbook file
        :param v_file: File path + name for playbook file
        """
        self.set_scenario_file(s_file)
        self.set_var_file(v_file)
        self.set_playbook_file(p_file)
        self.assertion = assertion

    def set_playbook_file(self, playbook_file: str) -> None:
        self.playbook_file = playbook_file
        self.generate_playbook(self.playbook_file)

    def generate_playbook(self, playbook_file: str = None) -> None:
        if playbook_file is None:
            playbook_file = self.playbook_file
        self.playbook = P(playbook_file)

    def set_scenario_file(self, scenario_file: str) -> None:
        self.scenario_file = scenario_file
        self.generate_scenarios(self.scenario_file)

    def set_var_file(self, var_file: str) -> None:
        self.var_file = var_file
        self.generate_variables(self.var_file)

    def generate_variables(self, var_file: str) -> None:
        self.variables = V(var_file)

    def generate_scenarios(self, scenario_file: str) -> None:
        self.scenarios = S(scenario_file)

    def run_scenario(self, scenario_name: str) -> R:
        return self.scenarios.run_scenario(
            scenario_name, self.variables
        )

    def run_playbook(self) -> list[R]:
        """Runs the full playbook

        :returns: List of result objects for each play in the book
            or up to the point a failure occured
        """
        return self.playbook.run(self.scenarios,
                                 self.variables,
                                 self.assertion)

    def print(self) -> None:
        self.scenarios.print()
        self.variables.print()
