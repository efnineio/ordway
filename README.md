# Ordway

[![PyPi Version](https://img.shields.io/pypi/v/ordway.svg)](https://pypi.org/project/ordway)
[![Supported Versions](https://img.shields.io/pypi/pyversions/ordway.svg)](https://pypi.org/project/ordway)
[![MIT License](https://img.shields.io/pypi/l/ordway)](https://raw.githubusercontent.com/efnineio/ordway/v0.4.0/LICENSE)

Ordway is a simple API wrapper for [Ordway](https://www.ordwaylabs.com/). It's currently in pre-alpha stage, so be wary if you decide to use this in production. Please report any issues you encounter.

## Installation

The easiest way to install ordway is via [pip](https://pypi.python.org/pypi/pip).

```bash
pip install ordway
```

## Quickstart

```python
from ordway import OrdwayClient

ordway = OrdwayClient(
    email="EMAIL",
    user_token="USER_TOKEN",
    api_key="API_KEY",
    company="COMPANY",
)

for payment in ordway.payments.all():
    print(payment)

for subscription in ordway.subscriptions.list(
    page = 1, 
    filters = { "updated_date>": "2020-01-01" }, 
    sort="updated_date", 
    ascending=False
):
    print(subscription)

print(ordway.customers.get(id="CUST-01"))

ordway.customers.create(data={
    "name": "Jason",
    "description": "Hello",
    "contacts": [{
        "first_name": "Jason"
    }],
    ...
})
```

## Documentation

**TODO**
