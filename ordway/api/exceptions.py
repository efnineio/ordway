from typing import Optional, Dict, Union
from ordway.exceptions import OrdwayClientException
from requests.exceptions import RequestException


class OrdwayAPIException(OrdwayClientException):
    """ Base exception for all Ordway API errors. """


class OrdwayAPIRequestException(OrdwayAPIException, RequestException):
    def __init__(self, *args, **kwargs):
        """ Initalizes an OrdwayAPIRequestException with `errors` object easily accessible, if returned. """

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
