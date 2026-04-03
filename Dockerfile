# 1. Utilizamos una imagen base oficial de Python ligera
FROM python:3.12-slim

# 2. Le decimos a Python que no escriba archivos .pyc (caché) y que imprima los logs directamente en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Creamos una carpeta llamada /app dentro del contenedor y nos movemos a ella
WORKDIR /app

# 4. Copiamos SOLO el archivo de requisitos primero (esto optimiza la caché de Docker)
COPY requirements.txt /app/

# 5. Instalamos las librerías
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# 6. Copiamos todo el resto de nuestro código local a la carpeta /app del contenedor
COPY . /app/

# 7. Exponemos el puerto 8000 para que podamos conectarnos desde fuera
EXPOSE 8000

# 8. El comando que se ejecutará por defecto al encender el contenedor
# IMPORTANTE: Usamos 0.0.0.0 para que el servidor sea accesible desde fuera del contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]