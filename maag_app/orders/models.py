from django.db import models

from maag_app.products.models import Product


class Order(models.Model):
    """Заказ с номером и ключевыми датами."""

    number = models.CharField(max_length=56, blank=False)
    order_date = models.DateField(blank=False)
    handover_date = models.DateField(blank=False)
    expected_wh_date = models.DateField(blank=False)

    def __str__(self):
        return f"{self.number} - {self.order_date}"


class OrderItem(models.Model):
    """Единичная позиция заказа."""

    mcc = models.ForeignKey(
        Product, related_name="orderitems", on_delete=models.CASCADE
    )
    purchased_qty = models.IntegerField(default=0)
    received_qty = models.IntegerField(default=0)
    final_qty = models.IntegerField(default=0)
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)

    def __str__(self):
        return f"Mcc - {self.mcc.mcc}. Order {self.order.number}"
