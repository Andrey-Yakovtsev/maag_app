from django.urls import path

from maag_app.domain.models import Product
from django_filters.views import FilterView


app_name = "domain"
urlpatterns = [
    path("mcc-report-filter/", FilterView.as_view(model=Product), name="mcc_report"),
]
