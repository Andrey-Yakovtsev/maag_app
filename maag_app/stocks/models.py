from django.db import models

from maag_app.domain.models import Product


class Stock(models.Model):
    date = models.DateField(blank=False)
    mcc = models.ForeignKey(Product, related_name="stocks", on_delete=models.CASCADE)
    stores_qty = models.IntegerField(default=0)
    country_qty = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.mcc.mcc} - {self.country_qty}"
