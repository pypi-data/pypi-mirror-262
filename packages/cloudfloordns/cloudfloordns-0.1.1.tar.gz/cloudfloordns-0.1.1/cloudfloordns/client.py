import json
import logging
import os

import requests

from .domain import Domains
from .record import Records

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

DEFAULT_BASE_URL = "https://apiv2.mtgsy.net/api/v1"


def parse_response(response):
    res = response.json()
    error = res.get("error")
    if error:
        logging.debug(error)
        raise Exception(error.get("description", "Unknown error"))
    return res.get("data")


class BaseClient:
    def __init__(self, username=None, apikey=None, url=DEFAULT_BASE_URL) -> None:
        if not username:
            username = os.environ.get("CLOUDFLOOR_USERNAME", "").strip()
        if not username:
            raise Exception("username required")

        if not apikey:
            apikey = os.environ.get("CLOUDFLOOR_APIKEY", "").strip()
        if not apikey:
            raise Exception("username required")
        self._username = username
        self._apikey = apikey
        self._url = url.rstrip("/")

    def request(self, method, url, data=None, timeout=None):
        if not url.startswith("/"):
            raise Exception(
                f"url '{url}' is invalid: must be a path with a leading '/' "
            )
        if not data:
            data = {}
        data = {
            **data,
            "username": self._username,
            "apikey": self._apikey,
        }
        url = f"{self._url}{url}"
        res = requests.request(
            method,
            url,
            headers=DEFAULT_HEADERS,
            data=json.dumps(data),
            allow_redirects=True,
            timeout=timeout,
        )
        return parse_response(res)

    def get(self, url, data=None, timeout=None):
        return self.request("GET", url, data=data, timeout=timeout)

    def post(self, url, data=None, timeout=None):
        return self.request("POST", url, data=data, timeout=timeout)

    def patch(self, url, data=None, timeout=None):
        return self.request("PATCH", url, data=data, timeout=timeout)

    def delete(self, url, data=None, timeout=None):
        return self.request("DELETE", url, data=data, timeout=timeout)


class Client(BaseClient):
    def __init__(self, username=None, apikey=None, url=DEFAULT_BASE_URL) -> None:
        super().__init__(username=username, apikey=apikey, url=url)
        self.records = Records(self)
        self.domains = Domains(self)
