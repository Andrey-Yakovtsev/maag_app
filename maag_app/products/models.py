import datetime
from typing import Self

from django.db import models


class ReportEntity(models.Model):
    date: datetime.date = models.DateField(blank=False)
    week: int = models.IntegerField(null=True, blank=True)
    year: int = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def _add_week_number(self) -> None:
        self.week = self.date.isocalendar()[1]

    def _add_year(self) -> None:
        self.year = self.date.year

    def save(self, *args, **kwargs) -> None:
        self._add_week_number()
        self._add_year()
        super().save(*args, **kwargs)


class ProductEnumFilter(models.Model):
    name: str = models.CharField(blank=False, unique=True)

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


class Product(models.Model):
    mcc: str = models.CharField(blank=False, unique=True)
    description: str = models.CharField(max_length=512, default="")
    subfamily: Subfamily = models.ForeignKey(
        Subfamily, related_name="products", on_delete=models.CASCADE
    )
    family: Family = models.ForeignKey(
        Family, related_name="products", on_delete=models.CASCADE
    )
    group: Group = models.ForeignKey(
        Group, related_name="products", on_delete=models.CASCADE
    )
    section: Section = models.ForeignKey(
        Section, related_name="products", on_delete=models.CASCADE
    )
    season: Season = models.ForeignKey(
        Season, related_name="products", on_delete=models.CASCADE
    )
    carry_over: bool = models.BooleanField(default=False)
    mirror_mcc: Self = models.OneToOneField(
        "Product", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.mcc
