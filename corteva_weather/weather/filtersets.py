import django_filters
from .models import WeatherRecord, WeatherStatistic


class WeatherRecordFilter(django_filters.FilterSet):
    station_name = django_filters.CharFilter(
        field_name="station__station_name", lookup_expr="iexact"
    )
    station_id = django_filters.NumberFilter(field_name="station", lookup_expr="iexact")

    date_after = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_before = django_filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = WeatherRecord
        fields = ["station_name", "station_id", "date_after", "date_before"]


class WeatherStatisticFilter(django_filters.FilterSet):
    station_name = django_filters.CharFilter(
        "station__station_name", lookup_expr="iexact"
    )

    station_id = django_filters.NumberFilter(field_name="station", lookup_expr="iexact")

    year = django_filters.NumberFilter(field_name="year", lookup_expr="iexact")

    class Meta:
        model = WeatherStatistic
        fields = ["station_name", "station_id", "year"]
