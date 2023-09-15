"""
Построение отчета по МСС
"""
import datetime

import django_tables2 as tables

from maag_app.domain.models import Product
from maag_app.sales.models import Sales

four_weeks_bckwd = datetime.date.today() - datetime.timedelta(weeks=4)


class MccTable(tables.Table):
    class Meta:
        model = Product
        template_name = "django_tables2/bootstrap.html"
        fields = ("mcc",)


class MccReport:
    """
    Построение отчета по каждому отдельному МСС на указанную (или дефолтную дату)
    """

    def __init__(self, mcc: str, date: datetime.date = four_weeks_bckwd):
        self.mcc = self._get_mcc(mcc)
        self.date: datetime.date = date
        self.week_number: int = self.date.isocalendar()[1]
        self.actual_sales = self._get_actual_sales()
        self.mirror_mcc_sales = None
        self.planned_sales = None

    @staticmethod
    def _get_mcc(mcc) -> Product:
        return Product.objects.filter(mcc=mcc).first()

    def _get_actual_sales(self) -> list[int]:
        """Cписок продаж за 12 недель (4 назад + 8 хардкодом)."""
        # FIXME может просить с фронта диапазон недель вместо 8 хардкода?
        return (
            Sales.objects.filter(
                mcc=self.mcc,
                date__range=[
                    self.date,
                    str(datetime.date.today() + datetime.timedelta(weeks=8)),
                ],
            )
            .select_related("mcc")
            .values_list("quantity", flat=True)
        )

    def _get_mirror_mcc_sales(self) -> list[int]:
        if self.mcc.mirror_mcc:
            return (
                Sales.objects.filter(
                    mcc=self.mcc.mirror_mcc,
                    date__range=[
                        self.date,
                        str(datetime.date.today() + datetime.timedelta(weeks=8)),
                    ],
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
