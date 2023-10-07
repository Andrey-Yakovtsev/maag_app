from django import forms

from maag_app.sales.models import Sales


class PlannedForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ["planned"]
