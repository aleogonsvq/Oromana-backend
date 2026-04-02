from django.contrib import admin
from .models import User, TramoHorario, MaestroGuardia, Falta, Disponibilidad
from django.contrib.auth.hashers import make_password

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Columnas que se verán en la lista de usuarios
    list_display = ('email', 'rol', 'is_staff', 'is_active')
    # Filtros laterales
    list_filter = ('rol', 'is_staff')
    # Barra de búsqueda
    search_fields = ('email',)
    # AÑADE ESTA FUNCIÓN: Intercepta el guardado para encriptar la contraseña
    def save_model(self, request, obj, form, change):
        # Si hay contraseña y NO empieza por el algoritmo de encriptación de Django...
        if obj.password and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(obj.password) # ...la encriptamos
        super().save_model(request, obj, form, change)

@admin.register(TramoHorario)
class TramoHorarioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


# 1. Creamos el Inline para la disponibilidad
class DisponibilidadInline(admin.TabularInline):
    model = Disponibilidad
    extra = 1  # Filas en blanco que aparecerán por defecto

@admin.register(MaestroGuardia)
class MaestroGuardiaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol_guardia')
    list_filter = ('rol_guardia',)
    search_fields = ('usuario__email',)
    # Añadimos el panel integrado
    inlines = [DisponibilidadInline]

@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    list_display = ('maestro', 'fecha', 'clase', 'estado', 'maestro_asignado')
    list_filter = ('estado', 'fecha')
    search_fields = ('maestro__email', 'clase')
    filter_horizontal = ('tramos_ausencia',)

