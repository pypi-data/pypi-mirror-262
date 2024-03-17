from src.rest_playbook_micro.rest_playbook import RESTPlaybook as RP

def test_success_playbook():
    rp = RP(
        "tests/test_auth/simple.playbook",
        "tests/test_auth/simple_test.scenario",
        "tests/test_auth/file_test.vars"
    )
    results = rp.run_playbook()
    assert len(results) == 2
    assert results[0].status == 200
    assert results[1].status == 401