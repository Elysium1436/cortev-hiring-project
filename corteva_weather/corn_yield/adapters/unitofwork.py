from corteva_weather.adapters.unitofwork import DjangoUnitOfWork
from .repository import DjangoCornYieldRepository


class DjangoCornYieldUnitOfWork(DjangoUnitOfWork):
    def __init__(self, yield_repository: DjangoCornYieldRepository):
        self.yield_repository = yield_repository
        return super().__init__()
