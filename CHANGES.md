# Changes

## [0.2.0] - 2020-09-19

- Added new entities:
  * JournalEntries
  * PaymentRuns
  * Statements
  * Coupons
  * Orders
  * Usages
  * BillingRuns
  * RevenueSchedules
  * BillingSchedules
  * RevenueRules
  * ChartOfAccounts
- Bug fixes
  * Pass page size from `ListAPIMixin.all` to `ListAPIMixin.list`
  * Unnecessary `GeneratorExit` exception

## [0.1.0] - 2020-09-03

- Set Accept header to *application/json* by default for `ordway.client.OrdwayClient`'s session
- Attached a custom `requests.adapters.HTTPAdapter` to handle retries and HTTP timeouts
- Functionality for using a context manager with `ordway.client.OrdwayClient` added