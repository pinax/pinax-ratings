from decimal import Decimal

from django import template
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType

from agon_ratings.models import Rating, OverallRating


NUM_OF_RATINGS = getattr(settings, "AGON_NUM_OF_RATINGS", 5)


register = template.Library()


def guard_argument_count(bits, min_count, max_count):
    if len(bits) < min_count:
        raise template.TemplateSyntaxError("Too few arguments provided to %r" % bits[0])
    if len(bits) > max_count:
        raise template.TemplateSyntaxError("Too many arguments provided to %r" % bits[0])


def user_rating_value(user, obj, category=None):

    if user.is_anonymous():
        return None

    rating = None
    try:
        rating = Rating.objects.get(
            user = user,
            category=category,
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
        ).rating
    except Rating.DoesNotExist:
        pass

    return rating


class UserRatingNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()

        guard_argument_count(bits, min_count=5, max_count=6)

        if len(bits) == 5:
            category = None
        elif len(bits) == 6:
            category = parser.compile_filter(bits[3])
        
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


class UserRatingWidgetNode(template.Node):

    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        
        guard_argument_count(bits, min_count=3, max_count=4)

        if len(bits) == 3:
            category = None
        elif len(bits) == 4:
            category = parser.compile_filter(bits[3])

        return cls(
            user = parser.compile_filter(bits[1]),
            obj = parser.compile_filter(bits[2]),
            category = category,
        )

    def __init__(self, user,obj, category=None):
        self.user = user
        self.obj = obj
        self.category = category

    def render(self, context):

        user = self.user.resolve(context)
        obj = self.obj.resolve(context)

        app_name = obj._meta.app_label
        model_name = obj._meta.object_name

        if self.category:
            category = self.category.resolve(context)
            widget_id = 'agon_rating_%s_%s_%s_%s' % (app_name, model_name, category, obj.pk)
        else:
            category = None
            widget_id = 'agon_rating_%s_%s_%s' % (app_name, model_name, obj.pk)

        agon_rating_context = {
            'widget_id': widget_id, # TODO make this configurable
            'category': category,
            'user': user,
            'obj': obj,
            'action_url': rating_post_url(user, obj),
            'rating_range': range(1, NUM_OF_RATINGS + 1),
            'current_rating': user_rating_value(user, obj, category),
        }

        return render_to_string([
            'agon_ratings/%s/%s_%s.html' % (app_name, model_name, category),
            'agon_ratings/%s/%s_rating.html' % (app_name, model_name),
            'agon_ratings/%s/rating.html' % (app_name),
            'agon_ratings/_widget.html',
        ], agon_rating_context, context)

@register.tag
def user_rating_widget(parser, token):
    return UserRatingWidgetNode.handle_token(parser, token)

class OverallRatingNode(template.Node):
    
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.split_contents()
        category = None
        
        guard_argument_count(bits, min_count=4, max_count=5)
        
        if len(bits) >= 5:
            category = parser.compile_filter(bits[2])
        
        return cls(
            obj = parser.compile_filter(bits[1]),
            as_var = bits[len(bits) - 1],
            category = category,
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
            rating = OverallRating.objects.get(
                object_id = obj.pk,
                content_type = ct,
                category = category,
            ).rating
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
def user_rating_js():
    return {"STATIC_URL": settings.STATIC_URL}

@register.inclusion_tag("agon_ratings/_style.html")
def user_rating_css():
    return {"STATIC_URL": settings.STATIC_URL}


@register.simple_tag
def user_rating_url(user, obj):
    return rating_post_url(user, obj)

