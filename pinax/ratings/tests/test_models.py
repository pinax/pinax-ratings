from decimal import Decimal

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

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
        self.rating_object = Rating.objects.create(
            object_id=self.expedition.pk,
            content_type=ContentType.objects.get_for_model(self.expedition),
            user=self.paltman,
            category="color",
            rating=7
        )
        self.overall_rating_object = OverallRating.objects.create(
            object_id=self.expedition.pk,
            content_type=ContentType.objects.get_for_model(self.expedition),
            category="color",
            rating=7
        )
        self.rating_object.overall_rating = self.overall_rating_object
        self.rating_object.save()

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
        self.assertEqual(str(self.rating_object), "7")

    def test_update_with_a_zero_rating(self):
        """
        Ensure that if a rating is updated with zero, the overall rating returned is
        equal to zero
        """
        overall = Rating.update(self.expedition, self.paltman, rating=0, category="color")
        self.assertEquals(overall, Decimal("0"))

    def test_clear(self):
        """
        Ensure clear method returns an overall rating of zero when the rating is
        cleared
        """
        overall = self.rating_object.clear()
        self.assertEquals(overall, 0)
