from rest_framework.routers import DefaultRouter
from .views import CornYieldViewSet


router = DefaultRouter()

router.register(r"", CornYieldViewSet, basename="corn-yield")


urlpatterns = router.urls
