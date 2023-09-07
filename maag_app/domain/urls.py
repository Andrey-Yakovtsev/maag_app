from django.urls import path
from django_filters.views import FilterView

from maag_app.domain.models import Product

app_name = "domain"
urlpatterns = [
    path(
        "mcc-report/",
        FilterView.as_view(
            model=Product,
            filterset_fields=["subfamily", "family", "group", "section", "season"],
            extra_context={"foo": {"some": "bar"}},
        ),
        name="mcc_report",
    ),
]
