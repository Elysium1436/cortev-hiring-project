import datetime
from .models import WeatherStation, WeatherRecord
from .adapters.repositories import (
    WeatherStationRepository,
    DjangoWeatherStationRepository,
)
from .adapters.unitofwork import StationUnitOfWork, DjangoStationUnitOfWork
from io import StringIO
from typing import Callable
from pathlib import Path
import logging
import glob


def deserialize_USC_line(line_str: str) -> tuple[datetime.date, float, float, float]:
    date, max_temp, min_temp, precipitation = line_str.strip().split()
    date = datetime.datetime.strptime(date, "%Y%m%d").date()
    max_temp = None if max_temp == "-9999" else float(max_temp) / 10
    min_temp = None if min_temp == "-9999" else float(min_temp) / 10
    precipitation = None if precipitation == "-9999" else float(precipitation) / 10
    return date, max_temp, min_temp, precipitation


def deserialize_station_data_native_python(
    station: WeatherStation, buffer: StringIO
) -> list[WeatherRecord]:
    records = []
    for line in buffer.readlines():
        if line.strip():
            date, max_temp, min_temp, precipitation = deserialize_USC_line(line)
            records.append(
                WeatherRecord(
                    station=station,
                    date=date,
                    max_temperature=max_temp,
                    min_temperature=min_temp,
                    precipitation=precipitation,
                )
            )
    return records


def ingest_station_data(
    uow: StationUnitOfWork,
    # Could get the station name from the buffer, but it will not always be the case.
    station_name: str,
    # Using a buffer allows us to easily implement data ingestion from simple file upload or streaming.
    buffer: StringIO,
    # Allows us to seamlessly change the deserializatin strategy to something potentially more efficient, like polars or duckdb.
    deserialization_strategy: Callable[[WeatherStation, StringIO], list[WeatherRecord]],
) -> tuple[WeatherStation, list[WeatherRecord]]:
    station, _ = uow.station_repository.get_or_create_station(station_name=station_name)
    records = deserialization_strategy(station, buffer)
    weather_records = uow.station_repository.add_records(records)
    return station, weather_records


def ingest_station_file_from_local_files(folder_path):
    paths = [Path(file_path) for file_path in glob.glob(folder_path + "/*.txt")]

    repo = DjangoWeatherStationRepository()
    uow = DjangoStationUnitOfWork(station_repository=repo)
    # If any data ingestion file goes wrong, rollback everything.

    total_records_before = repo.record_count()
    logging.info("Started ingesting station data")

    with uow:
        counter = 1
        for station_name, path in ((path.stem, path) for path in paths):
            logging.info(f"Ingesting file {station_name} {counter}/{len(paths)}")

            with open(path, "r") as f:
                ingest_station_data(
                    uow, station_name, f, deserialize_station_data_native_python
                )
            counter += 1

    total_records_after = repo.record_count()
    logging.info("Finished ingesting station data.")
    logging.info(
        f"Number of records created: {total_records_after-total_records_before}."
    )
