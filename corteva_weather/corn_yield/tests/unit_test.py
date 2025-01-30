import pytest
from ..services import ingest_yield_data, deserialize_yield_file_native_python


class FakeUoW:

    def __init__(self, fake_yield_repository):
        self.yield_repository = fake_yield_repository

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return


class FakeRepository:
    def bulk_create_or_update_yield(self, yield_instances):
        return yield_instances


class FakeFile:
    def readlines(self):
        return ["1989   10", "1990   10"]


def test_ingest_yield_data():

    with FakeUoW(FakeRepository()) as uow:
        instances = ingest_yield_data(
            uow, FakeFile(), deserialize_yield_file_native_python
        )

    assert instances[0].year == 1989
    assert instances[0].corn_yield == 10
    assert instances[1].year == 1990
    assert instances[1].corn_yield == 10
