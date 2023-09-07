import datetime

from django.db import models


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


# def set_deleted_name(model):
#     return model.objects.get_or_create(name="deleted")[0]


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

    @property
    def country_stock(self) -> int:
        from maag_app.stocks.models import Stock

        return (
            Stock.objects.select_related("mcc")
            .filter(mcc=self, date=str(datetime.date.today()))
            .first()
            .country_qty
        )

    @property
    def stores_stock(self) -> int:
        from maag_app.stocks.models import Stock

        return (
            Stock.objects.select_related("mcc")
            .filter(mcc=self, date=str(datetime.date.today()))
            .first()
            .stores_qty
        )

    @property
    def rotation(self) -> int:
        from maag_app.sales.models import Sales

        week_ago = str(datetime.date.today() - datetime.timedelta(weeks=1))
        last_week_sales = (
            Sales.objects.select_related("mcc")
            .filter(mcc=self, date__range=[week_ago, str(datetime.date.today())])
            .values_list("quantity", flat=True)
        )
        return round(self.country_stock / sum(last_week_sales))

    @property
    def sellthrough(self) -> float:
        from maag_app.orders.models import OrderItem
        from maag_app.sales.models import Sales

        ordered = (
            OrderItem.objects.select_related("mcc")
            .filter(mcc=self)
            .values_list("purchased_qty", flat=True)
        )
        total_sales = (
            Sales.objects.select_related("mcc")
            .filter(mcc=self)
            .values_list("quantity", flat=True)
        )
        return round(sum(ordered) / sum(total_sales), 2)

    @property
    def pending_delivery(self) -> float:
        from maag_app.orders.models import OrderItem

        pending = (
            OrderItem.objects.select_related("mcc")
            .filter(mcc=self)
            .values_list("final_qty", flat=True)
        )
        return sum(pending)

    @property
    def continuity(self) -> str:
        return "Yes" if self.carry_over else "No"

    def __str__(self):
        return self.mcc
