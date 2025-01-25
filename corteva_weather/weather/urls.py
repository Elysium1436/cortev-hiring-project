from rest_framework.routers import DefaultRouter
from django.urls import include
from .views import WeatherRecordsViewSet, WeatherStationViewSet, WeatherStatisticsViewSet


router = DefaultRouter()

router.register(r"weather-station", WeatherStationViewSet, basename="weather-station")
router.register(r"weather-record", WeatherRecordsViewSet, basename="weather-record")
router.register(r"weather-statistics", WeatherStatisticsViewSet, basename="weather-statistics")


urlpatterns = router.urls