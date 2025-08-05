#!/bin/bash

echo "🚨 Reiniciando migraciones de Django (sin borrar la base de datos)..."

# Paso 1: Eliminar archivos de migración (excepto __init__.py)
echo "🧹 Eliminando archivos de migración..."
find . -path "*/migrations/0*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

# Paso 2: Regenerar migraciones
#echo "⚙️  Generando nuevas migraciones..."
#python manage.py makemigrations

# Paso 3: Aplicar migraciones
#echo "🚀 Aplicando migraciones..."
#python manage.py migrate

echo "✅ Migraciones reiniciadas (base de datos conservada)."
