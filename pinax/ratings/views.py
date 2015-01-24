from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from django.contrib.contenttypes.models import ContentType

from account.decorators import login_required

from .categories import category_value
from .models import Rating


NUM_OF_RATINGS = getattr(settings, "PINAX_RATINGS_NUM_OF_RATINGS", 5)


@require_POST
@login_required
def rate(request, content_type_id, object_id):
    ct = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ct.model_class(), pk=object_id)
    rating_input = int(request.POST.get("rating"))
    category = request.POST.get("category")
    cat_choice = category_value(obj, category)

    # Check for errors and bail early
    if category is not None and cat_choice is None:
        return HttpResponseForbidden(
            "Invalid category. It must match a preconfigured setting"
        )
    if rating_input not in range(NUM_OF_RATINGS + 1):
        return HttpResponseForbidden(
            "Invalid rating. It must be a value between 0 and %s" % NUM_OF_RATINGS
        )

    data = {
        "user_rating": rating_input,
        "overall_rating": 0,
        "category": category
    }

    data["overall_rating"] = Rating.update(
        rating_object=obj,
        user=request.user,
        category=cat_choice,
        rating=rating_input
    )

    return JsonResponse(data)
