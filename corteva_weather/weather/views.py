from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter
from .models import WeatherStation, WeatherRecord, WeatherStatistics
from .serializers import WeatherStationSerializer, WeatherRecordSerializer, WeatherStatisticsSerializer
from  django_filters.rest_framework import DjangoFilterBackend
# Create your views here.


class WeatherStationViewSet(ReadOnlyModelViewSet):
    queryset = WeatherStation.objects.order_by("station_id", "station_name").all()
    serializer_class = WeatherStationSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["station"]

class WeatherRecordsViewSet(ReadOnlyModelViewSet):
    queryset = WeatherRecord.objects.order_by("station", "date").select_related("weather_station").all()
    # Make it so that it shows the id and name of the station
    serializer_class = WeatherRecordSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]

class WeatherStatisticsViewSet(ReadOnlyModelViewSet):
    queryset = WeatherStatistics.objects.order_by("station").all()
    serializer_class = WeatherStatisticsSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["station"]