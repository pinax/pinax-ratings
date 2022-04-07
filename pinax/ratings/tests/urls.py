try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url

from django.conf.urls import include

urlpatterns = [
    url(r"^", include("pinax.ratings.urls", namespace="pinax_ratings")),
]
