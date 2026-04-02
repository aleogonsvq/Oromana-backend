from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

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