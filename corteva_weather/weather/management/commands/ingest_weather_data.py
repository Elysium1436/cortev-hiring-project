from django.core.management.base import BaseCommand
from corteva_weather.weather.services import ingest_station_file_from_local_files
import os
import logging


class Command(BaseCommand):
    help = "Ingests weather data"

    def add_arguments(self, parser):
        parser.add_argument(
            "folder_path", type=str, help="The path to the station folder"
        )

    def handle(self, *args, **kwargs):
        folder_path = kwargs["folder_path"]

        if not os.path.isdir(folder_path):
            self.stderr.write(
                self.style.ERROR(f"The path '{folder_path}' is not a valid folder.")
            )
            return
        ingest_station_file_from_local_files(folder_path)
