import datetime

from django.db import models


class ReportEntity(models.Model):
    date: datetime.date = models.DateField(blank=False)
    week: int = models.IntegerField(null=True, blank=True)
    year: int = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    def _add_week_number(self):
        self.week = self.date.isocalendar()[1]

    def _add_year(self):
        self.year = self.date.year

    def save(self):
        self._add_week_number()
        self._add_year()
        super().save()


class ProductEnumFilter(models.Model):
    name = models.CharField(blank=False, unique=True)

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
    mcc = models.CharField(blank=False, unique=True)
    description = models.CharField(max_length=512, default="")
    subfamily = models.ForeignKey(
        Subfamily, related_name="products", on_delete=models.CASCADE
    )
    family = models.ForeignKey(
        Family, related_name="products", on_delete=models.CASCADE
    )
    group = models.ForeignKey(Group, related_name="products", on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, related_name="products", on_delete=models.CASCADE
    )
    season = models.ForeignKey(
        Season, related_name="products", on_delete=models.CASCADE
    )
    carry_over = models.BooleanField(default=False)
    mirror_mcc = models.OneToOneField(
        "Product", null=True, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.mcc
