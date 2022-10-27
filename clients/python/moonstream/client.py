import uuid
from typing import Any, Dict, Union

import requests

from .data import (
    APISpec,
    AuthType,
    Method,
    MoonstreamQueries,
    MoonstreamQuery,
    MoonstreamQueryResultUrl,
)
from .exceptions import MoonstreamResponseException, MoonstreamUnexpectedResponse
from .settings import MOONSTREAM_API_URL, MOONSTREAM_REQUEST_TIMEOUT

ENDPOINT_PING = "/ping"
ENDPOINT_VERSION = "/version"
ENDPOINT_NOW = "/now"
ENDPOINT_QUERIES = "/queries"

ENDPOINTS = [
    ENDPOINT_PING,
    ENDPOINT_VERSION,
    ENDPOINT_NOW,
    ENDPOINT_QUERIES,
]


def moonstream_endpoints(url: str) -> Dict[str, str]:
    """
    Creates a dictionary of Moonstream API endpoints at the given Moonstream API URL.
    """
    if not (url.startswith("http://") or url.startswith("https://")):
        url = f"http://{url}"

    normalized_url = url.rstrip("/")

    return {endpoint: f"{normalized_url}{endpoint}" for endpoint in ENDPOINTS}


class Moonstream:
    """
    A Moonstream client configured to communicate with a given Moonstream API server.
    """

    def __init__(self, moonstream_api_url: str = MOONSTREAM_API_URL):
        """
        Initializes a Moonstream API client.

            Arguments:
            url - Moonstream API URL. By default this points to the production Moonstream API at https://api.moonstream.to,
            but you can replace it with the URL of any other Moonstream API instance.
        """
        endpoints = moonstream_endpoints(moonstream_api_url)
        self.api = APISpec(url=moonstream_api_url, endpoints=endpoints)

    def _call(
        self,
        method: Method,
        url: str,
        timeout: float = MOONSTREAM_REQUEST_TIMEOUT,
        **kwargs,
    ):
        try:
            response = requests.request(
                method.value, url=url, timeout=timeout, **kwargs
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as err:
            r = err.response
            if not err.response:
                # Connection errors, timeouts, etc...
                raise MoonstreamResponseException(
                    "Network error", status_code=599, detail=str(err)
                )
            if r.headers.get("Content-Type") == "application/json":
                exception_detail = r.json()["detail"]
            else:
                exception_detail = r.text
            raise MoonstreamResponseException(
                "An exception occurred at Bugout API side",
                status_code=r.status_code,
                detail=exception_detail,
            )
        except Exception as e:
            raise MoonstreamUnexpectedResponse(str(e))
        return response.json()

    def ping(self) -> Dict[str, Any]:
        """
        Checks that you have a connection to the Moonstream API.
        """
        result = self._call(method=Method.GET, url=self.api.endpoints[ENDPOINT_PING])
        return result

    def version(self) -> Dict[str, Any]:
        """
        Gets the Moonstream API version information from the server.
        """
        result = self._call(method=Method.GET, url=self.api.endpoints[ENDPOINT_VERSION])
        return result

    def create_query(
        self,
        token: Union[str, uuid.UUID],
        query: str,
        name: str,
        public: bool = False,
        auth_type: AuthType = AuthType.bearer,
        timeout: float = MOONSTREAM_REQUEST_TIMEOUT,
    ) -> MoonstreamQuery:
        """
        Creates new query.
        """
        json = {
            "query": query,
            "name": name,
            "public": public,
        }
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        response = self._call(
            method=Method.POST,
            url=f"{self.api.endpoints[ENDPOINT_QUERIES]}",
            headers=headers,
            json=json,
            timeout=timeout,
        )

        return MoonstreamQuery(
            id=response["id"],
            journal_url=response["journal_url"],
            name=response["title"],
            query=response["content"],
            tags=response["tags"],
            created_at=response["created_at"],
            updated_at=response["updated_at"],
        )

    def list_queries(
        self,
        token: Union[str, uuid.UUID],
        auth_type: AuthType = AuthType.bearer,
        timeout: float = MOONSTREAM_REQUEST_TIMEOUT,
    ) -> MoonstreamQueries:
        """
        Returns list of all queries available to user.
        """
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        response = self._call(
            method=Method.GET,
            url=f"{self.api.endpoints[ENDPOINT_QUERIES]}/list",
            headers=headers,
            timeout=timeout,
        )

        return MoonstreamQueries(
            queries=[
                MoonstreamQuery(
                    id=query["entry_id"],
                    name=query["name"],
                    query_type=query["type"],
                    user=query["user"],
                    user_id=query["user_id"],
                )
                for query in response
            ]
        )

    def exec_query(
        self,
        token: Union[str, uuid.UUID],
        name: str,
        params: Dict[str, Any] = {},
        auth_type: AuthType = AuthType.bearer,
        timeout: float = MOONSTREAM_REQUEST_TIMEOUT,
    ) -> MoonstreamQueryResultUrl:
        """
        Executes queries and upload data to external storage.
        """
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        json = {
            "params": params,
        }
        response = self._call(
            method=Method.POST,
            url=f"{self.api.endpoints[ENDPOINT_QUERIES]}/{name}/update_data",
            headers=headers,
            json=json,
            timeout=timeout,
        )

        return MoonstreamQueryResultUrl(url=response["url"])

    def delete_query(
        self,
        token: Union[str, uuid.UUID],
        name: str,
        auth_type: AuthType = AuthType.bearer,
        timeout: float = MOONSTREAM_REQUEST_TIMEOUT,
    ) -> uuid.UUID:
        """
        Deletes query specified by name.
        """
        headers = {
            "Authorization": f"{auth_type.value} {token}",
        }
        response = self._call(
            method=Method.DELETE,
            url=f"{self.api.endpoints[ENDPOINT_QUERIES]}/{name}",
            headers=headers,
            timeout=timeout,
        )

        return response["id"]
