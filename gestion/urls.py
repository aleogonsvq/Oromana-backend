from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TramoHorarioViewSet, MaestroGuardiaViewSet, FaltaViewSet

router = DefaultRouter()
router.register(r'tramos', TramoHorarioViewSet)
router.register(r'guardias', MaestroGuardiaViewSet)
router.register(r'faltas', FaltaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]