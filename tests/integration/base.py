from vcr_unittest import VCRTestCase
from ordway import OrdwayClient
from ordway.exceptions import OrdwayClientException


class VCRIntegrationTestCase(VCRTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        try:
            cls.client = OrdwayClient.from_env()
        except OrdwayClientException:
            cls.client = OrdwayClient(
                email="test@aol.com",
                api_key="test_api_key",
                company="test_company",
                user_token="test_user_token",
            )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def _get_vcr(self, **kwargs):
        vcr = super()._get_vcr(**kwargs)

        vcr.decode_compressed_response = True
        vcr.filter_headers = (
            "X-User-Company",
            "X-API-Key",
            "X-User-Token",
            "X-User-Email",
            "cf-request-id",
            "X-Request-Id",
            "Set-Cookie",
            "Cookies",
        )
        # TODO Will need to scrub a lot of sensitive info before completing integration tests.
        # vcr.before_record_response = _before_record_response

        return vcr
