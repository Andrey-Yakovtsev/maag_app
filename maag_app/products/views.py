import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
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

logger = logging.getLogger()


def mcc_report_view(request):
    context = {}
    mcc_filter = MccFilter(request.GET, queryset=Product.objects.select_related().all())
    template = loader.get_template("domain/product_filter.html")
    context["filter"] = mcc_filter
    context["dates"] = {
        "sales": get_latest_sales_report_date(),
        "stock": get_latest_stock_report_date(),
        "orders": get_latest_orders_report_date(),
    }
    # TODO Понять как к странице с фильтром на полученный
    #  кверисет прикручивать контекст...
    return HttpResponse(template.render(context, request))


class MccReportView(FilterView):
    model = Product
    filterset_class = MccFilter
    # template_name = "report_simple.html"

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

        for mcc in self.filterset.qs:
            report = MccReport(mcc.mcc).generate()
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
            # logger.info(f"MCC DATA ==> {mcc.__dict__}")
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = PlannedForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            logger.info(f"Form content ==> {form.data}")
            # redirect to a new URL:
            return form


def sales_form_view(request):
    # logger.info(f"SALES FORM request ==>> {request.__dict__}")
    # logger.info(f"SALES FORM request ==>> {request.data}")
    if request.method == "POST":
        logger.info(f"POST FORM request method ==>> {request.method}")
        # logger.info(f"POST FORM DATA ==>> {request.data}")
        # create a form instance and populate it with data from the request:
        form = PlannedForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            logger.info(f"Form content ==> {form.data}")
            # redirect to a new URL:
            return render(
                request,
                "pages/report_simple.html",
                {"form": form, "request_m": request.method},
            )

        return render(
            request,
            "pages/report_simple.html",
            {"form": form, "request_m": request.__dict__},
        )
        # if a GET (or any other method) we'll create a blank form
    else:
        logger.info(f"POST FORM request method ==>> {request.method}")
        # logger.info(f"REQUEST context ==>> {request.context}")
        form = PlannedForm()

    return render(
        request,
        "pages/report_simple.html",
        {"form": form, "request_m": request.__dict__},
    )
