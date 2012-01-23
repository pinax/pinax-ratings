from django.conf import settings


AGON_RATINGS_CATEGORY_CHOICES = getattr(settings, "AGON_RATINGS_CATEGORY_CHOICES", {})
ALLOWED_RATINGS = {}

if len(AGON_RATINGS_CATEGORY_CHOICES.keys()) > 0:
    for model_str in AGON_RATINGS_CATEGORY_CHOICES.keys():
        categories = AGON_RATINGS_CATEGORY_CHOICES[model_str]

        if categories is True:
            categories = []

        ALLOWED_RATINGS[model_str] = categories


def get_model_string(obj):
    """
    Takes a model instance, and returns a unique identifier for this model type
    """
    return "%s.%s" % (obj._meta.app_label, obj._meta.object_name)


def is_valid_category(obj, category=None):
    """
    Check if a given object and category is a valid combination for rating

    Parameters:
        obj - The object that is being rated
        category - The rating category. Can be None.

    Returns:
    True if the combination of object and category is valid, False otherwise
    """
    obj_str = get_model_string(obj)
    if obj_str not in ALLOWED_RATINGS:
        return False

    if category is None:
        return True
    else:
        return category in ALLOWED_RATINGS[obj_str]
