# Generated by Django 4.2.4 on 2023-09-06 11:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("domain", "0002_product_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="carry_over",
            field=models.BooleanField(default=False),
        ),
    ]
