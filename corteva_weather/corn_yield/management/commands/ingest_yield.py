from django.core.management.base import BaseCommand
from corteva_weather.corn_yield.services import (
    ingest_yield_data_from_local_file,
)
import os


class Command(BaseCommand):
    help = "Ingests weather data"

    def add_arguments(self, parser):
        parser.add_argument(
            "folder_path", type=str, help="The path to the station folder"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["folder_path"]

        if not os.path.isfile(file_path):
            self.stderr.write(
                self.style.ERROR(f"The path '{file_path}' is not a valid folder.")
            )
            return
        ingest_yield_data_from_local_file(file_path)
