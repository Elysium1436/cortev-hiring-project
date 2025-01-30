from rest_framework.viewsets import ReadOnlyModelViewSet
from drf_spectacular.utils import extend_schema
from ..models import WeatherRecord
from ..serializers import (
    WeatherRecordSerializer,
)
from ..filtersets import WeatherRecordFilter
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(tags=["Weather Records"])
class WeatherRecordsViewSet(ReadOnlyModelViewSet):
    queryset = (
        WeatherRecord.objects.order_by("station", "date")
        .select_related("station")
        .all()
    )
    # Make it so that it shows the id and name of the station
    serializer_class = WeatherRecordSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WeatherRecordFilter
