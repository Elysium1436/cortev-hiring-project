from rest_framework import serializers
from .models import WeatherStation, WeatherRecord, WeatherStatistics




class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        

class WeatherRecordSerializer(serializers.ModelSerializer):
    station_id = serializers.CharField(source="weather_station.station_id")
    class Meta:
        model = WeatherRecord
        

class WeatherStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStatistics
        