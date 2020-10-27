from typing import TYPE_CHECKING, Optional, List, Dict, Any, Generator, Union, Tuple
from logging import getLogger
from requests.exceptions import RequestException
from ordway.consts import API_ENDPOINT_BASE, STAGING_ENDPOINT_BASE
from ordway.utils import transform_datetimes

from .exceptions import OrdwayAPIRequestException, OrdwayAPIException

if TYPE_CHECKING:
    from ordway.client import OrdwayClient  # pylint: disable=cyclic-import

logger = getLogger(__name__)

_Response = Union[List[Dict[str, Any]], Dict[str, Any]]


class APIBase:
    collection: str

    def __init__(self, client: "OrdwayClient", staging: bool = False):
        self.client = client
        self.session = client.session
        self.staging = staging

    def _construct_headers(self) -> Dict[str, str]:
        """ Returns a dictionary of headers Ordway always expects for API requests. """

        return {
            "X-User-Company": self.client.company,
            "X-API-Key": self.client.api_key,
            "X-User-Token": self.client.user_token,
            "X-User-Email": self.client.email,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _request(  # pylint: disable=too-many-arguments
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, str]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> _Response:
        if self.staging:
            base = STAGING_ENDPOINT_BASE
        else:
            base = API_ENDPOINT_BASE

        json, data = transform_datetimes(json), transform_datetimes(data)

        url = f"{base}/v{self.client.api_version}/{endpoint}"

        logger.debug(
            'Sending a request to Ordway endpoint "%s" with the following query params: %s',
            endpoint,
            params,
        )

        # Ensure any changes to client attrs are reflected in headers on request.
        self.session.headers.update(self._construct_headers())

        try:
            response = self.session.request(
                method=method, url=url, params=params, data=data, json=json
            )

            response.raise_for_status()

            return response.json()
        except RequestException as err:
            raise OrdwayAPIRequestException(
                str(err), request=err.request, response=err.response
            ) from err
        except ValueError as err:
            raise OrdwayAPIRequestException(
                "Ordway returned HTTP success, but no valid JSON was present. Please report this as an issue on GitHub."
            ) from err

    def _get_request(
        self, endpoint: str, params: Optional[Dict[str, str]] = None
    ) -> _Response:
        return self._request("GET", endpoint, params=params)

    def _post_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> _Response:
        if json is None and data is None:
            raise ValueError("Either `json` or `data` must be passed to post_request.")

        return self._request("POST", endpoint, json=json, data=data, params=params)

    def _put_request(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> _Response:
        return self._request("PUT", endpoint, json=json, data=data, params=params)


def _remove_order_from_sort(sort_str: str) -> Tuple[str, Optional[bool]]:
    sort_str = sort_str.lower()

    if sort_str.endswith(" asc"):
        return (sort_str[:-4], True)
    if sort_str.endswith(" desc"):
        return (sort_str[:-5], False)

    return (sort_str, None)


class ListAPIMixin(APIBase):
    """ Mixin for retrieving a collection of Ordway resources. """

    MAX_PAGE_SIZE = 50
    MAX_PAGES = 1000

    def list(  # pylint: disable=too-many-arguments
        self,
        page: int,
        size: int = 20,
        sort: str = "",
        filters: Optional[Dict[str, Any]] = None,
        ascending: bool = False,
    ) -> Generator[Dict[str, Any], None, None]:
        """ Retrieve a single page of resource from a collection """

        if size > self.MAX_PAGE_SIZE:
            logger.warning(
                'Maximum page size for "%s" is %s, setting `size` to maximum.',
                self.collection,
                self.MAX_PAGE_SIZE,
            )

            size = self.MAX_PAGE_SIZE

        filters = {} if filters is None else filters
        params: Dict[str, str] = {"size": str(size), "page": str(page), **filters}

        # Ordway appends order onto the end of the sort string. It's best
        # to ensure that if a user does, we remove it. Sice we're going to
        # append it later.
        sort, order = _remove_order_from_sort(sort)

        if order is not None:
            ascending = order

        if len(sort.strip()) > 0:
            params["sort"] = f"{sort} {'asc' if ascending else 'desc'}"

        response_json = self._get_request(
            self.collection,
            params=params,
        )

        if isinstance(response_json, dict):
            response_json = [response_json]

        # Mostly for consistency's sake.
        for result in response_json:
            yield result

        if len(response_json) < size:
            self._exhausted = True

    def all(  # pylint: disable=too-many-arguments
        self,
        size: int = 20,
        sort: str = "",
        filters: Optional[Dict[str, Any]] = None,
        ascending: bool = False,
        ignore_max_pages: bool = False,
    ) -> Generator[Dict[str, Any], None, None]:
        """ Retrieve all resources from a collection """

        page = 1

        self._exhausted = False

        # Maybe separate into Paginator class? Could be needed elsewhere.
        while True:
            if not ignore_max_pages and page >= self.MAX_PAGES:
                logger.warning(
                    "Call to `.all()` has reached the maximum number of pages (%s). If this is desirable, please call with `ignore_max_pages` set to True.",
                    self.MAX_PAGES,
                )

                break

            yield from self.list(
                page=page,
                size=size,
                sort=sort,
                filters=filters,
                ascending=ascending,
            )

            if self._exhausted:
                break

            page += 1


class GetAPIMixin(APIBase):
    """ Mixin for retrieving a single Ordway resource. """

    def get(self, id: str) -> Dict[str, Any]:
        """ Retrieve a particular resource """

        response_json = self._get_request(f"{self.collection}/{id}")

        if isinstance(response_json, list):
            if len(response_json) == 1:
                return response_json[0]

            raise OrdwayAPIException(
                "Call to `.get_request` returned an unexpected JSON array. Please report this as an issue on GitHub."
            )

        return response_json


class CreateAPIMixin(APIBase):
    """ Mixin for creating a single Ordway resource. """

    def create(
        self, data: Optional[Dict[str, Any]], params: Optional[Dict[str, str]] = None
    ) -> _Response:
        """ Create a new resource """

        return self._post_request(self.collection, json=data, data=None, params=params)


class UpdateAPIMixin(APIBase):
    """ Mixin for updating a single Ordway resource. """

    def update(
        self,
        id: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, str]] = None,
    ) -> _Response:
        """ Update a resource identified by `id`. """

        return self._put_request(
            f"{self.collection}/{id}", json=data, data=None, params=params
        )


class DeleteAPIMixin(APIBase):
    """ Mixin for deleting a single Ordway resource. """

    def delete(self, id: str) -> _Response:
        """ Delete a resource identified by `id`. """

        return self._request("DELETE", f"{self.collection}/{id}")


__all__ = [
    "APIBase",
    "ListAPIMixin",
    "GetAPIMixin",
    "CreateAPIMixin",
    "UpdateAPIMixin",
    "DeleteAPIMixin",
]
