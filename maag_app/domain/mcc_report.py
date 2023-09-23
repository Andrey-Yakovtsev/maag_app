"""
Построение отчета по МСС
"""
import datetime
import logging

logger = logging.getLogger(__name__)

# import django_tables2 as tables

from maag_app.domain.models import Product
from maag_app.sales.models import Sales
from maag_app.stocks.models import Stock

four_weeks_bckwd = datetime.date.today() - datetime.timedelta(weeks=4)


# class MccTable(tables.Table):
#     class Meta:
#         model = Product
#         template_name = "django_tables2/bootstrap.html"
#         fields = ("mcc",)


class MccReport:
    """
    Построение отчета по каждому отдельному МСС на указанную (или дефолтную дату)
    """

    def __init__(self, mcc: str, date: datetime.date = datetime.date.today()):
        self.mcc = self._get_mcc(mcc)
        self.date = date
        self.week_number: int = self.date.isocalendar()[1]
        # FIXME заменить на список номеров недель... - функцию.
        self.report_range = None

    @staticmethod
    def _get_mcc(mcc) -> Product:
        try:
            return Product.objects.filter(mcc=mcc).first()
        except Product.DoesNotExist as err:
            logger.error(f'No product with given MCC: {mcc}. Error: {err}')

    def _set_report_period(self) -> None:
        """Устанавливает период для отчета на 12 недель"""
        start_date = self.date - datetime.timedelta(weeks=4)
        end_date = self.date + datetime.timedelta(weeks=8)
        self.report_range = [start_date, end_date]

    def _get_actual_sales(self) -> list[int]:
        return (
            Sales.objects.filter(
                mcc=self.mcc,
                date__range=self.report_range
            )
            .select_related("mcc")
            .values_list("quantity", flat=True)
        )

    def _get_mirror_mcc_sales(self) -> list[int]:
        if self.mcc.mirror_mcc:
            return (
                Sales.objects.filter(
                    mcc=self.mcc.mirror_mcc,
                    date__range=self.report_range
                )
                .select_related("mcc")
                .values_list("quantity", flat=True)
            )
        else:
            # Если миррор не присвоен, то берем от текущего МСС все МСС, что
            # выфильтровываются по 5 фильтрам и выводим средние продажи
            # по неделям для них - должен получиться list[int]
            return []
            # TODO доделаю позже, как разберусь с основной формой

    def _get_stocks(self) -> list[int]:
        return (
            Stock.objects.filter(
                mcc=self.mcc,
                date__range=self.report_range
            )
            .select_related("mcc")
            .values_list("stores_qty", "country_qty", flat=True)
        )

    def _get_aggergated_data(self):
        """ВСе добытые МСС аггрегируем тут"""
        pass


    def _get_planned_sales(self):
        pass


    def _get_mcc_metrics(self):
        """Вытащить сюда все данные из пропертей"""
        pass
    def generate(self):
        """ Генерирует контекст для вывода на странице отчета. """
        sales = self._get_actual_sales()
        mcc_sales = self._get_mirror_mcc_sales()
        stocks = self._get_stocks()
        return {
            # "weeks":
            "sales": sales,
            "mcc_sales": mcc_sales,
            "stocks": stocks
        }

report = MccReport("000/0012/1231")

print(report.generate())
