from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from pinax.ratings.models import Rating

from .models import Car


class Tests(TestCase):

    def setUp(self):
        self.paltman = User.objects.create(username="paltman")
        self.jtauber = User.objects.create(username="jtauber")
        self.bronco = Car.objects.create(name="Ford Bronco")
        self.blazer = Car.objects.create(name="Cheverolet Blazer")
        self.expedition = Car.objects.create(name="Ford Expedition")

    def test_rating(self):
        overall = Rating.update(self.bronco, self.paltman, rating=5)
        self.assertEquals(overall, Decimal("5"))
        overall = Rating.update(self.bronco, self.jtauber, rating=2)
        self.assertEquals(overall, Decimal("3.5"))
