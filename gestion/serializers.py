from rest_framework import serializers
from .models import User, TramoHorario, MaestroGuardia, Disponibilidad, Falta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'rol']

class TramoHorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TramoHorario
        fields = ['id', 'nombre']

class DisponibilidadSerializer(serializers.ModelSerializer):
    tramo = TramoHorarioSerializer(read_only=True) # Para que nos devuelva el nombre del tramo, no solo el ID

    class Meta:
        model = Disponibilidad
        fields = ['id', 'dia', 'tramo']

class MaestroGuardiaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    disponibilidades = DisponibilidadSerializer(many=True, read_only=True)

    class Meta:
        model = MaestroGuardia
        fields = ['id', 'usuario', 'rol_guardia', 'disponibilidades']

class FaltaSerializer(serializers.ModelSerializer):
    # Al leer, queremos ver los datos completos del maestro y los tramos
    maestro_detalle = UserSerializer(source='maestro', read_only=True)
    tramos_detalle = TramoHorarioSerializer(source='tramos_ausencia', many=True, read_only=True)
    maestro_asignado_detalle = MaestroGuardiaSerializer(source='maestro_asignado', read_only=True)

    class Meta:
        model = Falta
        fields = [
            'id', 'maestro', 'maestro_detalle', 'fecha', 'clase', 
            'tramos_ausencia', 'tramos_detalle', 'archivo', 
            'estado', 'maestro_asignado', 'maestro_asignado_detalle'
        ]
        # Hacemos que ciertos campos sean solo de lectura para evitar que un maestro los modifique al crear la falta
        read_only_fields = ['estado', 'maestro_asignado', 'maestro']