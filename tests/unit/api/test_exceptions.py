from unittest import TestCase
from unittest.mock import Mock
from ordway.api.exceptions import OrdwayAPIRequestException


class TestOrdwayAPIRequestException(TestCase):
    def test_grabs_errors_from_response(self):
        error = {"status": 404, "source": "refunds", "details": "No reason specified."}
        mocked_response = Mock()
        mocked_response.json.return_value = {"errors": error}

        exc = OrdwayAPIRequestException(response=mocked_response)

        self.assertDictEqual(exc.errors, error)

    def test_errors_is_none_if_no_response_json(self):
        mocked_response = Mock()
        mocked_response.json.side_effect = ValueError

        exc = OrdwayAPIRequestException(response=mocked_response)
        self.assertIsNone(exc.errors)

    def test_errors_set_if_passed(self):
        error = {"status": 500, "source": "refunds", "details": "No reason specified."}

        exc = OrdwayAPIRequestException(errors=error)
        self.assertDictEqual(error, exc.errors)

        exc = OrdwayAPIRequestException(errors=None)
        self.assertIsNone(exc.errors)
