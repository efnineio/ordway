from typing import Optional, Dict, Union
from requests.exceptions import RequestException
from ordway.exceptions import OrdwayClientException


class OrdwayAPIException(OrdwayClientException):
    """ Base exception for all Ordway API errors. """


class OrdwayAPIRequestException(OrdwayAPIException, RequestException):
    """ An Ordway API exception with the `errors` object easily accessible, if it was returned in API response body. """

    def __init__(self, *args, **kwargs):
        self.errors: Optional[
            Dict[str, Union[int, str, Dict[str, Dict[str, str], str]]]
        ] = kwargs.pop("errors", None)

        if self.errors is None:
            # Attempt to grab errors from response.
            response = kwargs.get("response")

            if response is not None:
                try:
                    response_json = response.json()

                    self.errors = response_json.get("errors")
                except ValueError:
                    pass

        if self.errors is not None:
            args = (self.errors, *args)

        super().__init__(*args, **kwargs)
