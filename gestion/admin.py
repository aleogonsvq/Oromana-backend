from django.contrib import admin
from .models import User, TramoHorario, MaestroGuardia, Falta

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    # Columnas que se verán en la lista de usuarios
    list_display = ('email', 'rol', 'is_staff', 'is_active')
    # Filtros laterales
    list_filter = ('rol', 'is_staff')
    # Barra de búsqueda
    search_fields = ('email',)

@admin.register(TramoHorario)
class TramoHorarioAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(MaestroGuardia)
class MaestroGuardiaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol_guardia', 'mostrar_tramos')
    list_filter = ('rol_guardia',)
    search_fields = ('usuario__email',)
    # filter_horizontal crea una interfaz visual mucho más cómoda para asignar múltiples tramos
    filter_horizontal = ('tramos_disponibles',)

    def mostrar_tramos(self, obj):
        # Muestra los tramos asignados separados por comas en la tabla principal
        return ", ".join([tramo.nombre for tramo in obj.tramos_disponibles.all()])
    mostrar_tramos.short_description = 'Tramos Disponibles'

@admin.register(Falta)
class FaltaAdmin(admin.ModelAdmin):
    list_display = ('maestro', 'fecha', 'clase', 'estado', 'maestro_asignado')
    list_filter = ('estado', 'fecha')
    search_fields = ('maestro__email', 'clase')
    filter_horizontal = ('tramos_ausencia',)

