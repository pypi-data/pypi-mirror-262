from src.rest_playbook_micro.rest_playbook import RESTPlaybook as RP


def test_status():
    rp = RP(
        "tests/test_status/simple.playbook",
        "tests/test_status/simple_test.scenario",
        "tests/test_status/file_test.vars"
    )
    results = rp.run_playbook()
    assert len(results) == 2
    assert results[0].status == 200
    assert rp.playbook.plays[0].valid_status() is True
    assert results[1].status == 404
    assert rp.playbook.plays[1].valid_status() is False
