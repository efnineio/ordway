from .base import ListAPIMixin, GetAPIMixin


class Products(ListAPIMixin, GetAPIMixin):
    collection = "products"


class Invoices(ListAPIMixin, GetAPIMixin):
    collection = "invoices"


class Customers(ListAPIMixin, GetAPIMixin):
    collection = "customers"


class Payments(ListAPIMixin, GetAPIMixin):
    collection = "payments"


class Credits(ListAPIMixin, GetAPIMixin):
    collection = "credits"


class Refunds(ListAPIMixin, GetAPIMixin):
    collection = "refunds"


class Plans(ListAPIMixin, GetAPIMixin):
    collection = "plans"


class Subscriptions(ListAPIMixin, GetAPIMixin):
    collection = "subscriptions"
