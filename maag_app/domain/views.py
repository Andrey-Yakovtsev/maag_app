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


# TODO попробовал от таблицы к фильтрам идти... Надо видимо на микро варианте раскурить...
