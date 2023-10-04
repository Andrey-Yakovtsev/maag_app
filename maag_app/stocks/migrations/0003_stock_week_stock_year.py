# Generated by Django 4.2.4 on 2023-09-24 17:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stocks", "0002_rename_quantity_stock_country_qty_stock_stores_qty"),
    ]

    operations = [
        migrations.AddField(
            model_name="stock",
            name="week",
            field=models.IntegerField(blank=True, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name="stock",
            name="year",
            field=models.IntegerField(blank=True, max_length=4, null=True),
        ),
    ]