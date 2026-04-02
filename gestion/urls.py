from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import TramoHorarioViewSet, MaestroGuardiaViewSet, FaltaViewSet, current_user

router = DefaultRouter()
router.register(r'tramos', TramoHorarioViewSet)
router.register(r'guardias', MaestroGuardiaViewSet)
router.register(r'faltas', FaltaViewSet, basename='falta')

urlpatterns = [
    # URLs para JWT (Login)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Nuestro endpoint para saber quién está logueado
    path('auth/me/', current_user, name='current_user'),
    
    # Resto de la API
    path('', include(router.urls)),
]