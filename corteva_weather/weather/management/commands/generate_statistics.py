from django.core.management.base import BaseCommand
from corteva_weather.weather.adapters.repositories import (
    DjangoWeatherStatisticRepository,
)
from corteva_weather.weather.adapters.unitofwork import DjangoStatisticUnitOfWork
import os
import logging


class Command(BaseCommand):
    help = "Ingests weather data"

    def handle(self, *args, **kwargs):
        repo = DjangoWeatherStatisticRepository()
        uow = DjangoStatisticUnitOfWork(statistic_repository=repo)
        with uow:
            uow.statistic_repository.create_or_update_all_station_statistics()
