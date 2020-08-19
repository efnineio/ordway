from ..base import VCRIntegrationTestCase


class TestProducts(VCRIntegrationTestCase):
    def test_list(self):
        self.client.products.list(page=1, size=5)
