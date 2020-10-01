# Changes

## [0.4.0] - 2020-09-22

- Added support for updating following entities:
  * Products
  * Customers
  * Plans
  * Coupons
  * Subscriptions
  * Orders
  * Webhooks
  * BillingSchedules
  * RevenueRules
  * Invoices
  * Payments
  * PaymentRuns
  * Credits

- Bug fixes
  * Passing no `sort` argument to `ListAPIMixin.all` to `ListAPIMixin.list` caused an Ordway API error. 
  * Entities added in 0.2.0 were not instantiated on the `ordway.Client`, rendering them unusable.

## [0.3.0] - 2020-09-21

- Added support for staging enviornment by passing `staging=True` to `ordway.client.OrdwayClient`

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