from django.urls import path
from django_filters.views import FilterView

from maag_app.domain.models import Product
from maag_app.domain.utils import (
    get_latest_orders_report_date,
    get_latest_sales_report_date,
    get_latest_stock_report_date,
)
from maag_app.domain.views import ReportView, testing

app_name = "domain"
urlpatterns = [
    path(
        "mcc-report/",
        FilterView.as_view(
            model=Product,
            filterset_fields=["subfamily", "family", "group", "section", "season"],
            extra_context={
                "dates": {
                    "sales": get_latest_sales_report_date(),
                    "stock": get_latest_stock_report_date(),
                    "orders": get_latest_orders_report_date(),
                }
            },
        ),
        name="mcc_report",
    ),
    path("mcc-report-2/", testing, name="mcc_report_2",),
]
