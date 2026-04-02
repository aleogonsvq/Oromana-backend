from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El Email es obligatorio')
        
        email = self.normalize_email(email)
        
        # Validación del dominio corporativo
        if not email.endswith('@ceiporomana.com'):
            raise ValidationError('El correo debe pertenecer al dominio @ceiporomana.com')
            
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'SUPERADMIN')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    # Definimos las opciones de roles
    ROLES = (
        ('MAESTRO', 'Maestro'),
        ('DIRECTIVO', 'Directivo'),
        ('SUPERADMIN', 'Superadmin'),
    )
    
    # Eliminamos el username tradicional de Django
    username = None 
    
    # Configuramos el email como campo principal y único
    email = models.EmailField('correo electrónico', unique=True)
    
    # Añadimos el campo de rol
    rol = models.CharField(max_length=15, choices=ROLES, default='MAESTRO')

    # Le decimos a Django que el login se hace con el email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} - {self.get_rol_display()}"
    
# Validador personalizado para el límite de 5MB
def validar_tamano_archivo(value):
    limite_mb = 5
    if value.size > limite_mb * 1024 * 1024:
        raise ValidationError(f'El tamaño máximo del archivo es de {limite_mb}MB.')

class TramoHorario(models.Model):
    """
    Define las horas o periodos lectivos (ej: '1ª Hora (09:00 - 09:45)', 'Recreo', etc.)
    """
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class MaestroGuardia(models.Model):
    """
    Tabla de profesores disponibles para hacer guardias.
    """
    ROLES_GUARDIA = (
        ('APOYO', 'Apoyo'),
        ('COORDINACION', 'Coordinación'),
        ('MAYOR55', 'Mayor de 55 años'),
    )
    
    # Lo vinculamos al usuario de forma única (un usuario solo tiene un perfil de guardia)
    usuario = models.OneToOneField('User', on_delete=models.CASCADE, related_name='perfil_guardia')
    rol_guardia = models.CharField(max_length=20, choices=ROLES_GUARDIA)
    
    # Relación muchos a muchos: Un maestro puede estar disponible en varios tramos
    tramos_disponibles = models.ManyToManyField(TramoHorario, related_name='maestros_disponibles')

    def __str__(self):
        return f"Guardia: {self.usuario.email} - {self.get_rol_guardia_display()}"

class Falta(models.Model):
    """
    Registro de la ausencia notificada por el maestro.
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('CUBIERTA', 'Cubierta'),
    )

    # El maestro que notifica la falta
    maestro = models.ForeignKey('User', on_delete=models.CASCADE, related_name='faltas_registradas')
    
    # Fecha de la ausencia (por defecto el día en curso)
    fecha = models.DateField(default=timezone.now)
    
    # Grupo de alumnos afectado
    clase = models.CharField(max_length=50, help_text="Ej: 3ºA, 5ºB")
    
    # Tramos afectados por la ausencia
    tramos_ausencia = models.ManyToManyField(TramoHorario, related_name='faltas_afectadas')
    
    # Material didáctico (con límite de 5MB)
    archivo = models.FileField(upload_to='materiales/', blank=True, null=True, validators=[validar_tamano_archivo])
    
    # Estado de la falta
    estado = models.CharField(max_length=15, choices=ESTADOS, default='PENDIENTE')
    
    # Maestro de guardia asignado por el directivo
    maestro_asignado = models.ForeignKey(MaestroGuardia, on_delete=models.SET_NULL, null=True, blank=True, related_name='sustituciones_asignadas')

    def __str__(self):
        return f"Falta de {self.maestro.email} - {self.fecha} ({self.estado})"