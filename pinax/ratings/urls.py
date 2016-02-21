from django.conf.urls import url

from pinax.ratings import views

urlpatterns = [
    url(r"^(?P<content_type_id>\d+)/(?P<object_id>\d+)/rate/$", views.RateView.as_view(), name="pinax_ratings_rate"),
]
