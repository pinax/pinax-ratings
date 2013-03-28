from decimal import Decimal

from django import template
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType

from agon_ratings.categories import category_value
from agon_ratings.models import Rating, OverallRating


register = template.Library()


def user_rating_value(user, obj, category=None):
    try:
        ct = ContentType.objects.get_for_model(obj)
        if category is None:
            rating = Rating.objects.filter(
                object_id = obj.pk,
                content_type = ct,
                user = user
            ).aggregate(r = models.Avg("rating"))["r"]
            rating = Decimal(str(rating or "0"))
        else:
            rating = Rating.objects.get(
                object_id = obj.pk,
                content_type = ct,
                user = user,
                category = category_value(obj, category)
            ).rating
    except Rating.DoesNotExist:
        rating = 0
    return rating


class UserRatingNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        
        if len(bits) == 5:
            category = None
        elif len(bits) == 6:
            category = parser.compile_filter(bits[3])
        else:
            raise template.TemplateSyntaxError()
        
        return cls(
            user = parser.compile_filter(bits[1]),
            obj = parser.compile_filter(bits[2]),
            as_var = bits[len(bits) - 1],
            category = category
        )
    
    def __init__(self, user, obj, as_var, category=None):
        self.user = user
        self.obj = obj
        self.as_var = as_var
        self.category = category
    
    def render(self, context):
        user = self.user.resolve(context)
        obj = self.obj.resolve(context)
        if self.category:
            category = self.category.resolve(context)
        else:
            category = None
        context[self.as_var] = user_rating_value(user, obj, category)
        return ""


@register.tag
def user_rating(parser, token):
    """
    Usage:
        {% user_rating user obj [category] as var %}
    """
    return UserRatingNode.handle_token(parser, token)


class OverallRatingNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        
        if len(bits) == 4:
            category = None
        elif len(bits) == 5:
            category = parser.compile_filter(bits[2])
        else:
            raise template.TemplateSyntaxError()
        
        return cls(
            obj = parser.compile_filter(bits[1]),
            as_var = bits[len(bits) - 1],
            category = category
        )
    
    def __init__(self, obj, as_var, category=None):
        self.obj = obj
        self.as_var = as_var
        self.category = category
    
    def render(self, context):
        obj = self.obj.resolve(context)
        if self.category:
            category = self.category.resolve(context)
        else:
            category = None
        
        try:
            ct = ContentType.objects.get_for_model(obj)
            if category is None:
                rating = OverallRating.objects.filter(
                    object_id = obj.pk,
                    content_type = ct
                ).aggregate(r = models.Avg("rating"))["r"]
                rating = Decimal(str(rating or "0"))
            else:
                rating = OverallRating.objects.get(
                    object_id = obj.pk,
                    content_type = ct,
                    category = category_value(obj, category)
                ).rating or 0
        except OverallRating.DoesNotExist:
            rating = 0
        context[self.as_var] = rating
        return ""


@register.tag
def overall_rating(parser, token):
    """
    Usage:
        {% overall_rating obj [category] as var %}
    """
    return OverallRatingNode.handle_token(parser, token)


def rating_post_url(user, obj):
    ct = ContentType.objects.get_for_model(obj)
    post_url = reverse(
        "agon_ratings_rate",
        kwargs = {
            "content_type_id": ct.pk,
            "object_id": obj.pk
        }
    )
    return post_url


@register.inclusion_tag("agon_ratings/_script.html")
def user_rating_js(user, obj, category=None):
    post_url = rating_post_url(user, obj)
    rating = user_rating_value(user, obj, category)
    
    return {
        "obj": obj,
        "post_url": post_url,
        "category": category,
        "the_user_rating": rating,
        "STATIC_URL": settings.STATIC_URL,
    }


@register.assignment_tag
def ratings(obj):
    ct = ContentType.objects.get_for_model(obj)
    try:
        return OverallRating.objects.get(
            content_type=ct,
            object_id=obj.pk,
            category=None
        ).ratings.all()
    except OverallRating.DoesNotExist:
        return []


@register.simple_tag
def user_rating_url(user, obj):
    return rating_post_url(user, obj)

