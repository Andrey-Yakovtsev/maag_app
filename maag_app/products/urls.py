from django.urls import path

from maag_app.products.views import MccReportView, mcc_report_view

app_name = "domain"
urlpatterns = [
    path(
        "mcc-report/",
        MccReportView.as_view(),
        name="mcc_report",
    ),
]
