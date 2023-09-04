from dataclasses import dataclass

from django.db import models


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


def set_deleted_name(model):
    return model.objects.get_or_create(name="deleted")[0]


class Product(models.Model):
    mcc = models.CharField(blank=False, unique=True)
    description = models.CharField(max_length=512, default='')
    subfamily = models.ForeignKey(Subfamily, related_name='products', on_delete=models.CASCADE)
    family = models.ForeignKey(Family, related_name='products', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='products', on_delete=models.CASCADE)
    section = models.ForeignKey(Section,related_name='products', on_delete=models.CASCADE)
    season = models.ForeignKey(Season, related_name='products', on_delete=models.CASCADE)
