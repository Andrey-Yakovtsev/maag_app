"""
Построение отчета по МСС
"""
import datetime
import logging
from array import array

from django.db.models import Model, Sum
from django.forms import forms

from maag_app.orders.models import OrderItem
from maag_app.products.forms import PlannedForm

logger = logging.getLogger(__name__)


from maag_app.products.models import Product
from maag_app.sales.models import Sales
from maag_app.stocks.models import Stock


class MccReport:
    """
    Построение отчета по каждому отдельному МСС на указанную (или дефолтную дату)
    """

    def __init__(self, mcc: str, date: datetime.date = datetime.date.today()):
        self.mcc: str = self._get_mcc(mcc)
        self.date: datetime.date = date
        self.report_range: list[int] = self._set_report_period_in_weeks()
        self.report_range_weeks_count: int = 13

    @staticmethod
    def _get_mcc(mcc) -> Product:
        try:
            mcc_from_db = Product.objects.filter(mcc=mcc).first()
            logger.debug(f"Product with given MCC: {mcc_from_db.mcc} found")
            return mcc_from_db
        except Product.DoesNotExist as err:
            logger.error(f"No product with given MCC: {mcc}. Error: {err}")

    def _set_report_period_in_days(self) -> list[datetime.date, datetime.date]:
        """Расчитывает начало и конец отчетного периода в днях."""
        start_date = self.date - datetime.timedelta(weeks=4)
        end_date = self.date + datetime.timedelta(weeks=8)
        logger.debug(f"_set_report_period_in_days ==> {[start_date, end_date]}")
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
        logger.debug(f"_set_weeks_numbers ==> {week_numbers}")
        return week_numbers

    def _set_weeks_starting_dates(self) -> list[datetime.date]:
        """Расчитывает начало отчетной недели и от него собирает строку с датами."""
        first_day_of_week = self.date + datetime.timedelta(days=-self.date.weekday())
        start_date = first_day_of_week - datetime.timedelta(weeks=4)
        days_list = [start_date]
        for i in range(1, self.report_range_weeks_count):
            days_list.append(start_date + datetime.timedelta(weeks=i))
        logger.debug(f"{self.mcc=}, " f"_set_weeks_starting_dates ==> {days_list}")
        return days_list

    def _get_actual_report_data(
        self,
        model: Model,
        value: str,
        attr_name: str = "quantity",
        use_mirror: bool = False,
    ) -> list[int] | array:
        """
        Универсальный метод для заполнения табличек из кверисета или перебора циклом.
        attrs: model - указание модели
        value: какое поле из таблицы выбирать
        """
        mcc = self.mcc if not use_mirror else self.mcc.mirror_mcc
        logger.info(f"REPORT RANGE WEEKS {self.report_range=}")
        result_qs = model.objects.filter(
            mcc=mcc, week__in=self.report_range
        ).select_related("mcc")
        if result_qs.count() >= len(self.report_range):
            # logger.info(f"{model} QS is full. Returning a values_list")
            logger.info(f"{result_qs.values_list(value, flat=True)=}")
            logger.info(f"QS without FLAT{result_qs=}")
            return result_qs.values_list(value, flat=True)

        else:
            logger.info(f"{model} QS is not full. Iterating ove a QS by weeks")
            weekly_report = array("L", [])
            for week in self.report_range:
                if (
                    data := model.objects.filter(mcc=self.mcc, week=week)
                    .select_related()
                    .first()
                ):
                    weekly_report.append(getattr(data, attr_name))
                else:
                    weekly_report.append(0)
            return weekly_report

    def _get_actual_sales(self) -> list[int] | array:
        # FIXME как по годам будет перенос недель???
        return self._get_actual_report_data(Sales, "quantity")

    def _get_planned_sales(self) -> list[dict[str, int]]:
        # FIXME как по годам будет перенос недель???
        plans = self._get_actual_report_data(Sales, "planned")
        days = self._set_weeks_starting_dates()
        # logger.info(f"PLANS {plans=}")
        # logger.info(f"DAYS {days=}")
        report = []
        result = dict(zip(days, plans))
        logger.info(f"PLANNED ZIP {result=}")
        for k, v in result.items():
            report.append({"day": k, "plan": v})
        logger.info(f"PLANNED {report=}")
        return report

    def _get_mirror_mcc_sales(self) -> list[int] | array:
        if self.mcc.mirror_mcc:
            return self._get_actual_report_data(Sales, "quantity", use_mirror=True)
        else:
            # Если миррор не присвоен, то берем от текущего МСС все МСС, что
            # выфильтровываются по 5 фильтрам и выводим средние продажи
            # по неделям для них - должен получиться list[int]
            return []
            # TODO доделаю позже, как разберусь с основной формой

    def _get_weekly_stocks(self) -> list[int]:
        stocks = self._get_actual_report_data(
            Stock, "stores_qty", attr_name="stores_qty"
        )

        logger.debug(
            f"{self.mcc=}, " f"{self.report_range=}, " f"_get_stocks ==> {stocks}"
        )
        return stocks

    def _get_aggergated_data(self):
        """ВСе добытые МСС агреггируем тут"""
        pass

    def _get_country_stock(self) -> int:
        """Сток страны (магазины + склад) на последнюю отчетную дату."""
        try:
            return (
                Stock.objects.filter(mcc=self.mcc)
                .select_related()
                .order_by("-date")
                .first()
                .country_qty
            )

        except AttributeError as err:
            logger.error(f"Country stock QS returned empty. Error: {err}")
            return 0

    def _get_stores_stock(self) -> int:
        """Сток всех магазинов на последнюю отчетную дату."""
        try:
            return (
                Stock.objects.filter(mcc=self.mcc)
                .select_related()
                .order_by("-date")
                .first()
                .stores_qty
            )
        except AttributeError as err:
            logger.error(f"Stores stock QS returned empty. Error: {err}")
            return 0

    def _get_rotation(self) -> int:
        week_ago = str(datetime.date.today() - datetime.timedelta(weeks=1))
        try:
            last_week_sales = (
                Sales.objects.filter(
                    mcc=self.mcc, date__range=[week_ago, str(datetime.date.today())]
                )
                .select_related("mcc")
                .aggregate(Sum("quantity"))
            )["quantity__sum"] or 0
            return round(self._get_country_stock() / last_week_sales)
        except (AttributeError, ZeroDivisionError):
            return 0

    def _get_sellthrough(self) -> float:
        ordered = (
            OrderItem.objects.filter(mcc=self.mcc)
            .select_related("mcc")
            .aggregate(Sum("purchased_qty"))
        )["purchased_qty__sum"]
        total_sales = (
            Sales.objects.filter(mcc=self.mcc)
            .select_related("mcc")
            .aggregate(Sum("quantity"))
        )["quantity__sum"]
        return round(ordered / total_sales, 2)

    def _get_pending_delivery(self) -> float:
        pending = (
            OrderItem.objects.filter(mcc=self.mcc)
            .select_related("mcc")
            .aggregate(Sum("final_qty"))
        )["final_qty__sum"]
        return pending

    def _get_purchased_qty(self) -> int:
        purchased_sum = (
            OrderItem.objects.filter(mcc=self.mcc)
            .select_related("mcc")
            .aggregate(Sum("purchased_qty"))
        )["purchased_qty__sum"]
        logger.debug(f"Calculating purchased_sum ==> {purchased_sum} ")
        return purchased_sum

    def generate(
        self,
    ) -> dict[str, str | list[int] | set[int] | float | list[datetime.date] | array]:
        """Генерирует контекст для вывода на странице отчета."""
        return {
            "country_stock": self._get_country_stock(),
            "stores_stock": self._get_stores_stock(),
            "rotation": self._get_rotation(),
            "sellthrough": self._get_sellthrough(),
            "pending_delivery": self._get_pending_delivery(),
            "purchased": self._get_purchased_qty(),
            "days": self._set_weeks_starting_dates(),
            "weeks": self._set_weeks_numbers(),
            "actual_sales": self._get_actual_sales(),
            "planned_sales": self._get_planned_sales(),
            "mirror_mcc_sales": self._get_mirror_mcc_sales(),
            "stocks": self._get_weekly_stocks(),
        }


# report = MccReport("000/0012/1231")
# print(report.generate())
