from django.db import transaction


class UnitOfWork:
    # Prototype
    def __enter__(self): ...

    def __exit__(self): ...


class DjangoUnitOfWork:
    def __init__(self):
        self._transaction = None
        self._savepoint = None

    def __enter__(self):
        self._transaction = transaction.atomic()
        self._transaction.__enter__()
        self._savepoint = transaction.savepoint()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._transaction.__exit__(exc_type, exc_value, traceback)
