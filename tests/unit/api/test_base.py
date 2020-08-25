from ordway.api.exceptions import OrdwayAPIRequestException, OrdwayAPIException
from ordway.api.base import ListAPIMixin, GetAPIMixin, _remove_order_from_sort
from requests.exceptions import RequestException
from unittest import TestCase
from unittest.mock import patch

from .base import APITestCase


class TestAPIBase(APITestCase):
    def test_construct_headers_returns_proper_dict(self):
        self.assertDictEqual(
            self.api_base._construct_headers(),
            {
                "X-User-Company": "TestCompany",
                "X-API-Key": "TestAPIKey",
                "X-User-Token": "TestUserToken",
                "X-User-Email": "TestEmail",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    def test_get_request_calls_request(self):
        self.mocked_response().json.return_value = {}

        response = self.api_base._get_request("test")

        self.assertDictEqual(response, {})

    def test_post_request_raises_value_error_without_data_and_json(self):
        with self.assertRaises(ValueError):
            self.api_base._post_request("test")

    def test_post_request_calls_request(self):
        self.mocked_response().json.return_value = {}

        response = self.api_base._post_request("test", json={})

        self.assertDictEqual(response, {})

    def test_request_raises_ordway_api_exception_on_request_exception(self):
        self.mocked_response.side_effect = RequestException

        with self.assertRaises(OrdwayAPIRequestException):
            self.api_base._request("GET", "test")

    def test_request_raises_ordway_api_exception_on_value_error(self):
        self.mocked_response().json.side_effect = ValueError

        with self.assertRaises(OrdwayAPIRequestException):
            self.api_base._request("GET", "test")


class TestRemovOrderFromSort(TestCase):
    def test_order_included(self):
        self.assertEqual(
            _remove_order_from_sort("updated_date,name asc"),
            ("updated_date,name", True),
        )
        self.assertEqual(
            _remove_order_from_sort("updated_date,name desc"),
            ("updated_date,name", False),
        )
        self.assertEqual(
            _remove_order_from_sort("updated_date desc,name asc"),
            ("updated_date desc,name", True),
        )
        self.assertEqual(
            _remove_order_from_sort("name_asc,updated_date desc"),
            ("name_asc,updated_date", False),
        )

    def test_order_excluded(self):
        self.assertEqual(
            _remove_order_from_sort("name_asc,updated_date"),
            ("name_asc,updated_date", None),
        )
        self.assertEqual(
            _remove_order_from_sort("name_asc,updated_date_desc"),
            ("name_asc,updated_date_desc", None),
        )


class TestListMixin(APITestCase):
    def setUp(self):
        super().setUp()

        self.get_request_patcher = patch("ordway.api.base.APIBase._get_request")
        self.mocked_get_request = self.get_request_patcher.start()

        self.list_api_mixin = ListAPIMixin(self.client)
        self.list_api_mixin.collection = "test_collection"

    def tearDown(self):
        super().tearDown()

        self.get_request_patcher.stop()

    def test_list_sort_affects_order(self):
        pass  # self.list_api_mixin.list(page=1, sort="updated_date,name desc")

    def test_list_yields_dicts_from_returned_list(self):
        self.mocked_get_request.return_value = [{"test": "1"}, {"test": "2"}]

        results = self.list_api_mixin.list(page=1)

        self.assertDictEqual(next(results), {"test": "1"})
        self.assertDictEqual(next(results), {"test": "2"})

    def test_list_raises_generator_exit_when_returned_list_is_empty(self):
        self.mocked_get_request.return_value = []

        results = self.list_api_mixin.list(page=1)

        with self.assertRaises(GeneratorExit):
            next(results)

    def test_list_handles_single_dict_response(self):
        self.mocked_get_request.return_value = {"foo": "bar"}

        results = self.list_api_mixin.list(page=1)

        self.assertDictEqual(next(results), {"foo": "bar"})

    def test_list_does_not_not_raise_generator_exit_early(self):
        self.mocked_get_request.return_value = [
            {"test": "1"},
            {"test": "2"},
            {"test": "3"},
        ]

        count = 0
        try:
            for _ in self.list_api_mixin.list(page=1):
                count += 1
        except GeneratorExit:
            self.fail(".list() did raised GeneratorExit early.")

        self.assertEqual(count, 3)

    def test_all_returns_all_results(self):
        def test_list_generator():
            results = [{"test": "1"}, {"test": "2"}]

            for result in results:
                yield result

        with patch.object(self.list_api_mixin, "list") as mocked_list:
            mocked_list.return_value = test_list_generator()

            results = self.list_api_mixin.all()

            self.assertEqual(next(results), {"test": "1"})
            self.assertEqual(next(results), {"test": "2"})


class TestGetMixin(APITestCase):
    def setUp(self):
        super().setUp()

        self.get_request_patcher = patch("ordway.api.base.APIBase._get_request")
        self.mocked_get_request = self.get_request_patcher.start()

        self.get_api_mixin = GetAPIMixin(self.client)
        self.get_api_mixin.collection = "test_collection"

    def tearDown(self):
        super().tearDown()

        self.get_request_patcher.stop()

    def test_get_handles_single_element_list_and_dict_response(self):
        self.mocked_get_request.return_value = [{"foo": "bar"}]
        self.assertEqual(self.get_api_mixin.get(id="foo_id"), {"foo": "bar"})

        self.mocked_get_request.return_value = {"foo": "bar"}
        self.assertEqual(self.get_api_mixin.get(id="foo_id"), {"foo": "bar"})

    def test_get_raises_exception_if_list_returned_has_more_than_one_element(self):
        self.mocked_get_request.return_value = [{"foo": "bar"}, {"roy": "gbiv"}]

        with self.assertRaises(OrdwayAPIException):
            self.get_api_mixin.get(id="foo_id")
