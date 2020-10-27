from typing import Any
from datetime import datetime, date


def transform_datetimes(data: Any) -> Any:
    """ Converts any date or datetime objects to string via their `isoformat` methods. """

    if isinstance(data, (datetime, date)):
        return data.isoformat()

    if isinstance(data, (list, tuple)):
        tmp_data = [transform_datetimes(elem) for elem in data]

        return tuple(tmp_data) if isinstance(data, tuple) else tmp_data

    if isinstance(data, dict):
        for key, val in data.items():
            data[key] = transform_datetimes(val)

    return data
