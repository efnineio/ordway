from .base import ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin, _Response
from typing import Dict, Any, Optional, Union, List


class Products(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "products"


class Invoices(ListAPIMixin, GetAPIMixin):
    collection = "invoices"


class Customers(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "customers"


class Payments(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "payments"


class Credits(ListAPIMixin, GetAPIMixin, CreateAPIMixin):
    collection = "credits"


class Refunds(ListAPIMixin, GetAPIMixin):
    collection = "refunds"


class Plans(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "plans"


class Subscriptions(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "subscriptions"


class Webhooks(ListAPIMixin, GetAPIMixin, CreateAPIMixin, DeleteAPIMixin):
    collection = "webhooks"
