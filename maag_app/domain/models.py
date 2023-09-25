import datetime

from django.db import models


class ReportEntity(models.Model):
    date: datetime.date = models.DateField(blank=False)
    week: int = models.IntegerField(null=True, blank=True)
    year: int = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def _add_week_number(self):
        self.week = self.date.isocalendar()[1]

    def _add_year(self):
        self.year = self.date.year

    def save(self):
        self._add_week_number()
        self._add_year()
        super().save()


class ProductEnumFilter(models.Model):
    name = models.CharField(blank=False, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Subfamily(ProductEnumFilter):
    ...


class Family(ProductEnumFilter):
    ...


class Group(ProductEnumFilter):
    ...


class Section(ProductEnumFilter):
    ...


class Season(ProductEnumFilter):
    ...


class Product(models.Model):
    mcc = models.CharField(blank=False, unique=True)
    description = models.CharField(max_length=512, default="")
    subfamily = models.ForeignKey(
        Subfamily, related_name="products", on_delete=models.CASCADE
    )
    family = models.ForeignKey(
        Family, related_name="products", on_delete=models.CASCADE
    )
    group = models.ForeignKey(Group, related_name="products", on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, related_name="products", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season, related_name="products", on_delete=models.CASCADE
    )
    carry_over = models.BooleanField(default=False)
    mirror_mcc = models.OneToOneField(
        "Product", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    @property
    def country_stock(self) -> int:
        from maag_app.stocks.models import Stock

        return (
            Stock.objects.filter(mcc=self)
            # .select_related("mcc")
            .select_related()
            .order_by("-date")
            .first()
            .country_qty
        )

    @property
    def stores_stock(self) -> int:
        from maag_app.stocks.models import Stock

        return (
            Stock.objects.filter(mcc=self)
            .select_related("mcc")
            .order_by("-date")
            .first()
            .stores_qty
        )

    @property
    def rotation(self) -> int:
        from maag_app.sales.models import Sales

        week_ago = str(datetime.date.today() - datetime.timedelta(weeks=1))
        try:
            last_week_sales = (
                Sales.objects.filter(
                    mcc=self, date__range=[week_ago, str(datetime.date.today())]
                )
                .select_related("mcc")
                .values_list("quantity", flat=True)
            )
            return round(self.country_stock / sum(last_week_sales))
        except (AttributeError, ZeroDivisionError):
            return 0

    @property
    def sellthrough(self) -> float:
        from maag_app.orders.models import OrderItem
        from maag_app.sales.models import Sales

        ordered = (
            OrderItem.objects.filter(mcc=self)
            .select_related("mcc")
            .values_list("purchased_qty", flat=True)
        )
        total_sales = (
            Sales.objects.filter(mcc=self)
            .select_related("mcc")
            .values_list("quantity", flat=True)
        )
        return round(sum(ordered) / sum(total_sales), 2)

    @property
    def pending_delivery(self) -> float:
        from maag_app.orders.models import OrderItem

        pending = (
            OrderItem.objects.filter(mcc=self)
            .select_related("mcc")
            .values_list("final_qty", flat=True)
        )
        return sum(pending)

    @property
    def purchased(self) -> int:
        from maag_app.orders.models import OrderItem

        purchased = (
            OrderItem.objects.filter(mcc=self)
            .select_related("mcc", "order")
            .values_list("purchased_qty", flat=True)
        )
        return sum(purchased)

    def __str__(self):
        return self.mcc
