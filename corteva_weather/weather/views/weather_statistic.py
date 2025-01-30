from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)
from ..models import WeatherStatistic
from ..adapters.repositories import (
    DjangoWeatherStationRepository,
    DjangoWeatherStatisticRepository,
)
from ..adapters.unitofwork import (
    DjangoStatisticUnitOfWork,
)
from ..serializers import (
    WeatherStatisticSerializer,
)
from ..filtersets import WeatherStatisticFilter
from django_filters.rest_framework import DjangoFilterBackend

example_field = OpenApiExample(
    "WeatherStatistic Response Example",
    value={
        "year": 2025,
        "avg_max_temperature": 10,
        "avg_min_temperature": 10,
        "total_precipitation": 10,
        "station": 25,
    },
    response_only=True,
)


@extend_schema(tags=["Weather Statistics"])
@extend_schema_view(
    generate_statistics=extend_schema(
        responses={201: WeatherStatisticSerializer(many=True)}, request=None
    ),
    generate_station_statistic=extend_schema(
        examples=[example_field],
        parameters=[
            OpenApiParameter(
                name="id",
                description="The **station's** id to generate statistics.",
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={201: WeatherStatisticSerializer},
        request=None,
    ),
)
class WeatherStatisticsViewSet(ReadOnlyModelViewSet):
    queryset = WeatherStatistic.objects.order_by("station", "year").all()
    serializer_class = WeatherStatisticSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = WeatherStatisticFilter

    @action(
        methods=["post"],
        detail=False,
        url_path="generate-statistics",
        pagination_class=None,
        filterset_class=None,
    )
    def generate_statistics(self, request):
        statistic_repository = DjangoWeatherStatisticRepository()
        uow = DjangoStatisticUnitOfWork(statistic_repository=statistic_repository)
        with uow:
            statistics = (
                uow.statistic_repository.create_or_update_all_station_statistics()
            )
        return Response(
            WeatherStatisticSerializer(statistics, many=True).data, status=201
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="generate-statistics",
        pagination_class=None,
        filterset_class=None,
    )
    def generate_station_statistic(self, request, pk):
        statistic_repository = DjangoWeatherStatisticRepository()
        station_repository = DjangoWeatherStationRepository()
        uow = DjangoStatisticUnitOfWork(statistic_repository=statistic_repository)

        with uow:
            station = station_repository.get_station_by_id(pk)
            statistic = uow.statistic_repository.create_or_update_station_statistics(
                station
            )

        return Response(
            WeatherStatisticSerializer(statistic, many=True).data, status=201
        )
