import requests
from enum import Enum
from .exceptions.api_error import APIError


class RequestMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


def send_request(method: RequestMethod, token: str, path: str, json: dict = None):
    """
        Sends a request to the DaSSCo Storage API with the given parameters

        Args:
            method (RequestMethod): The HTTP request method: GET, POST, PUT or DELETE
            token (str): A valid access token obtained from a successful authentication
            path (str): The resource endpoint
            json (dict): A dictionary that contains the json body sent with the request. The value is None by default.

        Returns:
            A dictionary containing the response data and status code.
    """
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/json',
    }

    api_url = f"https://storage.test.dassco.dk/api{path}"

    res = requests.request(method.name, headers=headers, url=api_url, json=json)

    if 200 <= res.status_code <= 299:
        return res
    else:
        raise APIError(res)


def send_request_to_file_proxy(method: RequestMethod, token: str, path: str, data=None):
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': 'application/octet-stream' if method == RequestMethod.PUT else 'application/json',
    }

    api_url = f"https://storage.test.dassco.dk/file_proxy/api{path}"

    res = requests.request(method.name, headers=headers, url=api_url, data=data)

    if 200 <= res.status_code <= 299:
        return res
    else:
        raise APIError(res)
