#!/usr/bin/env bash
# Salir si hay algún error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Recopilar archivos estáticos (CSS del admin)
python manage.py collectstatic --no-input

# Ejecutar migraciones en la base de datos de Neon
python manage.py migrate