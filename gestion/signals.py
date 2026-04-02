from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from .models import Falta

@receiver(post_save, sender=Falta)
def enviar_email_sustitucion(sender, instance, created, **kwargs):
    # Verificamos si la falta está cubierta y tiene un maestro de guardia asignado
    if instance.estado == 'CUBIERTA' and instance.maestro_asignado:
        
        # Preparamos los datos del correo
        destinatario = instance.maestro_asignado.usuario.email
        asunto = f"Aviso de Sustitución: {instance.clase} - {instance.fecha.strftime('%d/%m/%Y')}"
        
        # Extraemos los tramos afectados
        tramos = ", ".join([tramo.nombre for tramo in instance.tramos_ausencia.all()])
        
        mensaje = f"""
Hola,

Se te ha asignado una guardia para cubrir la ausencia del maestro {instance.maestro.email}.

DETALLES DE LA SUSTITUCIÓN:
-----------------------------------------
- Fecha: {instance.fecha.strftime('%d/%m/%Y')}
- Clase afectada: {instance.clase}
- Tramos a cubrir: {tramos}
-----------------------------------------

"""
        if instance.archivo:
            mensaje += "Se adjunta el material didáctico dejado por el profesor para los alumnos."
        else:
            mensaje += "El profesor no ha dejado material didáctico adjunto."

        mensaje += "\n\nUn saludo,\nEquipo Directivo."

        # Construimos el email
        email = EmailMessage(
            subject=asunto,
            body=mensaje,
            from_email='direccion@ceiporomana.com',
            to=[destinatario],
        )

        # Si hay archivo adjunto en la falta, lo incluimos en el correo
        if instance.archivo:
            email.attach_file(instance.archivo.path)

        # Enviamos el correo (se imprimirá en la consola gracias a nuestra configuración)
        email.send(fail_silently=False)