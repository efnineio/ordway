from unittest import TestCase
from ordway.api.base import APIBase
from ordway import OrdwayClient
from unittest import TestCase
from unittest.mock import patch


class APITestCase(TestCase):
    def setUp(self):
        self.client = OrdwayClient(
            email="TestEmail",
            company="TestCompany",
            user_token="TestUserToken",
            api_key="TestAPIKey",
        )
        self.response_patcher = patch.object(self.client.session, "request")
        self.mocked_response = self.response_patcher.start()

        self.api_base = APIBase(self.client)

    def tearDown(self):
        self.response_patcher.stop()
