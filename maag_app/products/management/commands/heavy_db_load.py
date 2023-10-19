import random
from datetime import datetime, timedelta
from typing import Any

from django.core.management import BaseCommand

from maag_app.orders.models import Order, OrderItem
from maag_app.products import models
from maag_app.products.models import Product
from maag_app.sales.models import Sales
from maag_app.stocks.models import Stock


def add_mirror_to_mcc(base: Product, mirror: Product):
    try:
        if not base.mirror_mcc:
            base.mirror_mcc = mirror
            base.save(update_fields=["mirror_mcc"])
    except Exception:
        pass


class Command(BaseCommand):
    help = "Initial database filling with most nesseccary data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        counter = 10

        items = [f"Subfamily {i}" for i in range(counter + 1)]
        for i in items:
            models.Subfamily.objects.update_or_create(name=i)

        items = [f"Family {i}" for i in range(counter + 1)]
        for i in items:
            models.Family.objects.update_or_create(name=i)

        items = [f"Group {i}" for i in range(counter + 1)]
        for i in items:
            models.Group.objects.update_or_create(name=i)

        items = [f"Section {i}" for i in range(counter + 1)]
        for i in items:
            models.Section.objects.update_or_create(name=i)

        items = [f"Season {i}" for i in range(counter + 1)]
        for i in items:
            models.Season.objects.update_or_create(name=i)

        mccs_list = []
        for i in range(2000):
            r = random.randint(1, 9)
            a = random.randint(1, 9)
            n = random.randint(1, 9)
            d = random.randint(1, 9)
            o = random.randint(1, 9)
            m = random.randint(1, 9)
            i = random.randint(1, 9)
            f = random.randint(1, 9)
            g = random.randint(1, 9)
            v = random.randint(1, 9)
            mccs_list.append(
                Product(
                    mcc=f"{r}{a}{n}{d}/{o}{m}{f}/{i}{g}{v}",
                    subfamily=models.Subfamily.objects.get(id=r),
                    family=models.Family.objects.get(id=r),
                    group=models.Group.objects.get(id=r),
                    section=models.Section.objects.get(id=r),
                    season=models.Season.objects.get(id=r),
                )
            )

        Product.objects.bulk_create(mccs_list)
        print("A lof of Products created for {} ")

        orders_objs = []
        mccs = Product.objects.all()
        for mcc in mccs:
            datetime_str = "03/01/2023"
            years_period = 1
            # datetime_str = "03/01/2022"  # На случай, если за 2 года надо создать
            # years_period = 2

            start_date = datetime.strptime(datetime_str, "%d/%m/%Y")
            report_date = start_date
            prdct = models.Product.objects.get(mcc=mcc)
            sales_obj = []
            stocks_obj = []
            for i in range(52 * years_period):
                qty = random.randint(1, 50)
                stores_qty = random.randint(200, 300)
                sales_obj.append(
                    Sales(mcc=prdct, date=report_date, quantity=qty, amount=qty * 1099)
                )
                stocks_obj.append(
                    Stock(
                        mcc=prdct,
                        date=report_date,
                        stores_qty=stores_qty,
                        country_qty=stores_qty * 3,
                    )
                )
                report_date += timedelta(weeks=1)
            Sales.objects.bulk_create(sales_obj)
            print(f"Sales created for {mcc=} ")
            Stock.objects.bulk_create(stocks_obj)
            print(f"Stocks created for {mcc=} ")

            orders_objs.append(
                Order(
                    number=f"PO-nsa-{random.randint(1, 898)}",
                    order_date=report_date + timedelta(weeks=1),
                    handover_date=report_date + timedelta(weeks=3),
                    expected_wh_date=report_date
                    + timedelta(weeks=random.randint(1, 12)),
                )
            )
        Order.objects.bulk_create(orders_objs)
        print("Orders created")

        order_items_obj = []
        for order in Order.objects.all():
            order_items_obj.append(
                OrderItem(
                    mcc=Product.objects.get(id=random.randint(1, 1999)),
                    order=order,
                    purchased_qty=random.randint(2000, 3000),
                    received_qty=random.randint(1000, 2000),
                    final_qty=random.randint(500, 1000),
                )
            )
        OrderItem.objects.bulk_create(order_items_obj)
        print("OrderItems created")

        for i in range(1500):
            prd1 = Product.objects.get(id=random.randint(1, 1999))
            prd2 = Product.objects.get(id=random.randint(1, 1999))
            add_mirror_to_mcc(prd1, prd2)

        print("Success!!! All DB entries created")
