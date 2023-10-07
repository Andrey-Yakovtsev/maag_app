from django.urls import path

from maag_app.products.views import MccReportView, sales_form_view

app_name = "domain"
urlpatterns = [
    path(
        "mcc-report/",
        MccReportView.as_view(),
        name="mcc_report",
    ),
    path(
        "planned-sales/",
        sales_form_view,
        name="sales_plans",
    ),
]
