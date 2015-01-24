from django.conf.urls import patterns, url


urlpatterns = patterns(
    "pinax.ratings.views",
    url(r"^(?P<content_type_id>\d+)/(?P<object_id>\d+)/rate/$", "rate", name="pinax_ratings_rate"),
)
