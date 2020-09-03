# Changes

## [0.1.0] - 2020-09-03

- Set Accept header to *application/json* by default for `ordway.client.OrdwayClient`'s session
- Attached a custom `requests.adapters.HTTPAdapter` to handle retries and HTTP timeouts
- Functionality for using a context manager with `ordway.client.OrdwayClient` added