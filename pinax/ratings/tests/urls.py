from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("pinax.ratings.urls", namespace="pinax_ratings")),
]
