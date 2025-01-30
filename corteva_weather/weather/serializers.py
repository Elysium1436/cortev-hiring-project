from rest_framework import serializers
from .models import WeatherStation, WeatherRecord, WeatherStatistic
import logging


class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        fields = "__all__"


class WeatherRecordSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source="station.station_name", read_only=True)

    class Meta:
        model = WeatherRecord
        fields = "__all__"


class WeatherStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStatistic
        fields = "__all__"


class WeatherStationFileSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        file_name = value.name
        logging.info(f"Uploaded file {file_name}")
        return value


class WeatherStationRecordSerializer(serializers.Serializer):
    """Will only be used for deserializing both the station and records"""

    station = WeatherStationSerializer()
    records = WeatherRecordSerializer(many=True)
