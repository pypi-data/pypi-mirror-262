from .dassco_test_client import client


def test_can_list_collections():
    res = client.collections.list("ld")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_can_create_collection():
    # TODO: Requires a DELETE endpoint to clean up
    pass
