from .repositories import (
    WeatherStationRepository,
    DjangoWeatherStationRepository,
    DjangoWeatherStatisticRepository,
)
from corteva_weather.adapters.unitofwork import UnitOfWork, DjangoUnitOfWork


class StationUnitOfWork(UnitOfWork):
    # Prototype
    def __init__(self, station_repository: WeatherStationRepository):
        self.station_repository: WeatherStationRepository


class DjangoStationUnitOfWork(DjangoUnitOfWork):
    def __init__(self, station_repository: DjangoWeatherStationRepository):
        self.station_repository = station_repository
        super().__init__()


class DjangoStatisticUnitOfWork(DjangoUnitOfWork):
    def __init__(self, statistic_repository: DjangoWeatherStatisticRepository):
        self.statistic_repository = statistic_repository
        super().__init__()
