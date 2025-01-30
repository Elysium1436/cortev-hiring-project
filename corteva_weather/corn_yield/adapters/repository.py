from ..models import CornYieldModel
from typing import Iterable


class DjangoCornYieldRepository:
    def __init__(self):
        self.yield_model = CornYieldModel

    def bulk_create_or_update_yield(self, instances: Iterable[CornYieldModel]):
        return self.yield_model.objects.bulk_create(
            instances,
            update_conflicts=True,
            update_fields=["corn_yield"],
            unique_fields=["year"],
        )
