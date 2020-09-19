from .base import ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin


class Products(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "products"


class JournalEntries(CreateAPIMixin):
    collection = "journal_entries"


class Invoices(ListAPIMixin, GetAPIMixin):
    collection = "invoices"


class Customers(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "customers"


class Payments(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "payments"


class PaymentRuns(GetAPIMixin, CreateAPIMixin):
    collection = "payment_runs"


class Credits(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "credits"


class Refunds(ListAPIMixin, GetAPIMixin):
    collection = "refunds"


class Statements(ListAPIMixin, GetAPIMixin):
    collection = "statements"


class Plans(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "plans"


class Coupons(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "coupons"


class Subscriptions(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "subscriptions"


class Orders(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "orders"


class Usages(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "usages"


class Webhooks(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "webhooks"


class BillingRuns(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "billing_runs"


class RevenueSchedules(ListAPIMixin, GetAPIMixin):
    MAX_PAGE_SIZE = 500

    collection = "revenue_schedules"


class BillingSchedules(ListAPIMixin, GetAPIMixin):
    collection = "billing_schedules"


class RevenueRules(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "revenue_rules"


class ChartOfAccounts(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "chart_of_accounts"
