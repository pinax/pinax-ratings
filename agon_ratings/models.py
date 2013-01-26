import datetime

from decimal import Decimal

from django.db import models

from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from agon_ratings.categories import RATING_CATEGORY_CHOICES
from agon_ratings.managers import OverallRatingManager

USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', User)

class OverallRating(models.Model):
    
    object_id = models.IntegerField(db_index=True)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey()
    rating = models.DecimalField(decimal_places=1, max_digits=6, null=True)
    
    category = models.IntegerField(null=True, choices=RATING_CATEGORY_CHOICES)
    
    objects = OverallRatingManager()
    
    class Meta:
        unique_together = [
            ("object_id", "content_type", "category"),
        ]
    
    def update(self):
        self.rating = Rating.objects.filter(
            overall_rating = self
        ).aggregate(r = models.Avg("rating"))["r"]
        self.rating = Decimal(str(self.rating or "0"))
        self.save()


class Rating(models.Model):
    overall_rating = models.ForeignKey(OverallRating, null = True, related_name = "ratings")
    object_id = models.IntegerField(db_index=True)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey()
    user = models.ForeignKey(USER_MODEL)
    rating = models.IntegerField()
    timestamp = models.DateTimeField(default=datetime.datetime.now)
    
    category = models.IntegerField(null=True, choices=RATING_CATEGORY_CHOICES)
    
    class Meta:
        unique_together = [
            ("object_id", "content_type", "user", "category"),
        ]
    
    def __unicode__(self):
        return unicode(self.rating)
