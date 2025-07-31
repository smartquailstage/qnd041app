import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from usuarios.models import Prospeccion

class Command(BaseCommand):
    help = "Importa datos desde un archivo CSV al modelo Prospeccion"

    def handle(self, *args, **kwargs):
        BASE_DIR = Path(settings.BASE_DIR)
        ENV_FILE_PATH = BASE_DIR / ".env_stage"
        load_dotenv(dotenv_path=ENV_FILE_PATH)

        csv_path = os.getenv('CSV_PATH')

        if not csv_path:
            raise CommandError("❌ La variable de entorno CSV_PATH no está definida en .env_stage.")

        if not os.path.exists(csv_path):
            raise CommandError(f"❌ No se encontró el archivo CSV en: {csv_path}")

        self.stdout.write(f"📄 Cargando archivo CSV desde: {csv_path}")

        # Intentar leer el CSV con delimitador ';' y engine='python'
        try:
            df = pd.read_csv(csv_path, encoding='utf-8', sep=';', engine='python')
        except Exception as e:
            raise CommandError(f"❌ Error al leer el archivo CSV: {e}")

        # Eliminar columnas sin nombre si existen
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Verificar columnas requeridas
        campos_requeridos = ['DISTRITO', 'NOMBRE DE LA INSTITUCIÓN']
        for campo in campos_requeridos:
            if campo not in df.columns:
                raise CommandError(f"❌ Falta columna obligatoria en el CSV: '{campo}'")

        # Eliminar filas con valores NaN en las columnas clave
        df = df.dropna(subset=['DISTRITO', 'NOMBRE DE LA INSTITUCIÓN'], how='any')

        nuevos = 0
        actualizados = 0
        filas_omitidas = 0

        # Función para manejar los valores NaT y NaN y convertirlos a None
        def safe_to_datetime(val):
            # Si el valor es 'NaT', 'nan' o cualquier valor vacío, devolver None
            if pd.isnull(val) or val == 'NaT' or val == 'nan':
                return None
            return pd.to_datetime(val, errors='coerce')

        # Función para truncar los valores a 20 caracteres si es necesario
        def truncate_value(val, max_length=20):
            if isinstance(val, str) and len(val) > max_length:
                return val[:max_length]
            return val

        # Procesar fila por fila
        for _, row in df.iterrows():
            try:
                # Convertir las fechas de forma segura
                tl_fecha_contacto = safe_to_datetime(row.get('TERAPIA DE LENGUAJE\nFECHA DE CONTACTO'))
                tl_fecha_proximo_contacto = safe_to_datetime(row.get('TL\nFECHA PROXIMO CONTACTO'))
                psicologia_fecha_proximo_contacto = safe_to_datetime(row.get('P\nFECHA PROXIMO CONTACTO'))
                vya_fecha_proximo_contacto = safe_to_datetime(row.get('VYA\nFECHA PROXIMO\n CONTACTO'))

                # Truncar valores para asegurarse de que no excedan el límite de 20 caracteres
                nombre_institucion = truncate_value(row.get('NOMBRE DE LA INSTITUCIÓN'))
                distrito = truncate_value(row.get('DISTRITO'))
                provincia = truncate_value(row.get('PROVINCIA'))
                zona = truncate_value(row.get('ZONA'))
                sostenimiento = truncate_value(row.get('SOSTENIMIENTO'))
                estado = truncate_value(row.get('ESTADO'))
                telefono = truncate_value(row.get('TELEFONO'))
                sector = truncate_value(row.get('SECTOR'))
                direccion = truncate_value(row.get('DIRECCION'))

                # Crear o actualizar objeto en la base de datos
                obj, created = Prospeccion.objects.update_or_create(
                    nombre_institucion=nombre_institucion,
                    defaults={
                        'distrito': distrito,
                        'provincia': provincia,
                        'zona': zona,
                        'sostenimiento': sostenimiento,
                        'estado': estado,
                        'telefono': telefono,
                        'sector': sector,
                        'direccion': direccion,
                        'tl_nombre_contacto': row.get('TERAPIA DE LENGUAJE \nNOMBRE DE CONTACTO'),
                        'tl_cargo_contacto': row.get('TERAPIA DE LENGUAJE \nCARGO CONTACTO'),
                        'tl_email': row.get('TERAPIA DE LENGUAJE \nEMAIL'),
                        'tl_proceso_realizado': row.get('TERAPIA DE LENGUAJE\nPROCESO REALIZADO'),
                        'tl_responsable': row.get('TERAPIA DE LENGUAJE\nRESPONSABLE'),
                        'tl_fecha_contacto': tl_fecha_contacto,
                        'tl_observaciones': row.get('TL\nGENERAL OBSERVACIONES'),
                        'tl_fecha_proximo_contacto': tl_fecha_proximo_contacto,
                        'psicologia_email': row.get('PSICOLOGIA\nEMAIL'),
                        'psicologia_observaciones': row.get('P\nGENERAL OBSERVACIONES'),
                        'psicologia_fecha_proximo_contacto': psicologia_fecha_proximo_contacto,
                        'vya_observacion': row.get('VYA\nOBSERVACIÓN'),
                        'vya_observaciones': row.get('VYA\nGENERAL OBSERVACIONES'),
                        'vya_fecha_proximo_contacto': vya_fecha_proximo_contacto,
                    }
                )
                if created:
                    nuevos += 1
                else:
                    actualizados += 1
            except Exception as e:
                filas_omitidas += 1
                self.stdout.write(self.style.ERROR(f"❌ Error al procesar fila: {e}"))

        self.stdout.write(self.style.SUCCESS(
            f"✅ Importación completada: {nuevos} nuevos, {actualizados} actualizados, {filas_omitidas} filas omitidas."
        ))
