from django.conf.urls import url

from pinax.ratings import views

app_name = "pinax_ratings"


urlpatterns = [
    url(r"^(?P<content_type_id>\d+)/(?P<object_id>\d+)/rate/$", views.RateView.as_view(), name="rate"),
]
