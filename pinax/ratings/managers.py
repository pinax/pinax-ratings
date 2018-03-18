from django.contrib.contenttypes.models import ContentType
from django.db import models

from .categories import category_value


class OverallRatingManager(models.Manager):

    def top_rated(self, klass, category=""):
        cat = category_value(klass, category)
        if cat is None:
            cat = ""
        qs = self.filter(
            content_type=ContentType.objects.get_for_model(klass),
            category=cat
        )
        qs = qs.extra(
            select={
                "sortable_rating": "COALESCE(rating, 0)"
            }
        )
        return qs.order_by("-sortable_rating")
