from django.http import HttpResponse
from django.template import loader
from django.views.generic import TemplateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .filters import MccFilter
from .mcc_report import MccTable
from .models import Product


class MccListView(SingleTableMixin, FilterView):
    table_class = MccTable
    model = Product
    template_name = "product_list.html"
    filterset_class = MccFilter


class ReportView(TemplateView):
    template_name = "report_simple.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["new_stuff"] = {"bull": "shit"}

        print("context.__dict__====>>>", context.items())


def testing(request):
  template = loader.get_template('report_simple.html')
  context = {"new_stuff": {"bull": "shit"}}
  # TODO Понять как к странице с фильтром на полученный
  #  кверисет прикручивать контекст...
  return HttpResponse(template.render(context, request))
