import pytest
from django.db.models.functions import ExtractYear
from django.db.models import Avg, Sum, F
from ..models import WeatherStation, WeatherRecord, WeatherStatistic
from ..adapters.repositories import (
    DjangoWeatherStationRepository,
    DjangoWeatherStatisticRepository,
)
from ..adapters.unitofwork import DjangoStationUnitOfWork
from ..services import deserialize_station_data_native_python, ingest_station_data
import datetime
from typing import Callable


@pytest.mark.django_db
def test_uow_commit():

    with DjangoStationUnitOfWork(
        station_repository=DjangoWeatherStationRepository()
    ) as uow:
        WeatherStation.objects.create(station_name="test123")

    assert len(WeatherStation.objects.all()) == 1


@pytest.mark.django_db
def test_uow_rollback():
    try:
        with DjangoStationUnitOfWork(
            station_repository=DjangoWeatherStationRepository()
        ) as uow:
            WeatherStation.objects.create(station_name="test123")
            raise Exception
    except Exception as e:
        ...

    assert len(WeatherStation.objects.all()) == 0


@pytest.mark.django_db
def test_uow_accesses_repositories():
    class FakeRepo:
        def __init__(self):
            return

    repo = FakeRepo()

    with DjangoStationUnitOfWork(station_repository=repo) as uow:
        assert id(repo) == id(uow.station_repository)


@pytest.mark.django_db
def test_add_weather():
    repo = DjangoWeatherStationRepository()
    station = WeatherStation(station_name="test_station")
    repo.add_station(station)
    s = WeatherStation.objects.first()
    assert station == s


@pytest.mark.django_db
def test_add_records():
    repo = DjangoWeatherStationRepository()
    station = WeatherStation(station_name="test123")
    repo.add_station(station)
    record_1 = WeatherRecord(station=station, date=datetime.date(1989, 4, 20))
    record_2 = WeatherRecord(station=station, date=datetime.date(2014, 5, 20))
    repo.add_records([record_1, record_2])

    assert len(WeatherRecord.objects.all()) == 2


@pytest.mark.django_db
def test_add_update_records():
    repo = DjangoWeatherStationRepository()
    station = WeatherStation(station_name="test123")
    repo.add_station(station)

    record_1 = WeatherRecord(station=station, date=datetime.date(1989, 4, 20))
    record_2 = WeatherRecord(station=station, date=datetime.date(2014, 5, 20))
    repo.add_records([record_1, record_2])

    update_record = WeatherRecord(
        station=station, date=datetime.date(1989, 4, 20), precipitation=123
    )

    repo.add_records([update_record])

    assert (
        WeatherRecord.objects.filter(date=datetime.date(1989, 4, 20))
        .first()
        .precipitation
        is not None
    )


@pytest.fixture
def station_repository():
    return DjangoWeatherStationRepository()


@pytest.fixture
def create_station_with_two_10_records(
    station_repository,
) -> tuple[Callable[[str], WeatherStation], DjangoWeatherStationRepository]:
    def callback(station_name: str) -> WeatherStation:
        repo = DjangoWeatherStationRepository()
        station, _ = repo.get_or_create_station(station_name)
        repo.get_or_create_record(
            station,
            date=datetime.date(1989, 1, 1),
            max_temperature=10,
            min_temperature=10,
            precipitation=10,
        )
        repo.get_or_create_record(
            station,
            date=datetime.date(1990, 1, 1),
            max_temperature=10,
            min_temperature=10,
            precipitation=10,
        )
        return station

    return callback, station_repository


@pytest.mark.django_db
def test_weather_statistic(create_station_with_two_10_records):
    callback, repo = create_station_with_two_10_records
    station = callback("test123")
    stat_repo = DjangoWeatherStatisticRepository()
    statistics = stat_repo.create_or_update_station_statistics(station)
    assert len(statistics) == 2


@pytest.mark.django_db
def test_weather_statistic_year_truncated(create_station_with_two_10_records):
    callback, repo = create_station_with_two_10_records
    station1 = callback("test123")
    station2 = callback("test456")
    stat_repo = DjangoWeatherStatisticRepository()
    statistics = stat_repo.create_or_update_all_station_statistics()
    assert len(statistics) == 4
