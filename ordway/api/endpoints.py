from typing import Dict, Optional, Any
from .base import (
    ListAPIMixin,
    GetAPIMixin,
    CreateAPIMixin,
    DeleteAPIMixin,
    UpdateAPIMixin,
)


class Products(
    ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, UpdateAPIMixin
):
    """Interface for interacting with Ordway Products

    Documentation: https://ordwaylabs.api-docs.io/v1/products/list-products
    """

    collection = "products"


class JournalEntries(CreateAPIMixin):
    """Interface for interacting with Ordway Journal Entries

    Documentation: https://ordwaylabs.api-docs.io/v1/journal-entries
    """

    collection = "journal_entries"


class Invoices(ListAPIMixin, GetAPIMixin):
    """Interface for interacting with Ordway Invoices

    Documentation: https://ordwaylabs.api-docs.io/v1/invoices
    """

    collection = "invoices"

    def reverse(self, id: str, reversed_on: str):
        """ Reverse an invoice """

        return self._put_request(
            f"{self.collection}/{id}/reverse", json={"reversed_on": reversed_on}
        )

    def refund(self, id: str, data: Dict[str, Any]):
        """ Refund a negative invoice """

        return self._put_request(f"{self.collection}/{id}/refund", json=data)


class Customers(
    ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, UpdateAPIMixin
):
    """Interface for interacting with Ordway Customers

    Documentation: https://ordwaylabs.api-docs.io/v1/customers
    """

    collection = "customers"


class Payments(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    """Interface for interacting with Ordway Payments

    Documentation: https://ordwaylabs.api-docs.io/v1/payments
    """

    collection = "payments"

    def reverse(self, id: str, reversed_on: str):
        """ Reverse a payment """

        return self._put_request(
            f"{self.collection}/{id}/reverse", json={"reversed_on": reversed_on}
        )

    def refund(self, id: str, data: Dict[str, Any]):
        """ Refund a payment """

        return self._put_request(f"{self.collection}/{id}/refund", json=data)


class PaymentRuns(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    """Interface for interacting with Ordway Payment Runs

    Payment Runs are operations that automatically generate payments during a set interval.

    Documentation: https://ordwaylabs.api-docs.io/v1/payment-runs
    """

    collection = "payment_runs"

    def reverse(self, id: str):
        """ Reverse a payment run """

        return self._put_request(f"{self.collection}/{id}/reverse", json={})


class Credits(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    """Interface for interacting with Ordway Credits

    Documentation: https://ordwaylabs.api-docs.io/v1/credits
    """

    collection = "credits"

    def reverse(self, id: str, reversed_on: str):
        """ Reverse a credit """

        return self._put_request(
            f"{self.collection}/{id}/reverse", json={"reversed_on": reversed_on}
        )

    def refund(self, id: str, data: Dict[str, Any]):
        """ Refund a credit """

        return self._put_request(f"{self.collection}/{id}/refund", json=data)


class Refunds(ListAPIMixin, GetAPIMixin):
    """Interface for interacting with Ordway Refunds

    Documentation: https://ordwaylabs.api-docs.io/v1/refunds
    """

    collection = "refunds"


class Statements(ListAPIMixin, GetAPIMixin):
    """Interface for interacting with Ordway Statements

    Statements allow you to send customers information about their account.

    Documentation: https://ordwaylabs.api-docs.io/v1/statements
    """

    collection = "statements"


class Plans(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, UpdateAPIMixin):
    """Interface for interacting with Ordway Plans

    Plans are collection of charges grouped together.

    Documentation: https://ordwaylabs.api-docs.io/v1/plans
    """

    collection = "plans"


class Coupons(ListAPIMixin, GetAPIMixin, CreateAPIMixin, UpdateAPIMixin):
    """Interface for interacting with Ordway Coupons

    Documentation: https://ordwaylabs.api-docs.io/v1/coupons
    """

    collection = "coupons"


class Subscriptions(
    ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, UpdateAPIMixin
):
    """Interface for interacting with Ordway Subscriptions

    Documentation: https://ordwaylabs.api-docs.io/v1/subscriptions
    """

    collection = "subscriptions"

    def activate(self, id: str, data: Dict[str, Any]):
        """ Activate a subscription """

        return self._put_request(f"{self.collection}/{id}/activate", json=data)

    def cancel(self, id: str, data: Dict[str, Any]):
        """ Cancel a subscription """

        return self._put_request(f"{self.collection}/{id}/cancel", json=data)

    def renew(self, id: str, data: Dict[str, Any], callback_url: Optional[str] = None):
        """ Renew a subscription """

        params = {"callback_url": callback_url} if callback_url is not None else None

        return self._put_request(
            f"{self.collection}/{id}/cancel", json=data, params=params
        )

    def change(self, id: str, data: Dict[str, Any], callback_url: Optional[str] = None):
        """ Change an active subscription """

        params = {"callback_url": callback_url} if callback_url is not None else None

        return self._put_request(
            f"{self.collection}/{id}/change", json=data, params=params
        )


class Orders(ListAPIMixin, GetAPIMixin, CreateAPIMixin, UpdateAPIMixin):
    """Interface for interacting with Ordway Orders

    Documentation: https://ordwaylabs.api-docs.io/v1/orders
    """

    collection = "orders"

    def cancel(self, id: str, data: Optional[Dict[str, Any]] = None):
        """ Cancel an order """

        return self._put_request(f"{self.collection}/{id}/cancel", json=data)


class Usages(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    """Interface for interacting with Ordway Usages

    Usage is the amount of units a customer uses and is always billed in arrears.

    Documentation: https://ordwaylabs.api-docs.io/v1/usages
    """

    collection = "usages"


class Webhooks(
    ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, UpdateAPIMixin
):
    """Interface for interacting with Ordway Webhooks

    Documentation: https://ordwaylabs.api-docs.io/v1/webhooks
    """

    collection = "webhooks"


class BillingRuns(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    """Interface for interacting with Ordway Billing Runs

    Documentation: https://ordwaylabs.api-docs.io/v1/billing-runs
    """

    collection = "billing_runs"


class RevenueSchedules(ListAPIMixin, GetAPIMixin):
    """Interface for interacting with Ordway Revenue Schedules

    Documentation: https://ordwaylabs.api-docs.io/v1/revenue-schedules
    """

    MAX_PAGE_SIZE = 500

    collection = "revenue_schedules"


class BillingSchedules(ListAPIMixin, GetAPIMixin, UpdateAPIMixin):
    """Interface for interacting with Ordway Billing Schedules

    Billing Schedules show how customers will be billed/invoiced over the
    course of time for a specific subscription contract.

    Documentation: https://ordwaylabs.api-docs.io/v1/billing-schedules
    """

    collection = "billing_schedules"

    def manage_prepayment_lines(self, id: str, data: Dict[str, Any]):
        """ Manage prepaid credits, allowing addition or refund of prepaid credits """

        return self._put_request(
            f"{self.collection}/{id}/manage_prepayment_lines", json=data
        )


class RevenueRules(
    ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, UpdateAPIMixin
):
    """Interface for interacting with Ordway Revenue Rules

    Documentation: https://ordwaylabs.api-docs.io/v1/revenue-rules
    """

    collection = "revenue_rules"


class ChartOfAccounts(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    """Interface for interacting with Ordway Chart of Accounts

    Documentation: https://ordwaylabs.api-docs.io/v1/chart-of-accounts
    """

    collection = "chart_of_accounts"
