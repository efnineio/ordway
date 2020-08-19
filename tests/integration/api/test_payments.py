from ..base import VCRIntegrationTestCase


class TestPayments(VCRIntegrationTestCase):
    def test_list(self):
        payments = self.client.payments.list(page=1, size=5)

        next(payments)
