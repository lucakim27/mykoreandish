from unittest.mock import patch
from backend.tests.setup import SetupTestCase

class TestReviewsAPI(SetupTestCase):

    @patch(
        "project.controllers.api.reviewsController.aggregate_manager.get_total_reviews"
    )
    def test_get_total_reviews_success(self, mock_get_total_reviews):
        mock_get_total_reviews.return_value = 42

        res = self.client.get("/api/reviews/get_total_reviews")

        self.assertEqual(res.status_code, 200)
        self.assertIn("total_reviews", res.get_json())
        self.assertEqual(res.get_json()["total_reviews"], 42)

    @patch(
    "project.controllers.api.reviewsController.aggregate_manager.get_total_reviews",
    side_effect=Exception("DB error")
    )
    def test_get_total_reviews_failure(self, mock_get_total_reviews):
        res = self.client.get("/api/reviews/get_total_reviews")
        self.assertEqual(res.status_code, 500)
