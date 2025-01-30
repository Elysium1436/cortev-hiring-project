import django_filters
from .models import CornYieldModel


class CornYieldFilter(django_filters.FilterSet):

    year_after = django_filters.DateFilter(field_name="year", lookup_expr="gte")
    year_before = django_filters.DateFilter(field_name="year", lookup_expr="lte")
    yield_after = django_filters.DateFilter(field_name="corn_yield", lookup_expr="gte")
    yield_before = django_filters.DateFilter(field_name="corn_yield", lookup_expr="lte")

    class Meta:
        model = CornYieldModel
        fields = ["year_after", "year_before", "yield_after", "yield_before"]
