import random
from datetime import datetime, timedelta
from typing import Any

from django.core.management import BaseCommand

from maag_app.orders.models import Order
from maag_app.products import models as prod_models
from maag_app.products.models import Product


class Command(BaseCommand):
    help = "Initial database filling with most nesseccary data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        Product.objects.all().delete()
        Order.objects.all().delete()
        prod_models.Season.objects.all().delete()
        prod_models.Subfamily.objects.all().delete()
        prod_models.Family.objects.all().delete()
        prod_models.Group.objects.all().delete()
        prod_models.Section.objects.all().delete()

        print("Success!!! All DB entries DELETED")
