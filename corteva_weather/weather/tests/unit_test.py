from ..models import WeatherStation, WeatherRecord
from ..services import deserialize_station_data_native_python, ingest_station_data

import datetime


class FakeBuffer:

    def __init__(self, lines: list[str] = None):
        self.lines = lines

    def readlines(self):
        return self.lines or [
            "19850101	  -22	 -128	   94",
            "19850103	 -106	 -244	    0",
        ]


class FakeStationUOW:
    def __init__(self, station_repository):
        self.station_repository = station_repository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return


class FakeStationRepository:
    def __init__(self):
        self.stations: set[WeatherStation] = set()
        self.records = []
        return

    def add_station(self, station: WeatherStation):
        self.stations.add(station)

    def bulk_create_records(self, records):
        self.records.extend(records)

    def get_records(self, station):
        return self.records

    def get_station(self, station_name):
        return next(
            (
                station
                for station in self.stations
                if station.station_name == station_name
            ),
            None,
        )

    def get_or_create_station(self, station_name) -> tuple[WeatherStation, True]:
        station = self.get_station(station_name)

        return (
            (station, False)
            if station
            else (self.add_station(WeatherStation(station_name=station_name)), True)
        )

    def add_records(
        self, records: list[WeatherRecord], station: WeatherStation | None = None
    ):
        self.records.extend(records)


def fake_deserialize_weather_strategy(station, _):
    return [
        WeatherRecord(
            station=station,
            date=datetime.date(1111, 11, 22),
            max_temperature=1.0,
            min_temperature=1.0,
            precipitation=1.0,
        )
    ]


def test_deserialize_weather():
    station = WeatherStation(station_name="test123")
    f = FakeBuffer(["11111111\t22\t333\t44"])
    records = deserialize_station_data_native_python(station, f)

    record = records[0]

    assert record
    assert record.date.year == 1111
    assert record.max_temperature == 2.2
    assert record.min_temperature == 33.3
    assert record.precipitation == 4.4
    assert record.station == station


def test_deserialize_weather_null():
    station = WeatherStation(station_name="test123")
    f = FakeBuffer(["11111111\t-9999\t-9999\t-9999"])
    records = deserialize_station_data_native_python(station, f)

    record = records[0]

    assert record
    assert record.max_temperature == None
    assert record.min_temperature == None
    assert record.precipitation == None
    assert record.station == station


def test_ingest_data():
    repo = FakeStationRepository()

    with FakeStationUOW(station_repository=repo) as uow:
        ingest_station_data(
            uow,
            "test_123",
            FakeBuffer(),
            fake_deserialize_weather_strategy,
        )

    assert repo.get_station("test_123").station_name == "test_123"
    assert len(repo.get_records("bogus")) != 0
