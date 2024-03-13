from .dassco_test_client import client


def test_can_create_workstation():
    # TODO: Requires a DELETE endpoint to clean up
    pass


def test_can_list_workstations():
    institution_name = "test-institution"
    res = client.workstations.list(institution_name)
    status_code = res.get('status_code')
    workstations = res.get('data')
    assert status_code == 200
    assert isinstance(workstations, list)


def test_can_update_workstation():
    institution_name = "test-institution"
    workstation_name = "ti-ws-01"
    body = {
        'name': workstation_name,
        'status': 'IN_SERVICE'
    }
    res = client.workstations.update(institution_name, workstation_name, body)
    assert res.status_code == 204



