from django.http import HttpResponse
from django.template import loader
from django_filters.views import FilterView

from maag_app.domain.filters import MccFilter
from maag_app.domain.models import Product
from maag_app.domain.utils import get_latest_sales_report_date, \
    get_latest_stock_report_date, get_latest_orders_report_date


def mcc_report_view(request):
    context = {}
    mcc_filter = MccFilter(request.GET, queryset=Product.objects.select_related().all())
    template = loader.get_template('domain/product_filter.html')
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
        # TODO - Продолжить с контекстом
        return self.render_to_response(context)
