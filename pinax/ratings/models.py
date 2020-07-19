from decimal import Decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Avg
from django.utils import timezone

from .categories import RATING_CATEGORY_CHOICES
from .managers import OverallRatingManager


class OverallRating(models.Model):

    object_id = models.IntegerField(db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey()
    rating = models.DecimalField(decimal_places=1, max_digits=6, null=True)
    category = models.CharField(max_length=250, blank=True, choices=RATING_CATEGORY_CHOICES)

    objects = OverallRatingManager()

    class Meta:
        unique_together = [
            ("object_id", "content_type", "category"),
        ]

    def update(self):
        r = Rating.objects.filter(overall_rating=self).aggregate(r=Avg("rating"))["r"] or 0
        self.rating = Decimal(str(r))
        self.save()


class Rating(models.Model):
    overall_rating = models.ForeignKey(OverallRating, null=True, related_name="ratings", on_delete=models.CASCADE)
    object_id = models.IntegerField(db_index=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField()
    timestamp = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=250, blank=True, choices=RATING_CATEGORY_CHOICES)

    def clear(self):
        overall = self.overall_rating
        self.delete()
        overall.update()
        return overall.rating

    @classmethod
    def update(cls, rating_object, user, rating, category=""):
        # @@@ Still doing too much in this method
        ct = ContentType.objects.get_for_model(rating_object)
        rating_obj = cls.objects.filter(
            object_id=rating_object.pk,
            content_type=ct,
            user=user,
            category=category
        ).first()

        if rating_obj and rating == 0:
            return rating_obj.clear()

        if rating_obj is None:
            rating_obj = cls.objects.create(
                object_id=rating_object.pk,
                content_type=ct,
                user=user,
                category=category,
                rating=rating
            )
        overall, _ = OverallRating.objects.get_or_create(
            object_id=rating_object.pk,
            content_type=ct,
            category=category
        )
        rating_obj.overall_rating = overall
        rating_obj.rating = rating
        rating_obj.save()
        overall.update()
        return overall.rating

    class Meta:
        unique_together = [
            ("object_id", "content_type", "user", "category"),
        ]

    def __str__(self):
        return str(self.rating)
