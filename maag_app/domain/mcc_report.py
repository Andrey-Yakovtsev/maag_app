"""
Построение отчета по МСС
"""
import datetime
import logging

logger = logging.getLogger(__name__)

import django_tables2 as tables

from maag_app.domain.models import Product
from maag_app.sales.models import Sales
from maag_app.stocks.models import Stock


class MccTable(tables.Table):
    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap.html"
        fields = ("mcc",)


class MccReport:
    """
    Построение отчета по каждому отдельному МСС на указанную (или дефолтную дату)
    """
    def __init__(self, mcc: str, date: datetime.date = datetime.date.today()):
        self.mcc = self._get_mcc(mcc)
        self.date = date
        self.report_range = self._set_report_period_in_weeks()

    @staticmethod
    def _get_mcc(mcc) -> Product:
        try:
            mcc_from_db = Product.objects.filter(mcc=mcc).first()
            logger.debug(f'Product with given MCC: {mcc_from_db.mcc} found')
            return mcc_from_db
        except Product.DoesNotExist as err:
            logger.error(f'No product with given MCC: {mcc}. Error: {err}')

    def _set_report_period_in_days(self) -> list[datetime.date, datetime.date]:
        """Расчитывает начало и конец отчетного периода в днях."""
        start_date = self.date - datetime.timedelta(weeks=4)
        end_date = self.date + datetime.timedelta(weeks=8)
        logger.debug(f'_set_report_period_in_days ==> {[start_date, end_date]}')
        return [start_date, end_date]

    def _set_report_period_in_weeks(self) -> list[int]:
        """Получает начало и конец отчетного периода в неделях для фильтра кверисета"""
        return list(self._set_weeks_numbers())

    def _set_weeks_numbers(self) -> set[int]:
        """Расчитывает начало и конец отчетного периода в неделях."""
        week_numbers = set()
        delta = datetime.timedelta(days=1)
        start_date, end_date = self._set_report_period_in_days()
        while start_date <= end_date:
            week_numbers.add(start_date.isocalendar()[1])
            start_date += delta
            [start_date, end_date]
        logger.debug(f'_set_weeks_numbers ==> {week_numbers}')
        return week_numbers

    def _get_actual_sales(self) -> list[int]:
            # FIXME добавить выборку по неделям и додумать, как по годам будет...
        sales = Sales.objects.filter(
                mcc=self.mcc,
                week__in=self.report_range
            ).select_related("mcc").values_list("quantity", flat=True)
        logger.debug(f'{self.mcc=}, '
                     f'{self.report_range=}, '
                     f'_get_actual_sales ==> {sales}')
        return sales

    def _get_mirror_mcc_sales(self) -> list[int]:
        if self.mcc.mirror_mcc:
            return (
                Sales.objects.filter(
                    mcc=self.mcc.mirror_mcc,
                    week__in=self.report_range
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
        stocks = Stock.objects.filter(
                mcc=self.mcc,
                week__in=self.report_range
            ).select_related("mcc").values_list("stores_qty", flat=True)
        logger.debug(f'{self.mcc=}, '
                     f'{self.report_range=}, '
                     f'_get_stocks ==> {stocks}')
        return stocks

    def _get_aggergated_data(self):
        """ВСе добытые МСС агреггируем тут"""
        pass

    def _get_planned_sales(self):
        pass

    def _get_mcc_metrics(self):
        """Вытащить сюда все данные из пропертей"""
        pass

    def generate(self):
        """ Генерирует контекст для вывода на странице отчета. """
        return {
            "weeks": self._set_weeks_numbers(),
            "sales": self._get_actual_sales(),
            "mirror_mcc_sales": self._get_mirror_mcc_sales(),
            "stocks": self._get_stocks()
        }

# report = MccReport("000/0012/1231")
# TODO  Добавить автоматизацию создания в админке и
#  насаздовать продуктов и стоков и заказос и выводиь уже репорт.
# print(report.generate())
