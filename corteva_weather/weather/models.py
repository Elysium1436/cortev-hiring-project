from django.db import models

# Create your models here.

class WeatherStation(models.Model):
    station_id = models.CharField(max_length=30, unique=True)
    station_name = models.CharField(max_length=100, null=True)

class WeatherRecord(models.Model):
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name='weather_records')
    date = models.DateField()
    max_temperature = models.FloatField(null=True)
    min_temperature = models.FloatField(null=True)
    precipitation = models.FloatField(null=True)


class WeatherStatistics(models.Model):
    station = models.ForeignKey(WeatherStation, on_delete=models.CASCADE, related_name='weather_statistics')
    avg_max_temp = models.FloatField(null=False)
    avg_min_temp = models.FloatField(null=False)
    avg_precipitation = models.FloatField(null=False)
    