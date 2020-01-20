from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import View

from .categories import category_value
from .models import Rating

try:
    from account.mixins import LoginRequiredMixin
except ImportError:  # pragma: no cover
    from django.contrib.auth.mixins import LoginRequiredMixin  # pragma: no cover

NUM_OF_RATINGS = getattr(settings, "PINAX_RATINGS_NUM_OF_RATINGS", 5)


class RateView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        ct = get_object_or_404(ContentType, pk=self.kwargs.get("content_type_id"))
        obj = get_object_or_404(ct.model_class(), pk=self.kwargs.get("object_id"))
        rating_input = int(request.POST.get("rating"))
        category = request.POST.get("category", "")
        cat_choice = category_value(obj, category)

        # Check for errors and bail early
        if category and cat_choice is None:
            return HttpResponseForbidden(
                "Invalid category. It must match a preconfigured setting"
            )
        if rating_input not in range(NUM_OF_RATINGS + 1):
            return HttpResponseForbidden(
                "Invalid rating. It must be a value between 0 and {}".format(NUM_OF_RATINGS)
            )

        data = {
            "user_rating": rating_input,
            "category": category,
            "overall_rating": Rating.update(
                rating_object=obj,
                user=request.user,
                category=cat_choice,
                rating=rating_input
            )
        }
        # add support for eldarion-ajax
        data.update({
            "content_type_id": self.kwargs.get("content_type_id"),
            "object_id": self.kwargs.get("object_id")
        })
        data.update({
            "html": render_to_string("pinax/ratings/_rating.html", data, request)
        })
        return JsonResponse(data)
