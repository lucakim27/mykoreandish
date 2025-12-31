from src.tests.setup import SetupTestCase

class TestHomeRoutes(SetupTestCase):

    def test_home_page_loads(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"Discover Korean Cuisine", res.data)
