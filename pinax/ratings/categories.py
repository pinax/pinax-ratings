from django.conf import settings

RATING_CATEGORY_CHOICES_DICT = getattr(settings, "PINAX_RATINGS_CATEGORY_CHOICES", {})
RATING_CATEGORY_CHOICES = []
RATING_CATEGORY_LOOKUP = {}
for model_str in RATING_CATEGORY_CHOICES_DICT.keys():
    for choice in RATING_CATEGORY_CHOICES_DICT[model_str].keys():
        slug = "{}-{}".format(model_str, choice)
        RATING_CATEGORY_CHOICES.append((choice, slug))
        RATING_CATEGORY_LOOKUP[slug] = choice


def category_label(obj, choice):
    obj_str = "{}.{}".format(obj._meta.app_label, obj._meta.object_name)
    return RATING_CATEGORY_CHOICES_DICT.get(obj_str, {}).get(choice)


def is_valid_category(obj, choice):
    return category_label(obj, choice) is not None


def category_value(obj, choice):
    return RATING_CATEGORY_LOOKUP.get(
        "{}.{}-{}".format(obj._meta.app_label, obj._meta.object_name, choice)
    )
