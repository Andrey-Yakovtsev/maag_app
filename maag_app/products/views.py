import datetime
import logging
from copy import deepcopy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django_filters.views import FilterView

from maag_app.products.filters import MccFilter
from maag_app.products.forms import PlannedForm
from maag_app.products.mcc_report import MccReport
from maag_app.products.models import Product
from maag_app.products.utils import (
    get_latest_orders_report_date,
    get_latest_sales_report_date,
    get_latest_stock_report_date,
)
from maag_app.sales.models import Sales

logger = logging.getLogger()


def index_view(request):
    return redirect("domain:mcc_report")


class MccReportView(FilterView):
    model = Product
    filterset_class = MccFilter

    def get(self, request, *args, **kwargs):
        filterset_class = self.get_filterset_class()
        self.filterset = self.get_filterset(filterset_class)

        if (
            not self.filterset.is_bound
            or self.filterset.is_valid()
            or not self.get_strict()
        ):
            self.object_list = self.filterset.qs
        else:
            self.object_list = self.filterset.queryset.none()

        context = self.get_context_data(
            filter=self.filterset, object_list=self.object_list
        )
        context["dates"] = {
            "sales": get_latest_sales_report_date(),
            "stock": get_latest_stock_report_date(),
            "orders": get_latest_orders_report_date(),
        }

        context["planned_form"] = PlannedForm()
        entry_date = kwargs.get("store_entry_date")
        if entry_date and isinstance(entry_date, datetime.date):
            store_entry_date = entry_date
        elif entry_date and isinstance(entry_date, str):
            store_entry_date = datetime.datetime.strptime(entry_date, "%m/%d/%Y")
        else:
            store_entry_date = datetime.date.today()
        context["dates"]["store_entry_date"] = store_entry_date
        for mcc in self.filterset.qs:
            report = MccReport(mcc.mcc, store_entry_date).generate()
            mcc.country_stock = report["country_stock"]
            mcc.stores_stock = report["stores_stock"]
            mcc.rotation = report["rotation"]
            mcc.sellthrough = report["sellthrough"]
            mcc.pending_delivery = report["pending_delivery"]
            mcc.purchased = report["purchased"]
            mcc.sales_result = report["actual_sales"]
            mcc.sales_plans = report["planned_sales"]
            mcc.week_numbers = report["weeks"]
            mcc.start_days = report["days"]
            mcc.mirror_mcc_sales = report["mirror_mcc_sales"]
            mcc.stocks_data = report["stocks"]
            # logger.debug(f"MCC DATA ==> {mcc.__dict__}")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if store_entry_date := request.POST.get("store_entry_date"):
            logger.info(f"INSIDE POST Running get for new date {store_entry_date=}")
            return self.get(request, *args, store_entry_date=store_entry_date, **kwargs)

        form = PlannedForm(request.POST)
        entry_date = request.POST.get("date")
        store_entry_date = (
            datetime.datetime.strptime(entry_date, "%d/%m/%Y")
            if entry_date
            else datetime.date.today()
        )
        logger.info(f"{entry_date=}, {store_entry_date=}")
        if form.is_valid():
            week = form.cleaned_data["date"].isocalendar()[1]
            year = form.cleaned_data["date"].year
            obj, _ = Sales.objects.update_or_create(
                mcc=form.cleaned_data["mcc"],
                year=year,
                week=week,
                defaults={"planned": form.cleaned_data["planned"]},
            )
            logger.info(
                f"INSIDE POST. Form IS valid. Sales plan entry {'updated' if _ else 'created'}: {obj}"
            )
            return self.get(request, *args, store_entry_date=store_entry_date)
        logger.info("INSIDE POST. Form NOT VALID")
        return self.get(request, *args, store_entry_date=entry_date)
