from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from .models import Car
from .test import TestCase


class RateViewTest(TestCase):
    """
    tests for the RateView
    """

    def setUp(self):
        self.test_user = self.make_user(username="test_user")
        self.forester = Car.objects.create(name="Subaru Forester")

    def test_post_rating_returns_404(self):
        """
        Ensure view returns 404 if object is not found. This should
        typically happen when one of the two kwargs i.e content_type_id
        and object_id have invalid data
        """
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=400,
                object_id=1,
                data={
                    "rating": 3,
                    "category": "handling"
                },
            )
            self.response_404(response)

    def test_post_rating_with_invalid_category(self):
        """
        Ensure view returns 403 if an invalid category choice
        is provided in the POST data. category choices are added
        to the PINAX_RATINGS_CATEGORY_CHOICES setting in settings.py
        """
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.forester).pk,
                object_id=self.forester.pk,
                data={
                    "rating": settings.PINAX_RATINGS_NUM_OF_RATINGS,
                    "category": "non-existing-category"
                },
            )
            self.response_403(response)

    def test_post_rating_greater_than_range(self):
        """
        Ensure view returns 403 if the rating is greater
        than the minimum rating enforced by RatingView
        """
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.forester).pk,
                object_id=self.forester.pk,
                data={
                    "rating": settings.PINAX_RATINGS_NUM_OF_RATINGS + 1,
                    "category": "handling"
                },
            )
            self.response_403(response)

    def test_post_rating_less_than_range(self):
        """
        Ensure view returns 403 if the rating is less
        than the minimum rating enforced by RatingView
        """
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.forester).pk,
                object_id=self.forester.pk,
                data={
                    "rating": -1,
                    "category": "handling"
                },
            )
            self.response_403(response)

    def test_post_rating_with_valid_data(self):
        """
        Ensure view returns 200 if valid data is passed to
        the view. For data to be valid, the following conditions
        must be met;
        1. The url kwargs content_type_id and object_id both have valid IDs
        2. The body of the POST request has keys rating and category with
        valid values of rating num within the the range and valid category choice
        """
        with self.login(self.test_user):
            content_type_id = ContentType.objects.get_for_model(self.forester).pk
            object_id = self.forester.pk
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=content_type_id,
                object_id=object_id,
                data={
                    "rating": 3,
                    "category": "handling"
                },
            )
            self.response_200(response)
            self.assertContext("user_rating", 3)
            self.assertContext("category", "handling")
            self.assertContext("overall_rating", 3.0)
