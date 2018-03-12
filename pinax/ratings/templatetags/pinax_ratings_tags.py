from decimal import Decimal

from django import template
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from ..categories import category_value
from ..models import OverallRating, Rating

register = template.Library()


def user_rating_value(user, obj, category=""):
    try:
        ct = ContentType.objects.get_for_model(obj)
        if category:
            rating = Rating.objects.get(
                object_id=obj.pk,
                content_type=ct,
                user=user,
                category=category_value(obj, category)
            ).rating
        else:
            rating = Rating.objects.filter(
                object_id=obj.pk,
                content_type=ct,
                user=user
            ).aggregate(r=models.Avg("rating"))["r"]
            rating = Decimal(str(rating or "0"))
    except Rating.DoesNotExist:
        rating = 0
    return rating


@register.simple_tag
def user_rating(user, object, category=""):
    """
    Usage:
        {% user_rating user obj [category] as var %}
    """
    return user_rating_value(user, object, category)


@register.simple_tag
def overall_rating(object, category=""):
    """
    Usage:
        {% overall_rating obj [category] as var %}
    """
    try:
        ct = ContentType.objects.get_for_model(object)
        if category:
            rating = OverallRating.objects.get(
                object_id=object.pk,
                content_type=ct,
                category=category_value(object, category)
            ).rating or 0
        else:
            rating = OverallRating.objects.filter(
                object_id=object.pk,
                content_type=ct
            ).aggregate(r=models.Avg("rating"))["r"]
            rating = Decimal(str(rating or "0"))
    except OverallRating.DoesNotExist:
        rating = 0
    return rating


def rating_post_url(user, obj):
    ct = ContentType.objects.get_for_model(obj)
    post_url = reverse(
        "pinax_ratings:rate",
        kwargs={
            "content_type_id": ct.pk,
            "object_id": obj.pk
        }
    )
    return post_url


@register.inclusion_tag("pinax/ratings/_script.html")
def user_rating_js(user, obj, category=""):
    post_url = rating_post_url(user, obj)
    rating = user_rating_value(user, obj, category)

    return {
        "obj": obj,
        "post_url": post_url,
        "category": category,
        "the_user_rating": rating,
        "STATIC_URL": settings.STATIC_URL,
    }


@register.simple_tag
def ratings(obj):
    ct = ContentType.objects.get_for_model(obj)
    try:
        return OverallRating.objects.get(
            content_type=ct,
            object_id=obj.pk
        ).ratings.all()
    except OverallRating.DoesNotExist:
        return []


@register.simple_tag
def user_rating_url(user, obj):
    return rating_post_url(user, obj)


@register.simple_tag
def rating_count(obj):
    """
    Total amount of users who have submitted a positive rating for this object.

    Usage:
        {% rating_count obj %}
    """
    count = Rating.objects.filter(
        object_id=obj.pk,
        content_type=ContentType.objects.get_for_model(obj),
    ).exclude(rating=0).count()
    return count
