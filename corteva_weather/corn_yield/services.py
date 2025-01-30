import io
from .models import CornYieldModel
from .adapters.unitofwork import DjangoCornYieldUnitOfWork
from .adapters.repository import DjangoCornYieldRepository
from typing import Callable, Iterable


def deserialize_yield_file_native_python(file: io.StringIO):
    data = []
    for line in file.readlines():
        if line.strip():
            year, corn_yield = line.strip().split()
            year, corn_yield = int(year), int(corn_yield)
            instance = CornYieldModel(year=year, corn_yield=corn_yield)
            data.append(instance)
    return data


def ingest_yield_data(
    uow: DjangoCornYieldUnitOfWork,
    file: io.StringIO,
    deserialize_yield_file_strategy: Callable[[io.StringIO], Iterable[CornYieldModel]],
):

    yield_instances = deserialize_yield_file_strategy(file)
    instances = uow.yield_repository.bulk_create_or_update_yield(yield_instances)
    return instances


def ingest_yield_data_from_local_file(file_path):

    with open(file_path, "r") as f:
        uow = DjangoCornYieldUnitOfWork(DjangoCornYieldRepository())
        with uow:
            ingest_yield_data(uow, f, deserialize_yield_file_native_python)
