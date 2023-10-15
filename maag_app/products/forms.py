import logging
from typing import Any

from django import forms

from maag_app.products.models import Product
from maag_app.sales.models import Sales

logger = logging.getLogger()


class PlannedForm(forms.ModelForm):
    date = forms.DateField(input_formats=["%d/%m/%Y"])
    mcc = forms.CharField(max_length=12)

    class Meta:
        model = Sales
        fields = ["planned", "mcc", "date"]

    def clean(self) -> dict[str, Any] | None:
        cleaned_data = super().clean()
        try:
            mcc = Product.objects.get(mcc=cleaned_data.get("mcc"))
        except Product.DoesNotExist as err:
            logger.error(f"No Mcc entry found for {cleaned_data.get('mcc')}")
            mcc = None
        cleaned_data["mcc"] = mcc
        return cleaned_data
