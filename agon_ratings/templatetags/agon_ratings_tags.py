from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType

from agon_ratings.models import Rating, OverallRating


register = template.Library()


def get_user_rating(user, obj):
    try:
        ct = ContentType.objects.get_for_model(obj)
        rating = Rating.objects.get(
            object_id = obj.pk,
            content_type = ct,
            user = user
        ).rating
    except Rating.DoesNotExist:
        rating = 0
    return rating


class UserRatingNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 7:
            raise template.TemplateSyntaxError()
        return cls(
            user = parser.compile_filter(bits[2]),
            obj = parser.compile_filter(bits[4]),
            as_var = bits[6]
        )
    
    def __init__(self, user, obj, as_var):
        self.user = user
        self.obj = obj
        self.as_var = as_var
    
    def render(self, context):
        user = self.user.resolve(context)
        obj = self.obj.resolve(context)
        context[self.as_var] = get_user_rating(user, obj)
        return ""


@register.tag
def user_rating(parser, token):
    """
    Usage:
        {% user_rating for user and obj as var %}
    """
    return UserRatingNode.handle_token(parser, token)


class OverallRatingNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        if len(bits) != 5:
            raise template.TemplateSyntaxError()
        return cls(
            obj = parser.compile_filter(bits[2]),
            as_var = bits[4]
        )
    
    def __init__(self, obj, as_var):
        self.obj = obj
        self.as_var = as_var
    
    def render(self, context):
        obj = self.obj.resolve(context)
        try:
            ct = ContentType.objects.get_for_model(obj)
            rating = OverallRating.objects.get(
                object_id=obj.pk,
                content_type=ct
            ).rating or 0
        except OverallRating.DoesNotExist:
            rating = 0
        context[self.as_var] = rating
        return ""


@register.tag
def overall_rating(parser, token):
    """
    Usage:
        {% overall_rating for obj as var %}
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
def user_rating_js(user, obj):
    post_url = rating_post_url(user, obj)
    rating = get_user_rating(user, obj)
    
    return {
        "obj": obj,
        "post_url": post_url,
        "the_user_rating": rating,
        "STATIC_URL": settings.STATIC_URL
    }


@register.simple_tag
def user_rating_url(user, obj):
    return rating_post_url(user, obj)

