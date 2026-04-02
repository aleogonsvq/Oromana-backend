from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TramoHorarioViewSet, MaestroGuardiaViewSet, FaltaViewSet, current_user

router = DefaultRouter()
router.register(r'tramos', TramoHorarioViewSet)
router.register(r'guardias', MaestroGuardiaViewSet)

# AÑADIMOS EL BASENAME AQUÍ
router.register(r'faltas', FaltaViewSet, basename='falta')

urlpatterns = [
    path('auth/me/', current_user, name='current_user'),
    path('', include(router.urls)),
]