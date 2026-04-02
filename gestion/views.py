from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes # <- ¿Están estos dos?
from rest_framework.response import Response                       # <- ¿Está este?
from django.utils import timezone
from django.db.models import Q

from .models import TramoHorario, MaestroGuardia, Falta
from .serializers import TramoHorarioSerializer, MaestroGuardiaSerializer, FaltaSerializer, UserSerializer # <- ¿Añadiste UserSerializer aquí?
from .permissions import IsDirectivoOrSuperadmin
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def current_user(request):
    """
    Endpoint para que el frontend obtenga los datos del usuario logueado.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class TramoHorarioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TramoHorario.objects.all()
    serializer_class = TramoHorarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class MaestroGuardiaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MaestroGuardia.objects.all()
    serializer_class = MaestroGuardiaSerializer
    # Solo Directivos y Superadmins pueden ver quién está de guardia
    permission_classes = [permissions.IsAuthenticated, IsDirectivoOrSuperadmin]

class FaltaViewSet(viewsets.ModelViewSet):
    serializer_class = FaltaSerializer
    
    def get_permissions(self):
        """
        Define qué puede hacer cada rol.
        """
        # Si la acción es modificar o borrar, exigimos ser Directivo o Superadmin
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsDirectivoOrSuperadmin()]
        # Para listar, ver detalles o crear faltas, basta con estar logueado
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        """
        Filtra las faltas según el rol del usuario logueado.
        """
        user = self.request.user
        
        # El directivo o superadmin ve TODAS las faltas
        if user.rol in ['DIRECTIVO', 'SUPERADMIN']:
            return Falta.objects.all()
            
        # El maestro ve el historial completo de sus propias faltas [cite: 16]
        # Y además puede ver las faltas de todos los compañeros del día actual [cite: 17]
        hoy = timezone.now().date()
        return Falta.objects.filter(Q(maestro=user) | Q(fecha=hoy)).distinct()

    def perform_create(self, serializer):
        # Asignamos al creador como el maestro de la falta de forma automática
        serializer.save(maestro=self.request.user)