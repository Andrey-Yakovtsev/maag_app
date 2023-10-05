from django.db import models

from maag_app.products.models import Product, ReportEntity


class Stock(ReportEntity):
    mcc: Product = models.ForeignKey(
        Product, related_name="stocks", on_delete=models.CASCADE
    )
    stores_qty: int = models.IntegerField(default=0)
    country_qty: int = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.mcc.mcc} - {self.country_qty}"
