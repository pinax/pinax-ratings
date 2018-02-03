from django.contrib.contenttypes.models import ContentType

from .models import Car
from .test import TestCase


class RateViewTest(TestCase):
    # tests for the RateView

    def setUp(self):
        self.test_user = self.make_user(username="test_user")
        self.forester = Car.objects.create(name="Subaru Forester")

    def test_post_rating_with_invalid_content_type_id(self):
        # test line with code snippet:
        #   get_object_or_404(ContentType, pk=self.kwargs.get("content_type_id"))
        #
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

    def test_post_rating_with_invalid_object_id(self):
        # test line with code snippet:
        #   get_object_or_404(ct.model_class(), pk=self.kwargs.get("object_id"))
        #
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.forester).pk,
                object_id=100,
                data={
                    "rating": 3,
                    "category": "handling"
                },
            )
            self.response_404(response)

    def test_post_rating_with_invalid_category(self):
        # tests the condition:
        #   if category and cat_choice is None:
        #
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.forester).pk,
                object_id=self.forester.pk,
                data={
                    "rating": 4,
                    "category": "non-existing-category"
                },
            )
            self.response_403(response)

    def test_post_rating_with_invalid_rating(self):
        # tests the condition:
        #   if rating_input not in range(NUM_OF_RATINGS + 1):
        #
        with self.login(self.test_user):
            response = self.post(
                "pinax_ratings:rate",
                content_type_id=ContentType.objects.get_for_model(self.forester).pk,
                object_id=self.forester.pk,
                data={
                    "rating": 10,
                    "category": "handling"
                },
            )
            self.response_403(response)

    def test_post_rating_with_valid_data(self):
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
            # assert http response code
            self.response_200(response)
            # assert the data returned is as expected
            self.assertContext("user_rating", 3)
            self.assertContext("category", "handling")
            self.assertContext("overall_rating", 3.0)
            self.assertContext("content_type_id", str(content_type_id))
            self.assertContext("object_id", str(object_id))
