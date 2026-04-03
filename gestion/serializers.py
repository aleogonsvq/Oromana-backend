from rest_framework import serializers
from .models import User, TramoHorario, MaestroGuardia, Disponibilidad, Falta
# Añade esta importación arriba del todo si no la tienes
from django.contrib.auth.hashers import make_password

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
        read_only_fields = ['maestro']

# Añade esta clase al final del archivo
class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        # Regla 1: Validar el dominio del correo
        if not value.endswith('@ceiporomana.com'):
            raise serializers.ValidationError("Solo se permiten correos del dominio corporativo @ceiporomana.com")
        return value

    def create(self, validated_data):
        # Regla 2: Crear el usuario, encriptar contraseña y asignar rol MAESTRO por defecto
        user = User.objects.create(
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            rol='MAESTRO'
        )
        return user