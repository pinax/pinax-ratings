try:
    from django.conf.urls import url
except ImportError:  # pragma: no cover
    from django.urls import re_path as url  # pragma: no cover

from pinax.ratings import views

app_name = "pinax_ratings"


urlpatterns = [
    url(r"^(?P<content_type_id>\d+)/(?P<object_id>\d+)/rate/$", views.RateView.as_view(), name="rate"),
]
