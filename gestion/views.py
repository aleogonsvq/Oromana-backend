from rest_framework import viewsets
from .models import TramoHorario, MaestroGuardia, Falta
from .serializers import TramoHorarioSerializer, MaestroGuardiaSerializer, FaltaSerializer

class TramoHorarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para listar los tramos horarios. Solo lectura.
    """
    queryset = TramoHorario.objects.all()
    serializer_class = TramoHorarioSerializer

class MaestroGuardiaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint para ver los maestros de guardia y sus disponibilidades.
    """
    queryset = MaestroGuardia.objects.all()
    serializer_class = MaestroGuardiaSerializer

class FaltaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para el CRUD de faltas.
    """
    queryset = Falta.objects.all()
    serializer_class = FaltaSerializer

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario que está haciendo la petición como el 'maestro' de la falta
        serializer.save(maestro=self.request.user)