from .dassco_test_client import client


def test_can_list_pipelines():
    res = client.pipelines.list("ld")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_can_create_pipeline():
    # TODO: Requires a DELETE endpoint to clean up
    pass
