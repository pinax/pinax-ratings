from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import simplejson as json
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType

from agon_ratings.models import Rating, OverallRating
from agon_ratings.categories import is_valid_category


NUM_OF_RATINGS = getattr(settings, "AGON_NUM_OF_RATINGS", 5)


@login_required(redirect_field_name='rate')
def rate(request, content_type_id, object_id):

    ct = get_object_or_404(ContentType, pk=content_type_id)
    obj = get_object_or_404(ct.model_class(), pk=object_id)
    rating_input = int(request.POST.get("rating", -1))

    category = request.POST.get("category", None)
    if not is_valid_category(obj, category):
        return HttpResponseForbidden(
            "Invalid category. It must match a preconfigured setting"
        )

    if request.method != 'POST':
        return render(request, 'agon_ratings/rate_object.html', {
            'obj': obj,
        })
    
    # Check for errors and bail early
    if not (0 <= rating_input <= NUM_OF_RATINGS):
        return HttpResponseForbidden(
            "Invalid rating. It must be a value between 0 and %s" % NUM_OF_RATINGS
        )
    
    data = {
        "userRating": rating_input,
        "overallRating": 0,
        "category": category,
        "numOfRatings": NUM_OF_RATINGS,
    }

    overall, created = OverallRating.objects.get_or_create(
        object_id = obj.pk,
        content_type = ct,
        category = category,
    )
    
    # @@@ Seems like this could be much more DRY with a model method or something
    if rating_input == 0: # clear the rating
        try:
            rating = Rating.objects.get(
                object_id = object_id,
                content_type = ct,
                user = request.user,
                category = category
            )

            rating.delete()
            overall.update()

        except Rating.DoesNotExist:
            pass

    else: # set the rating
        rating, created = Rating.objects.get_or_create(
            object_id = obj.pk,
            content_type = ct,
            user = request.user,
            category = category,
            defaults = {
                "rating": rating_input
            }
        )
        rating.overall_rating = overall
        rating.rating = rating_input
        rating.save()

        overall.update()
    
    data["overallRating"] = float(overall.rating)
    
    # TODO Actually work with the Accept header, 
    if request.is_ajax():
        return HttpResponse(json.dumps(data), mimetype="application/json")
    else:
        return HttpResponseRedirect(request.META.get('Referer') or (obj.get_absolute_url and obj.get_absolute_url()) or '/')
