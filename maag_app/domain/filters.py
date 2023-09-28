import django_filters

from maag_app.domain.models import Product


class MccFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = (
            'subfamily', 'family', 'group', 'section', 'season',
        )
