from typing import TYPE_CHECKING, Optional
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

if TYPE_CHECKING:
    from requests import PreparedRequest  # pylint: disable=ungrouped-imports


class TimeoutAdapter(HTTPAdapter):
    """ Adds a default timeout to request Requests. """

    DEFAULT_TIMEOUT = 10

    def __init__(self, *args, **kwargs):
        _timeout = kwargs.pop("timeout", None)

        if _timeout is None:
            self.timeout = self.DEFAULT_TIMEOUT
        else:
            self.timeout = _timeout

        super().__init__(*args, **kwargs)

    def __getstate__(self):
        state = super().__getstate__()

        state["timeout"] = self.timeout

        return state

    def send(
        self, request: "PreparedRequest", *args, **kwargs
    ):  # pragma: no cover # pylint: disable=signature-differs
        kwargs.setdefault("timeout", self.timeout)

        return super().send(request, *args, **kwargs)


retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    backoff_factor=3,
)

timeout_retry_adapter = TimeoutAdapter(max_retries=retry_strategy)

DEFAULT_HEADERS = {"Accept": "application/json"}


def session_factory(session: Optional[Session] = None) -> Session:
    """ Creates or modifies `requests.Session` by attaching a timeout adapter with a retry strategy and default headers. """

    if session is None:
        session = Session()

    session.mount("https://", timeout_retry_adapter)
    session.mount("http://", timeout_retry_adapter)

    session.headers.update(DEFAULT_HEADERS)

    return session
