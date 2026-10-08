import os
import sys

# 1. Asegurar la ruta del proyecto
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# 2. Configurar entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qnd041app.settings')

import django
django.setup()

import csv
import re
from django.contrib.auth import get_user_model

User = get_user_model()

# ==========================================
# CONFIGURACIÓN DEL ARCHIVO DE ENTRADA
# ==========================================
INPUT_FILE = "entrada.csv"  # Cambia esto si tu archivo tiene otro nombre

def limpiar_telefono(tel):
    if not tel:
        return ""
    tel_limpio = re.sub(r'\D', '', str(tel))
    if tel_limpio.startswith('0') and len(tel_limpio) == 10:
        return '593' + tel_limpio[1:]
    elif len(tel_limpio) == 9:
        return '593' + tel_limpio
    return tel_limpio

def dividir_nombre(nombre_completo):
    if not nombre_completo:
        return "", ""
    partes = str(nombre_completo).strip().split()
    if len(partes) == 0:
        return "", ""
    elif len(partes) == 1:
        return partes[0], ""
    else:
        return partes[0], " ".join(partes[1:])

print(f"Iniciando la importación desde: '{INPUT_FILE}'...")

registros_totales = 0
registros_creados = 0
registros_omitidos_correo = 0
registros_omitidos_duplicados = 0
registros_omitidos_db = 0

correos_procesados = set()

try:
    with open(INPUT_FILE, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        reader.fieldnames = [col.strip() for col in reader.fieldnames]
        
        for row in reader:
            registros_totales += 1
            
            correo = row.get('CORREO', '').strip().lower()
            
            if not correo or correo == 'nan' or correo == '':
                registros_omitidos_correo += 1
                continue
                
            if correo in correos_procesados:
                registros_omitidos_duplicados += 1
                continue
                
            correos_procesados.add(correo)
            
            if User.objects.filter(email=correo).exists():
                registros_omitidos_db += 1
                continue
                
            nombre_completo = row.get('NOMBRE_CLIENTE', '').strip()
            telefono_raw = row.get('TELEFONO', row.get('CELULAR', ''))
            nombre_empresa = row.get('SUB_SEGMENTO', '').strip()
            
            first_name, last_name = dividir_nombre(nombre_completo)
            telefono = limpiar_telefono(telefono_raw)
            
            nombre_usuario_mail = correo.split('@')[0]
            password_temporal = f"{nombre_usuario_mail}12345"
            
            try:
                User.objects.create_user(
                    email=correo,
                    password=password_temporal,
                    first_name=first_name,
                    last_name=last_name,
                    nombre_empresa=nombre_empresa,
                    telefono=telefono,
                    is_active=True,
                    is_staff=True,
                    acepta_terminos=True,
                    suscripcion_noticias=False
                )
                registros_creados += 1
            except Exception as e:
                print(f"Error al crear el usuario {correo}: {e}")

    print("\n¡Proceso de importación y encriptación finalizado!")
    print(f"- Archivo procesado: {INPUT_FILE}")
    print(f"- Registros totales leídos: {registros_totales}")
    print(f"- Usuarios creados con contraseña cifrada: {registros_creados}")
    print(f"- Omitidos (sin correo): {registros_omitidos_correo}")
    print(f"- Omitidos (duplicados en CSV): {registros_omitidos_duplicados}")
    print(f"- Omitidos (ya existían en la BD): {registros_omitidos_db}")

except FileNotFoundError:
    print(f"Error: No se encontró el archivo '{INPUT_FILE}'.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")