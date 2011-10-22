from django.conf import settings


RATING_CATEGORY_CHOICES_DICT = getattr(settings, "AGON_RATINGS_CATEGORY_CHOICES", {})
RATING_CATEGORY_CHOICES = []
RATING_CATEGORY_LOOKUP = {}
if len(RATING_CATEGORY_CHOICES_DICT.keys()) > 0:
    for model_str in RATING_CATEGORY_CHOICES_DICT.keys():
        for choice in RATING_CATEGORY_CHOICES_DICT[model_str].keys():
            slug = "%s-%s" % (model_str, choice)
            val = len(RATING_CATEGORY_CHOICES) + 1
            RATING_CATEGORY_CHOICES.append((val, slug))
            RATING_CATEGORY_LOOKUP[slug] = val


def category_label(obj, choice):
    obj_str = "%s.%s" % (obj._meta.app_label, obj._meta.object_name)
    return RATING_CATEGORY_CHOICES_DICT.get(obj_str, {}).get(choice)


def is_valid_category(obj, choice):
    return category_label(obj, choice) is not None


def category_value(obj, choice):
    return RATING_CATEGORY_LOOKUP.get(
        "%s.%s-%s" % (obj._meta.app_label, obj._meta.object_name, choice)
    )
