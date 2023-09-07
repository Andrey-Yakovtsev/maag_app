from django.db import models

from maag_app.domain.models import Product


class Sales(models.Model):
    date = models.DateField(blank=False)
    mcc = models.ForeignKey(Product, related_name="sales", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)

    @property
    def avg_unit_price(self):
        return self.amount / self.quantity

    def __str__(self):
        return f"{self.date} - {self.mcc.mcc} - {self.quantity}"
