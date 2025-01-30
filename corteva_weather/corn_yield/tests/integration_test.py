import pytest
from ..adapters.unitofwork import DjangoCornYieldUnitOfWork
from ..adapters.repository import DjangoCornYieldRepository
from ..services import ingest_yield_data, deserialize_yield_file_native_python
from ..models import CornYieldModel
import io


@pytest.mark.django_db
def test_ingest_yield_data():
    file = io.StringIO("1989\t10\n1990\t10")
    repo = DjangoCornYieldRepository()
    with DjangoCornYieldUnitOfWork(repo) as uow:
        instances = ingest_yield_data(uow, file, deserialize_yield_file_native_python)

    instances = list(CornYieldModel.objects.order_by("id").all())

    assert instances[0].year == 1989
    assert instances[0].corn_yield == 10
    assert instances[1].year == 1990
    assert instances[1].corn_yield == 10
