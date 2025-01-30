from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from .serializers import CornYieldSerializer, CornYieldFileSerializer
from .models import CornYieldModel
from .adapters.repository import DjangoCornYieldRepository
from .adapters.unitofwork import DjangoCornYieldUnitOfWork
from .services import ingest_yield_data, deserialize_yield_file_native_python
from .filtersets import CornYieldFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

import io

# Create your views here.


@extend_schema(tags=["Corn Yield"])
@extend_schema_view(
    upload_corn_yield_file=extend_schema(
        request=CornYieldFileSerializer,
        responses={201: CornYieldSerializer},
    )
)
class CornYieldViewSet(ReadOnlyModelViewSet):
    queryset = CornYieldModel.objects.order_by("year").all()
    serializer_class = CornYieldSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CornYieldFilter

    @action(
        methods=["post"],
        detail=False,
        parser_classes=[MultiPartParser],
        url_path="upload-file",
    )
    def upload_corn_yield_file(self, request):
        serializer = CornYieldFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uploaded_file = serializer.validated_data["file"]

            # Buffer needs to be read as string.
            uploaded_file = io.TextIOWrapper(uploaded_file, encoding="utf-8")

            crop_yield_repository = DjangoCornYieldRepository()
            uow = DjangoCornYieldUnitOfWork(crop_yield_repository)

            with uow:
                yields = ingest_yield_data(
                    uow, uploaded_file, deserialize_yield_file_native_python
                )
            return Response(CornYieldSerializer(yields, many=True).data, status=201)
