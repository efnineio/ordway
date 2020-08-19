from unittest import TestCase
from unittest.mock import MagicMock, patch
from ordway import OrdwayClient
from ordway.exceptions import OrdwayClientException
from os import environ
from logging import getLogger, CRITICAL


class TestOrdwayClient(TestCase):
    def setUp(self):
        self.default_kwargs = {
            "email": "TestEmail",
            "company": "TestCompany",
            "user_token": "TestUserToken",
            "api_key": "TestAPIKey",
        }

        self.client = OrdwayClient(**self.default_kwargs)

    def test_updates_session_proxies(self):
        new_client = OrdwayClient(
            **self.default_kwargs, proxies={"http": "192.168.0.1"}
        )

        proxies = new_client.session.proxies

        self.assertIn("http", proxies)
        self.assertEqual(proxies["http"], "192.168.0.1")

    def test_updates_session_headers(self):
        new_client = OrdwayClient(**self.default_kwargs, headers={"User-Agent": "007"})

        headers = new_client.session.headers

        self.assertIn("User-Agent", headers)
        self.assertEqual(headers["User-Agent"], "007")

    def test_removes_v_from_api_version(self):
        new_client = OrdwayClient(**self.default_kwargs, api_version="v1")

        self.assertEqual(new_client.api_version, "1")

    def test_setting_api_version_raises_ordway_exception_if_not_supported(self):
        self.client.SUPPORTED_API_VERSIONS = ("1", "2")
        self.client.api_version = "1"
        self.client.api_version = "2"

        with self.assertRaises(OrdwayClientException):
            self.client.api_version = "3"

    def test_from_env_instantiates_client_from_env_vars(self):
        new_environ = {
            "ORDWAY_EMAIL": "test@aol.com",
            "ORDWAY_API_KEY": "test_api_key",
            "ORDWAY_COMPANY": "test_company",
            "ORDWAY_USER_TOKEN": "test_token",
        }

        with patch.dict(environ, new_environ, clear=True):
            new_client = OrdwayClient.from_env()

            self.assertEqual(new_client.email, "test@aol.com")
            self.assertEqual(new_client.api_key, "test_api_key")
            self.assertEqual(new_client.company, "test_company")
            self.assertEqual(new_client.user_token, "test_token")

        # Test with ORDWAY_API_VERSION
        new_environ["ORDWAY_API_VERSION"] = "2"
        with patch.object(OrdwayClient, "SUPPORTED_API_VERSIONS", ("2",)):
            with patch.dict(environ, new_environ, clear=True):
                new_client = OrdwayClient.from_env()

                self.assertEqual(new_client.api_version, "2")

    def test_from_env_raises_ordway_client_exception_on_missing_required_env_var(self):
        new_environ = {
            "ORDWAY_EMAIL": "test@aol.com",
        }

        with patch.dict(environ, new_environ, clear=True):
            with self.assertRaises(OrdwayClientException):
                OrdwayClient.from_env()
