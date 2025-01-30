from ..models import WeatherStation, WeatherRecord, WeatherStatistic
from django.db.models import Avg, F, Sum
from django.db.models.functions import ExtractYear


class WeatherStationRepository:
    # Prototype
    def __init__(self): ...

    def get_station_by_name(self, station_name: str) -> WeatherStation: ...

    def get_or_create_station(
        self, station_name: str
    ) -> tuple[WeatherStation, bool]: ...

    def add_station(self, station: WeatherStation) -> WeatherStation: ...

    def add_records(
        self, records: list[WeatherRecord], station: WeatherStation | None = None
    ): ...

    def station_count(self) -> int: ...

    def record_count(self) -> int: ...


class DjangoWeatherStationRepository:

    def __init__(self):
        self._station_model = WeatherStation
        self._record_model = WeatherRecord

    def get_station_by_id(self, station_id: int) -> WeatherStation:
        return self._station_model.objects.get(pk=station_id)

    def get_station_by_name(self, station_name: str):
        return self._station_model.objects.filter(station_name=station_name).first()

    def get_or_create_station(self, station_name: str) -> tuple[WeatherStation, None]:
        return self._station_model.objects.get_or_create(station_name=station_name)

    def get_or_create_record(
        self, station, date, **defaults
    ) -> tuple[WeatherRecord, bool]:
        return self._record_model.objects.get_or_create(
            station=station, date=date, defaults=defaults
        )

    def add_station(self, station: WeatherStation) -> WeatherStation:
        station.save()
        return station

    def station_count(self) -> int:
        return self._station_model.objects.count()

    def record_count(self) -> int:
        return self._record_model.objects.count()

    def add_records(
        self, records: list[WeatherRecord], station: WeatherStation | None = None
    ) -> list[WeatherRecord]:
        if station:
            for record in records:
                record.station = station.pk
        # update_conflicts will update on duplicates in station/date fields
        return self._record_model.objects.bulk_create(
            records,
            update_conflicts=True,
            update_fields=["max_temperature", "min_temperature", "precipitation"],
            unique_fields=["station", "date"],
        )


class WeatherStatisticsRepository:
    def __init__(self): ...

    def create_station_yearly_statistic(
        self, station: WeatherStation
    ) -> tuple[WeatherStatistic, bool]: ...

    def create_all_stations_yearly_statistics(self) -> list[WeatherStatistic]: ...


class DjangoWeatherStatisticRepository:
    def __init__(self):
        self._station_model = WeatherStation
        self._statistics_model = WeatherStatistic
        self._update_fields = [
            "avg_max_temperature",
            "avg_min_temperature",
            "total_precipitation",
        ]
        self._unique_fields = ["station", "year"]

    def create_or_update_station_statistics(
        self, station: WeatherStation
    ) -> list[WeatherStatistic]:

        statistics = list(
            (
                station.weather_records.annotate(year=ExtractYear("date"))
                .values("station_id", "year")
                .annotate(
                    avg_max_temperature=Avg("max_temperature"),
                    avg_min_temperature=Avg("min_temperature"),
                    total_precipitation=Sum(F("precipitation") / 10),
                )
            )
        )

        weather_statistics = (WeatherStatistic(**statistic) for statistic in statistics)

        return WeatherStatistic.objects.bulk_create(
            weather_statistics,
            update_conflicts=True,
            update_fields=self._update_fields,
            unique_fields=self._unique_fields,
        )

    def create_or_update_all_station_statistics(self) -> list[WeatherStatistic]:
        result = list(
            (
                WeatherRecord.objects.annotate(year=ExtractYear("date"))
                .values("station_id", "year")
                .annotate(
                    avg_max_temperature=Avg("max_temperature"),
                    avg_min_temperature=Avg("min_temperature"),
                    total_precipitation=Sum(F("precipitation") / 10),
                )
            )
        )

        weather_statistics = (WeatherStatistic(**statistic) for statistic in result)

        # Updates the values on station_id conflict instead of creating another instance
        return WeatherStatistic.objects.bulk_create(
            weather_statistics,
            update_conflicts=True,
            update_fields=self._update_fields,
            unique_fields=self._unique_fields,
        )
