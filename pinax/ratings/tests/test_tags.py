from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from ..categories import category_value
from ..models import Rating
from ..templatetags.pinax_ratings_tags import (
    overall_rating,
    rating_count,
    ratings,
    user_rating,
    user_rating_js,
    user_rating_url,
)
from .models import Car
from .test import TestCase


class TemplateTagsTest(TestCase):
    """
    Tests for the template tags
    """

    def setUp(self):
        self.handling = "handling"
        self.speed = "speed"
        self.hamilton = self.make_user(username="lewis_hamilton")
        self.schumacher = self.make_user(username="michael_schumacher")
        self.unrated_object = self.make_user(username="unrated_user")
        self.benz = Car.objects.create(name="Mercedes c200")

    def create_rating(self, user, rating, obj=None, category=""):
        """
        Helper function to post a rating for the benz object of
        type Car used in the tests
        :param user: User
        :param rating: int
        :param obj: obj
        :param category: str
        :return: http response object
        """
        if not obj:
            obj = self.benz
        cat_choice = category_value(obj, category)
        if not cat_choice:
            cat_choice = ""
        Rating.update(
            rating_object=obj,
            user=user,
            category=cat_choice,
            rating=rating
        )

    def test_user_rating_with_category(self):
        """
        Ensure `user_rating` renders rating posted by specified user.
        """
        # ratings for handling, ensure they are distinct
        self.create_rating(self.hamilton, 3, category=self.handling)
        self.create_rating(self.schumacher, 4, category=self.handling)
        self.assertEqual(user_rating(self.hamilton, self.benz, self.handling), 3)
        self.assertEqual(user_rating(self.schumacher, self.benz, self.handling), 4)

        # ratings for speed, different from handling
        self.create_rating(self.hamilton, 5, category=self.speed)
        self.create_rating(self.schumacher, 2, category=self.speed)
        self.assertEqual(user_rating(self.hamilton, self.benz, self.speed), 5)
        self.assertEqual(user_rating(self.schumacher, self.benz, self.speed), 2)

    def test_user_rating_on_unrated_object(self):
        """
        Ensure zero is returned from `user_rating` for object without a rating.
        """
        self.assertEqual(user_rating(self.hamilton, self.unrated_object, self.speed), 0)
        # Same check, no category
        self.assertEqual(user_rating(self.hamilton, self.unrated_object), 0)

    def test_user_rating_no_category(self):
        """
        Ensure `user_rating` returns the average of all ratings for object by user
        when no category is specified.
        """
        # Create first rating, return value should be same
        self.create_rating(self.schumacher, 5, category=self.handling)
        self.assertEqual(user_rating(self.schumacher, self.benz), 5)  # == (5) / 1

        # Add second rating in different category, should be averaged with first
        self.create_rating(self.schumacher, 3, category=self.speed)
        self.assertEqual(user_rating(self.schumacher, self.benz), 4)  # == (5 + 3) / 2

        # Add third rating with no category, should be averaged with first two ratings
        self.create_rating(self.schumacher, 1)
        self.assertEqual(user_rating(self.schumacher, self.benz), 3)  # == (5 + 3 + 1) / 3

    def test_user_rating_revised(self):
        """
        Ensure `user_rating` returns the latest rating for a category.
        """
        # Create first rating, return value should be same
        self.create_rating(self.schumacher, 5, category=self.handling)
        self.create_rating(self.schumacher, 2, category=self.handling)
        self.assertEqual(user_rating(self.schumacher, self.benz), 2)

    def test_overall_rating_tag_with_category(self):
        """
        Ensure `overall_rating` returns an average rating for
        a specified category.
        """
        self.create_rating(self.schumacher, 5, category=self.handling)
        self.create_rating(self.hamilton, 1, category=self.handling)
        self.assertEqual(overall_rating(self.benz, self.handling), 3)

        # Add rating for a different category
        self.create_rating(self.schumacher, 5, category=self.speed)
        # Overall "handling" rating should be same as before
        self.assertEqual(overall_rating(self.benz, self.handling), 3)

    def test_overall_rating_on_unrated_object(self):
        """
        Ensure zero is returned from `overall_rating` for object without a rating.
        """
        self.assertEqual(overall_rating(self.unrated_object, self.speed), 0)
        # Same check, no category
        self.assertEqual(overall_rating(self.unrated_object), 0)

    def test_overall_rating_tag_with_no_category(self):
        """
        Ensure `overall_rating` returns the average of all ratings for object by user
        when no category is specified.
        """
        # Create first rating, return value should be same
        self.create_rating(self.schumacher, 5, category=self.handling)
        self.assertEqual(overall_rating(self.benz), 5)  # == (5) / 1

        # Add second rating in different category, should be averaged with first
        self.create_rating(self.schumacher, 3, category=self.speed)
        self.assertEqual(overall_rating(self.benz), 4)  # == (5 + 3) / 2

        # Add third rating with no category, should be averaged with first two ratings
        self.create_rating(self.schumacher, 1)
        self.assertEqual(overall_rating(self.benz), 3)  # == (5 + 3 + 1) / 3

    def test_ratings_tag(self):
        """
        Ensure QuerySet of all Ratings for self.benz is returned
        """
        self.create_rating(self.schumacher, 5)
        self.create_rating(self.hamilton, 5)

        content_type = ContentType.objects.get_for_model(self.benz)
        output = ratings(self.benz)
        expected = Rating.objects.filter(
            content_type=content_type,
            object_id=self.benz.pk
        )
        self.assertEqual(len(expected), 2)
        self.assertSetEqual(set(output), set(expected))

    def test_ratings_tag_with_not_rated_object(self):
        """
        Ensure empty list is returned for object without Ratings
        """
        self.assertEqual(ratings(self.unrated_object), [])

    def test_user_rating_url_tag(self):
        """
        Ensure `user_rating_url` returns correct URL for user to post a rating
        """
        tag_url = user_rating_url(self.hamilton, self.benz)
        expected_path = reverse(
            "pinax_ratings:rate",
            kwargs={
                "content_type_id": ContentType.objects.get_for_model(self.benz).pk,
                "object_id": self.benz.pk
            })
        self.assertEqual(tag_url, expected_path)

    def test_rating_count_tag(self):
        """
        Ensure `rating_count` returns the number of ratings on an object
        regardless of who rated and regardless of category.
        """
        self.create_rating(self.schumacher, 5)
        self.create_rating(self.schumacher, 5, category=self.speed)
        self.create_rating(self.schumacher, 5, obj=self.unrated_object)  # should not be included
        self.create_rating(self.hamilton, 5)
        self.create_rating(self.hamilton, 5, category=self.handling)
        count = rating_count(self.benz)
        self.assertEqual(count, 4)

    def test_user_rating_js_tag(self):
        """
        Ensure the correct context is returned
        """
        self.create_rating(self.schumacher, 5, category=self.speed)
        context = user_rating_js(self.schumacher, self.benz, self.speed)

        self.assertEqual(context["obj"], self.benz)
        self.assertEqual(context["category"], self.speed)
        self.assertEqual(context["the_user_rating"], 5)
        self.assertEqual(context["STATIC_URL"], settings.STATIC_URL)
        self.assertEqual(
            context["post_url"],
            reverse(
                "pinax_ratings:rate",
                kwargs={
                    "content_type_id": ContentType.objects.get_for_model(self.benz).pk,
                    "object_id": self.benz.pk
                }
            ))
