from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from agon_ratings.models import Rating, OverallRating


NUM_OF_RATINGS = getattr(settings, "AGON_NUM_OF_RATINGS", 5)


@require_POST
@login_required
def rate(request, content_type_id, object_id):
    ct = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ct.model_class(), pk=object_id)
    rating_input = int(request.POST.get("rating"))
    
    data = {
        "user_rating": rating_input,
        "overall_rating": 0
    }
    
    # @@@ Seems like this could be much more DRY with a model method or something
    if rating_input == 0: # clear the rating
        try:
            rating = Rating.objects.get(
                object_id = object_id,
                content_type = ct,
                user = request.user
            )
            overall = rating.overall_rating
            rating.delete()
            overall.update()
            data["overall_rating"] = str(overall.rating)
        except Rating.DoesNotExist:
            pass
    elif 1 <= rating_input <= NUM_OF_RATINGS: # set the rating
        rating, created = Rating.objects.get_or_create(
            object_id = obj.pk,
            content_type = ct,
            user = request.user,
            defaults = {
                "rating": rating_input
            }
        )
        overall, created = OverallRating.objects.get_or_create(
            object_id = obj.pk,
            content_type = ct
        )
        rating.overall_rating = overall
        rating.rating = rating_input
        rating.save()
        overall.update()
        data["overall_rating"] = str(overall.rating)
    else: # whoops
        return HttpResponseForbidden(
            "Invalid rating. It must be a value between 0 and %s" % NUM_OF_RATINGS
        )
    
    return HttpResponse(json.dumps(data), mimetype="application/json")
