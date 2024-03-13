from .dassco_test_client import client


def test_can_create_institution():
    # TODO: Requires a DELETE endpoint to clean up
    pass


def test_can_list_institutions():
    res = client.institutions.list()
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_can_call_get_institution():
    institution_name = "test-institution"
    res = client.institutions.get(institution_name)
    institution = res.json()
    assert res.status_code == 200
    assert institution["name"] == institution_name
