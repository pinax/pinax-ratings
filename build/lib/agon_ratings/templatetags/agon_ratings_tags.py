from django import template

from django.contrib.contenttypes.models import ContentType

from agon_ratings.models import Rating, OverallRating


register = template.Library()


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
        try:
            ct = ContentType.objects.get_for_model(obj)
            rating = Rating.objects.get(
                object_id = obj.pk,
                content_type = ct,
                user = user
            ).rating
        except Rating.DoesNotExist:
            rating = 0
        context[self.as_var] = rating


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
        except Rating.DoesNotExist:
            rating = 0
        context[self.as_var] = rating


@register.tag
def overall_rating(parser, token):
    """
    Usage:
        {% overall_rating for obj as var %}
    """
    return OverallRatingNode.handle_token(parser, token)


@register.inclusion_tag("agon_ratings/_rate_form.html")
def user_rate_form(obj):
    ct = ContentType.objects.get_for_model(obj)
    return {"ct": ct, "obj": obj}
