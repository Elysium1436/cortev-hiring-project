from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from drf_spectacular.utils import extend_schema, extend_schema_view
from pathlib import Path
import io
from ..models import WeatherStation
from ..adapters.repositories import (
    DjangoWeatherStationRepository,
)
from ..adapters.unitofwork import (
    DjangoStationUnitOfWork,
)
from ..services import ingest_station_data, deserialize_station_data_native_python
from ..serializers import (
    WeatherStationSerializer,
    WeatherStationFileSerializer,
    WeatherStationRecordSerializer,
)


@extend_schema(tags=["Weather Station"])
@extend_schema_view(
    upload_station_file=extend_schema(
        request=WeatherStationFileSerializer,
        responses={201: WeatherStationRecordSerializer},
    )
)
class WeatherStationViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    queryset = WeatherStation.objects.order_by("station_name").all()
    serializer_class = WeatherStationSerializer

    @action(
        methods=["post"],
        detail=False,
        parser_classes=[MultiPartParser],
        url_path="upload-file",
    )
    def upload_station_file(self, request):
        """
        Ingests data from station file.
        Will use the filename as the station name, with the file extension exluded.
        """

        serializer = WeatherStationFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uploaded_file = serializer.validated_data["file"]
            file_name = uploaded_file.name

            # Buffer needs to be read as string.
            uploaded_file = io.TextIOWrapper(uploaded_file, encoding="utf-8")
            station_name = Path(file_name).stem

            station_repository = DjangoWeatherStationRepository()
            uow = DjangoStationUnitOfWork(station_repository=station_repository)
            with uow:
                station, records = ingest_station_data(
                    uow,
                    station_name,
                    uploaded_file,
                    deserialize_station_data_native_python,
                )

            response_data = WeatherStationRecordSerializer(
                {"station": station, "records": records}
            ).data
            return Response(data=response_data, status=201)
