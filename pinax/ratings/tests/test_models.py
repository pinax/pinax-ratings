from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from pinax.ratings.categories import (
    category_label,
    category_value,
    is_valid_category,
)
from pinax.ratings.models import OverallRating, Rating

from .models import Car
from .test import TestCase


class RatingModelTests(TestCase):

    def setUp(self):
        self.paltman = User.objects.create(username="paltman")
        self.jtauber = User.objects.create(username="jtauber")
        self.bronco = Car.objects.create(name="Ford Bronco")
        self.blazer = Car.objects.create(name="Cheverolet Blazer")
        self.expedition = Car.objects.create(name="Ford Expedition")
        self.speed = "speed"
        self.rating_object = Rating.objects.create(
            object_id=self.expedition.pk,
            content_type=ContentType.objects.get_for_model(self.expedition),
            user=self.paltman,
            category=self.speed,
            rating=5
        )
        self.overall_rating_object = OverallRating.objects.create(
            object_id=self.expedition.pk,
            content_type=ContentType.objects.get_for_model(self.expedition),
            category=self.speed,
            rating=5
        )
        self.rating_object.overall_rating = self.overall_rating_object
        self.rating_object.save()
        self.overall_rating_object.update()

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
            obj = self.expedition
        cat_choice = category_value(obj, category)
        if not cat_choice:
            cat_choice = ""
        Rating.update(
            rating_object=obj,
            user=user,
            category=cat_choice,
            rating=rating
        )

    def test_rating(self):
        overall = Rating.update(self.bronco, self.paltman, rating=5)
        self.assertEquals(overall, Decimal("5"))
        overall = Rating.update(self.bronco, self.jtauber, rating=2)
        self.assertEquals(overall, Decimal("3.5"))

    def test_str_(self):
        """
        Ensure that when str(object) is called on a Rating object, a string
        representation of the rating is returned by the __str__() method
        """
        self.assertEqual(str(self.rating_object), "5")

    def test_update_with_a_zero_rating(self):
        """
        Ensure that if a rating is updated with zero, the overall rating returned is
        equal to zero
        """
        overall = Rating.update(self.expedition, self.paltman, rating=0, category=self.speed)
        self.assertEquals(overall, Decimal("0"))

    def test_clear(self):
        """
        Ensure clear method returns an overall rating of zero when the rating is
        cleared
        """
        overall = self.rating_object.clear()
        self.assertEquals(overall, 0)

    def test_overallrating_top_rated_in_category(self):
        """
        Ensure ratings are returned in order for object class and category
        """
        self.create_rating(self.jtauber, 4, obj=self.bronco, category=self.speed)
        self.create_rating(self.paltman, 3, obj=self.blazer, category=self.speed)
        result = OverallRating.objects.top_rated(Car, self.speed)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].rating, 5)
        self.assertEqual(result[0].object_id, self.expedition.pk)
        self.assertEqual(result[1].rating, 4)
        self.assertEqual(result[1].object_id, self.bronco.pk)
        self.assertEqual(result[2].rating, 3)
        self.assertEqual(result[2].object_id, self.blazer.pk)

    def test_overallrating_top_rated_no_category(self):
        """
        Ensure ratings are returned in order for object class, no category
        """
        self.create_rating(self.jtauber, 5, obj=self.blazer)
        self.create_rating(self.paltman, 4, obj=self.bronco)
        self.create_rating(self.paltman, 3, obj=self.expedition)
        result = OverallRating.objects.top_rated(Car)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].rating, 5)
        self.assertEqual(result[0].object_id, self.blazer.pk)
        self.assertEqual(result[1].rating, 4)
        self.assertEqual(result[1].object_id, self.bronco.pk)
        self.assertEqual(result[2].rating, 3)
        self.assertEqual(result[2].object_id, self.expedition.pk)

    def test_category_label(self):
        expected = settings.PINAX_RATINGS_CATEGORY_CHOICES["tests.Car"]["speed"]
        label = category_label(self.expedition, "speed")
        self.assertEqual(label, expected)

    def test_is_valid_category(self):
        self.assertTrue(is_valid_category(self.expedition, "speed"))
        self.assertFalse(is_valid_category(self.expedition, "taste"))
        self.assertFalse(is_valid_category(self.paltman, "taste"))
