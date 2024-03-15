from typing import *
import requests

from ..utils.env import env_with_fallback
from ..utils.classproperty import classproperty
from .credentials import get_client_credentials


class HashboardAPI:
    def __init__(self) -> None:
        raise AssertionError("HashboardAPI is a singleton.")

    @classproperty
    def base_uri(self):
        return (
            env_with_fallback("HASHQUERY_API_BASE_URI", "HASHBOARD_CLI_BASE_URI")
            or "https://hashboard.com"
        )

    @classproperty
    def credentials(self):
        result = get_client_credentials()
        if not result:
            raise RuntimeError(
                "Could not authenticate to Hashboard services. "
                + "No credentials were found."
            )
        return result

    @classproperty
    def project_id(self):
        return self.credentials.project_id

    @classmethod
    def post(self, route: str, payload: dict):
        response = requests.post(
            f"{self.base_uri}/{route}",
            json=payload,
            headers=self.credentials.get_headers(),
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"Request failed with status code {response.status_code}. Response:\n"
                + response.text
            )

    @classmethod
    def graphql(self, query, variables=None):
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        return self.post("graphql/", payload)
