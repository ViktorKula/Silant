from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MachineViewSet, MaintenanceViewSet, ComplaintsViewSet

router = DefaultRouter()
router.register(r'machines', MachineViewSet)
router.register(r'maintenances', MaintenanceViewSet)
router.register(r'complaints', ComplaintsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]