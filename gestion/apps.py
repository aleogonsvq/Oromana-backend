from django.apps import AppConfig

class GestionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion'

    # Añadimos la función ready() para importar las señales al arrancar
    def ready(self):
        import gestion.signals