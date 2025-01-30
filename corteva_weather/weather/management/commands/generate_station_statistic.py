from django.core.management.base import BaseCommand
from corteva_weather.weather.adapters.repositories import (
    DjangoWeatherStatisticRepository,
    DjangoWeatherStationRepository,
)
from corteva_weather.weather.adapters.unitofwork import DjangoStatisticUnitOfWork
import os
import logging


class Command(BaseCommand):
    help = "Ingests weather data"

    def add_arguments(self, parser):
        parser.add_argument("station_name", type=str, help="The station name")

    def handle(self, *args, **kwargs):
        station_name = kwargs["station_name"]
        statistics_repo = DjangoWeatherStatisticRepository()
        station_repo = DjangoWeatherStationRepository()

        uow = DjangoStatisticUnitOfWork(statistic_repository=statistics_repo)
        with uow:
            station = station_repo.get_station_by_name(station_name)
            if station is None:
                print("Station name not found")
                return
            statistic, _ = uow.statistic_repository.create_or_update_station_statistic(
                station
            )
