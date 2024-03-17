from src.rest_playbook_micro.rest_playbook import RESTPlaybook as RP
from tests.test_assert.playbook_assert_file import TestAssertion

def test_playbook_assert():
    """
    Simple test of an assertion class
    class will try and set `assert_test` property on result
    object to True and then False
    """
    rp = RP(
        "tests/test_assert/simple.playbook",
        "tests/test_assert/simple_test.scenario",
        "tests/test_assert/file_test.vars",
        assertion=TestAssertion()
    )
    results = rp.run_playbook()
    assert results[0].assert_test is True
    assert results[1].assert_test is False
