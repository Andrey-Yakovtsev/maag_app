import random
from datetime import datetime, timedelta
from typing import Any

from django.core.management import BaseCommand

from maag_app.orders.models import Order, OrderItem
from maag_app.products import models
from maag_app.sales.models import Sales
from maag_app.stocks.models import Stock


def add_mirror_to_mcc(base, mirror):
    base_mcc = models.Product.objects.get(mcc=base)
    mirror_mcc = models.Product.objects.get(mcc=mirror)
    base_mcc.mirror_mcc = mirror_mcc
    base_mcc.save(update_fields=["mirror_mcc"])


class Command(BaseCommand):
    help = "Initial database filling with most nesseccary data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        items = ["Subfamily 1", "Subfamily 2", "Subfamily 3", "Subfamily 4"]
        for i in items:
            models.Subfamily.objects.update_or_create(name=i)

        items = ["Family 1", "Family 2", "Family 3", "Family 4"]
        for i in items:
            models.Family.objects.update_or_create(name=i)

        items = ["Group 1", "Group 2", "Group 3", "Group 4"]
        for i in items:
            models.Group.objects.update_or_create(name=i)

        items = ["Section 1", "Section 2", "Section 3", "Section 4"]
        for i in items:
            models.Section.objects.update_or_create(name=i)

        items = ["Season 1", "Season 2", "Season 3", "Season 4"]
        for i in items:
            models.Season.objects.update_or_create(name=i)

        mccs = [
            "1111/111/111",
            "2221/222/222",
            "3333/333/333",
            "4444/444/444",
            "5555/555/555",
            "6666/555/555",
            "7777/555/555",
            "8888/555/555",
            "9999/555/555",
            "5555/453/333",
            "1111/000/000",
            "2221/000/000",
            "3333/000/000",
        ]

        counter = 1
        for mcc in mccs:
            models.Product.objects.update_or_create(
                mcc=mcc,
                defaults={
                    "subfamily": models.Subfamily.objects.get(id=counter),
                    "family": models.Family.objects.get(id=counter),
                    "season": models.Season.objects.get(id=counter),
                    "group": models.Group.objects.get(id=counter),
                    "section": models.Section.objects.get(id=counter),
                },
            )
            if counter < 4:
                counter += 1
            else:
                counter = 1

        for mcc in mccs:
            datetime_str = "03/01/2023"
            years_period = 1
            # datetime_str = "03/01/2022"  # На случай, если за 2 года надо создать
            # years_period = 2

            start_date = datetime.strptime(datetime_str, "%d/%m/%Y")
            report_date = start_date
            prdct = models.Product.objects.get(mcc=mcc)
            for i in range(52 * years_period):
                qty = random.randint(1, 50)
                stores_qty = random.randint(200, 300)
                Sales.objects.update_or_create(
                    mcc=prdct,
                    date=report_date,
                    defaults={
                        "quantity": qty,
                        "amount": qty * 1099,
                        "planned": random.randint(1, 50),
                    },
                )
                Stock.objects.update_or_create(
                    mcc=prdct,
                    date=report_date,
                    defaults={"stores_qty": stores_qty, "country_qty": stores_qty * 3},
                )
                report_date += timedelta(weeks=1)

            order, _ = Order.objects.update_or_create(
                number=f"PO-nsa-{random.randint(1, 898)}",
                order_date=report_date + timedelta(weeks=1),
                handover_date=report_date + timedelta(weeks=3),
                expected_wh_date=report_date + timedelta(weeks=mccs.index(mcc)),
            )
            OrderItem.objects.update_or_create(
                mcc=prdct,
                order=order,
                defaults={
                    "purchased_qty": random.randint(2000, 3000),
                    "received_qty": random.randint(1000, 2000),
                    "final_qty": random.randint(500, 1000),
                },
            )
        add_mirror_to_mcc("1111/111/111", "1111/000/000")
        add_mirror_to_mcc("2221/222/222", "2221/000/000")
        add_mirror_to_mcc("3333/333/333", "3333/000/000")

        print("Success!!! All DB entries created")
