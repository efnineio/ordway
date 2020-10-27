from unittest import TestCase
from requests import Session
from datetime import datetime, date, timezone
from ordway.utils import transform_datetimes


class TransformDatetimes(TestCase):
    def test_with_dict(self):
        transformed_data = transform_datetimes(
            {
                "a": datetime(2020, 1, 2, tzinfo=timezone.utc),
                "b": [[datetime(2020, 1, 2)]],
                "c": [
                    {
                        "d": {
                            "date": datetime(2020, 1, 2),
                            "dates": [
                                datetime(2020, 1, 2),
                                datetime(2020, 1, 2),
                                datetime(2020, 1, 2),
                            ],
                        }
                    }
                ],
            }
        )

        self.assertIsInstance(transformed_data, dict)
        self.assertDictEqual(
            {
                "a": "2020-01-02T00:00:00+00:00",
                "b": [["2020-01-02T00:00:00"]],
                "c": [
                    {
                        "d": {
                            "date": "2020-01-02T00:00:00",
                            "dates": [
                                "2020-01-02T00:00:00",
                                "2020-01-02T00:00:00",
                                "2020-01-02T00:00:00",
                            ],
                        }
                    }
                ],
            },
            transformed_data,
        )

    def test_with_list(self):
        transformed_data = transform_datetimes([date(2020, 1, 1), date(2019, 12, 1)])

        self.assertIsInstance(transformed_data, list)
        self.assertEqual(transformed_data, ["2020-01-01", "2019-12-01"])

    def test_with_tuple(self):
        transformed_data = transform_datetimes((date(2020, 1, 1), date(2019, 12, 1)))

        self.assertIsInstance(transformed_data, tuple)
        self.assertEqual(transformed_data, ("2020-01-01", "2019-12-01"))

    def test_with_none_returns_none(self):
        transformed_data = transform_datetimes(None)

        self.assertIsNone(transformed_data)
