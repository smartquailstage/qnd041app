from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
import uuid
import hashlib
from django.utils import timezone
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError


from django.db import models

class CartaNombramiento(models.Model):
    # Datos de la sociedad
    nombre_sociedad = models.CharField(max_length=100, default="SMARTQUAIL S.A.S.")
    fecha_constitutiva = models.DateField(default="2020-10-20")
    fecha_acta = models.DateField(null=True, blank= True)
    fecha_inscripcion = models.DateField(null=True, blank= True)

    # Datos del accionista fundador
    nombre_accionista = models.CharField(max_length=100, default="Santiago Mauricio Silva Domínguez")
    cargo_accionista = models.CharField(max_length=50, default="Accionista fundador")

    # Datos del designado
    nombre_designado = models.CharField(max_length=100)
    numero_identificacion = models.CharField(max_length=100,null=True, blank=True)
    codigo_dactilar = models.CharField(max_length=100,null=True, blank=True)
    cargo_designado = models.CharField(max_length=50, default="Presidente")
    nacionalidad_designado = models.CharField(max_length=50, default="ecuatoriana")
    domicilio_designado = models.CharField(max_length=100, default="cantón Quito")

    # Duración del cargo
    duracion_anos = models.PositiveIntegerField(default=5)

    # Fecha de emisión de la carta
    fecha_emision = models.DateField(auto_now_add=True)

    hash_nombramiento = models.CharField(max_length=64, unique=True, null=True, blank=True) # Incidente

    # =====================================================
    # 🔐 MÉTODOS DE GENERACIÓN DE HASH
    # =====================================================
    def _generate_hash(self, doc_type: str) -> str:
        """
        Genera un hash SHA-256 único para cada documento.
        Incluye id del registro, tipo de documento, UUID y timestamp.
        """
        raw = f"{self.id}|{doc_type}|{uuid.uuid4()}|{timezone.now().isoformat()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate_hash_nombramiento(self):
        self.hash_nombramiento = self._generate_hash("DPD")
        self.save(update_fields=["hash_nombramiento"])
        return self.hash_nombramiento

    def __str__(self):
        return f"Carta de nombramiento de {self.nombre_designado} como {self.cargo_designado}"

    class Meta:
        verbose_name = "Nombramiento"
        verbose_name_plural = "Nombramientos"



# Opciones de documentación por entidad
DOC_SCVS = [
    ('ESTATUTOS', 'Estatutos de la compañía'),
    ('ACTAS_ASAMBLEA', 'Actas de Asamblea'),
    ('INFORME_FINANCIERO', 'Informe Financiero anual'),
    ('REGISTRO_DIRECTORES', 'Registro de Directores'),
]

DOC_SPDP = [
    ('CONSENTIMIENTOS', 'Consentimientos de clientes/usuarios'),
    ('RAT', 'Registro de Tratamiento de Datos'),
    ('DPIA', 'Evaluación de Impacto en Protección de Datos'),
    ('ARCO', 'Procedimiento ARCO'),
    ('INCIDENTES', 'Registro de Incidentes de Seguridad'),
    ('POLITICAS', 'Políticas internas de protección de datos'),
    ('ACTA_DELEGADO', 'Acta de nombramiento del Delegado de Datos'),
]

DOC_SRI = [
    ('RUC', 'Registro Único de Contribuyentes'),
    ('DECLARACION_IMPUESTOS', 'Declaración de Impuestos'),
    ('RETENCIONES', 'Comprobantes de Retención'),
]

DOC_MIN_TRABAJO = [
    ('CONTRATOS', 'Contratos de trabajo'),
    ('NOMINAS', 'Nóminas de empleados'),
    ('PLANILLAS', 'Planillas de seguridad social'),
]

DOC_IESS = [
    ('AFILIACIONES', 'Afiliaciones de empleados'),
    ('APORTES', 'Comprobantes de aportes'),
    ('HISTORIAL', 'Historial de aportes'),
]





class Regulacion(models.Model):


    # Nombre de la regulación o registro interno
    nombre_registro = models.CharField(max_length=255, help_text="Nombre del registro o cumplimiento interno")
    fecha_creacion = models.DateField(default=timezone.now)
    vigente = models.BooleanField(default=True)

    # Campos por entidad gubernamental
    nombre_SCVS = models.CharField(max_length=50, choices=DOC_SCVS, blank=True, null=True)
    nombre_SPDP = models.CharField(max_length=50, choices=DOC_SPDP, blank=True, null=True)
    nombre_SRI = models.CharField(max_length=50, choices=DOC_SRI, blank=True, null=True)
    nombre_MIN_TRABAJO = models.CharField(max_length=50, choices=DOC_MIN_TRABAJO, blank=True, null=True)
    nombre_IESS = models.CharField(max_length=50, choices=DOC_IESS, blank=True, null=True)
    # Campos “dummy” para Unfold conditional_fields
    scvs_extra = models.BooleanField(default=False)
    spdp_extra = models.BooleanField(default=False)
    sri_extra = models.BooleanField(default=False)
    mt_extra = models.BooleanField(default=False)
    iess_extra = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre_registro}"







# ===========================
# SCVS - Superintendencia de Compañías, Valores y Seguros
# ===========================
class SCVS_Estatutos(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='scvs_estatutos')
    nombre_empresa = models.CharField(max_length=255)
    fecha_aprobacion = models.DateField()
    notario = models.CharField(max_length=255)
    archivo = models.FileField(upload_to='scvs/estatutos/', blank=True, null=True)

    def get_document_name(self):
        return f"Estatutos_{self.nombre_empresa}_{self.fecha_aprobacion.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Estatuto SCVS"
        verbose_name_plural = "Estatutos SCVS"

from django.db import models




class SCVS_ActasAsamblea(models.Model):

    # =========================
    # RELACIÓN REGULATORIA
    # =========================
    regulacion = models.ForeignKey(
        'Regulacion',
        on_delete=models.CASCADE,
        related_name='scvs_actas',
        verbose_name="Regulación asociada",
        help_text="Regulación o proceso legal al que pertenece este conjunto documental SCVS."
    )

    # =====================================================
    # A. DATOS GENERALES DE LA JUNTA
    # =====================================================
    tipo_junta = models.CharField(
        "Tipo de junta",
        max_length=20,
        choices=[
            ('ORDINARIA', 'Junta Ordinaria'),
            ('EXTRAORDINARIA', 'Junta Extraordinaria'),
            ('UNIVERSAL', 'Junta Universal'),
        ],
        null=True, blank=True,
        help_text="Tipo de Junta General celebrada según la Ley de Compañías."
    )


    title = models.CharField(
            "Tema a tratar",
            max_length=20,
            choices=[
                ('NOMBRAMIENTOS', 'NOMBRAMIENTOS'),
                ('FINANCIERO', 'FINANCIERO'),
                ('ACCIONISTAS', 'ACCIONISTAS'),
            ],
            null=True, blank=True,
            help_text="Ttema a tratar."
        )


    fecha_asamblea = models.DateField(
        "Fecha de la asamblea",
        null=True, blank=True,
        help_text="Fecha en la que se celebró la Junta General."
    )

    hora_inicio = models.TimeField(
        "Hora de inicio",
        null=True, blank=True,
        help_text="Hora de inicio formal de la Junta General."
    )

    hora_cierre = models.TimeField(
        "Hora de cierre",
        null=True, blank=True,
        help_text="Hora de clausura de la Junta General."
    )

    lugar_asamblea = models.CharField(
        "Lugar de la asamblea",
        max_length=255,
        null=True, blank=True,
        help_text="Ciudad y dirección donde se celebró la Junta General."
    )

    ejercicio_fiscal = models.PositiveIntegerField(
        "Ejercicio fiscal",
        null=True, blank=True,
        help_text="Ejercicio económico al que corresponde la Junta General."
    )

    # =====================================================
    # B. CONVOCATORIA
    # =====================================================
    forma_convocatoria = models.CharField(
        "Forma de convocatoria",
        max_length=50,
        null=True, blank=True,
        help_text="Medio utilizado para convocar a la Junta (prensa, correo, estatuto o universal)."
    )

    fecha_convocatoria = models.DateField(
        "Fecha de convocatoria",
        null=True, blank=True,
        help_text="Fecha en la que se realizó la convocatoria formal."
    )

    medio_convocatoria = models.TextField(
        "Medio de convocatoria",
        null=True, blank=True,
        help_text="Detalle del medio de convocatoria utilizado."
    )

    convocatoria_valida = models.BooleanField(
        "Convocatoria válida",
        null=True, blank=True,
        help_text="Indica si la convocatoria cumple los requisitos legales."
    )

    # =====================================================
    # C. QUÓRUM
    # =====================================================
    capital_suscrito_total = models.DecimalField(
        "Capital suscrito total",
        max_digits=18, decimal_places=2,
        null=True, blank=True,
        help_text="Capital suscrito total de la compañía."
    )

    capital_presente = models.DecimalField(
        "Capital presente o representado",
        max_digits=18, decimal_places=2,
        null=True, blank=True,
        help_text="Capital presente o debidamente representado en la Junta."
    )

    porcentaje_asistencia = models.DecimalField(
        "Porcentaje de asistencia",
        max_digits=5, decimal_places=2,
        null=True, blank=True,
        help_text="Porcentaje del capital presente respecto al total."
    )

    quorum_valido = models.BooleanField(
        "Quórum válido",
        null=True, blank=True,
        help_text="Indica si se cumple el quórum legal para deliberar."
    )

    # =====================================================
    # D. ASISTENTES
    # =====================================================
    socios_asistentes = models.TextField(
        "Socios / Accionistas asistentes",
        null=True, blank=True,
        help_text="Listado detallado de socios o accionistas asistentes, con acciones y porcentajes."
    )

    administradores_asistentes = models.TextField(
        "Administradores asistentes",
        null=True, blank=True,
        help_text="Listado de administradores presentes en la Junta."
    )

    # =====================================================
    # E. DIRECTIVA DE LA JUNTA
    # =====================================================
    presidente_junta = models.CharField(
        "Presidente de la Junta",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre completo del presidente de la Junta General."
    )

    secretario_junta = models.CharField(
        "Secretario de la Junta",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre completo del secretario de la Junta General."
    )

    # =====================================================
    # F. ORDEN DEL DÍA
    # =====================================================
    orden_dia = models.TextField(
        "Orden del día",
        null=True, blank=True,
        help_text="Listado completo de los puntos tratados en la Junta."
    )

    # =====================================================
    # G. DESARROLLO Y RESOLUCIONES
    # =====================================================
    desarrollo_junta = models.TextField(
        "Desarrollo de la Junta",
        null=True, blank=True,
        help_text="Descripción del desarrollo de la Junta y deliberaciones."
    )

    resoluciones = models.TextField(
        "Resoluciones adoptadas",
        null=True, blank=True,
        help_text="Detalle completo de las resoluciones aprobadas."
    )

    resultados_votacion = models.TextField(
        "Resultados de votación",
        null=True, blank=True,
        help_text="Detalle de votos a favor, en contra y abstenciones."
    )

    # =====================================================
    # H. INFORME DE GERENTE
    # =====================================================
    gerente_nombre = models.CharField(
        "Nombre del gerente",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre completo del Gerente General que rinde el informe."
    )

    informe_gerente = models.TextField(
        "Informe del gerente",
        null=True, blank=True,
        help_text="Informe narrativo del gerente sobre la gestión del ejercicio fiscal."
    )

    # =====================================================
    # I. CERTIFICACIÓN Y FIRMAS
    # =====================================================
    representante_legal = models.CharField(
        "Representante legal",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del representante legal de la compañía."
    )

    abogado_patrocinador = models.CharField(
        "Abogado patrocinador",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del abogado patrocinador que certifica el acta."
    )

    contador = models.CharField(
        "Contador",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del contador responsable de la información financiera."
    )

    fecha_certificacion = models.DateField(
        "Fecha de certificación",
        null=True, blank=True,
        help_text="Fecha en que el documento fue certificado y firmado."
    )

    # =====================================================
    # ARCHIVO FINAL
    # =====================================================
    archivo = models.FileField(
        "Archivo PDF",
        upload_to='scvs/actas/',
        null=True, blank=True,
        help_text="Archivo PDF del acta firmada para subir a la SCVS."
    )


    # =====================================================
    # J. NÓMINA DE SOCIOS / ACCIONISTAS (SCVS 3.1.3)
    # =====================================================
    socios_anio_fiscal = models.PositiveIntegerField(
        "Año fiscal (Nómina de socios)",
        null=True, blank=True,
        help_text="Año fiscal al que corresponde la nómina de socios o accionistas."
    )

    socios_fecha_corte = models.DateField(
        "Fecha de corte de la nómina",
        null=True, blank=True,
        help_text="Fecha de corte de la información de socios o accionistas."
    )

    socios_tipo_compania = models.CharField(
        "Tipo de compañía",
        max_length=10,
        choices=[('SA', 'Sociedad Anónima'), ('LTDA', 'Compañía Limitada'), ('SAS', 'SAS')],
        null=True, blank=True,
        help_text="Tipo de compañía según su forma societaria."
    )

    socios_detalle = models.TextField(
        "Detalle de socios / accionistas",
        null=True, blank=True,
        help_text=(
            "Listado estructurado de socios o accionistas. "
            "Debe incluir por cada socio: tipo de persona, nombres/razón social, "
            "nacionalidad, tipo y número de identificación, número de acciones o participaciones, "
            "valor nominal, porcentaje de participación, tipo de aporte, capital suscrito y pagado."
        )
    )

    socios_total_numero = models.PositiveIntegerField(
        "Total de socios / accionistas",
        null=True, blank=True,
        help_text="Número total de socios o accionistas registrados."
    )

    socios_capital_suscrito_total = models.DecimalField(
        "Capital suscrito total (socios)",
        max_digits=18, decimal_places=2,
        null=True, blank=True,
        help_text="Capital suscrito total según la nómina de socios."
    )

    socios_capital_pagado_total = models.DecimalField(
        "Capital pagado total (socios)",
        max_digits=18, decimal_places=2,
        null=True, blank=True,
        help_text="Capital efectivamente pagado según la nómina de socios."
    )

    socios_representante_legal = models.CharField(
        "Representante legal (socios)",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del representante legal que certifica la nómina de socios."
    )

    socios_contador = models.CharField(
        "Contador (socios)",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del contador responsable de certificar la nómina de socios."
    )

    socios_fecha_certificacion = models.DateField(
        "Fecha de certificación (socios)",
        null=True, blank=True,
        help_text="Fecha de certificación de la nómina de socios."
    )



    # =====================================================
    # K. NÓMINA DE ADMINISTRADORES (SCVS 3.1.8)
    # =====================================================
    admins_anio_fiscal = models.PositiveIntegerField(
        "Año fiscal (administradores)",
        null=True, blank=True,
        help_text="Año fiscal al que corresponde la nómina de administradores."
    )

    admins_fecha_vigencia = models.DateField(
        "Fecha de vigencia del nombramiento",
        null=True, blank=True,
        help_text="Fecha desde la cual se encuentra vigente el nombramiento de los administradores."
    )

    admins_detalle = models.TextField(
        "Detalle de administradores",
        null=True, blank=True,
        help_text=(
            "Listado estructurado de administradores. "
            "Debe incluir: nombres, tipo y número de identificación, cargo, "
            "fecha de inicio y fin de funciones, forma de designación, nacionalidad."
        )
    )

    admins_representante_legal_vigente = models.BooleanField(
        "Representante legal vigente",
        null=True, blank=True,
        help_text="Indica si el representante legal consta como vigente en la nómina."
    )

    admins_observaciones = models.TextField(
        "Observaciones (administradores)",
        null=True, blank=True,
        help_text="Observaciones adicionales relacionadas con la nómina de administradores."
    )

    admins_representante_legal = models.CharField(
        "Representante legal (administradores)",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del representante legal que certifica la nómina de administradores."
    )

    admins_secretario = models.CharField(
        "Secretario de la compañía",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del secretario que certifica la nómina de administradores."
    )

    admins_fecha_certificacion = models.DateField(
        "Fecha de certificación (administradores)",
        null=True, blank=True,
        help_text="Fecha de certificación de la nómina de administradores."
    )


    # =====================================================
    # L. INFORME DE GERENTE (SCVS 3.1.5)
    # =====================================================
    gerente_anio_fiscal = models.PositiveIntegerField(
        "Año fiscal (informe del gerente)",
        null=True, blank=True,
        help_text="Año fiscal al que corresponde el informe del gerente."
    )

    gerente_nombre = models.CharField(
        "Nombre del gerente general",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre completo del Gerente General que emite el informe."
    )

    gerente_cargo = models.CharField(
        "Cargo del gerente",
        max_length=255,
        null=True, blank=True,
        help_text="Cargo oficial del gerente general."
    )

    gerente_periodo_informado = models.CharField(
        "Periodo informado",
        max_length=100,
        null=True, blank=True,
        help_text="Periodo que cubre el informe del gerente."
    )

    gerente_introduccion = models.TextField(
        "Introducción del informe",
        null=True, blank=True,
        help_text="Introducción general del informe del gerente."
    )

    gerente_situacion_financiera = models.TextField(
        "Situación financiera",
        null=True, blank=True,
        help_text="Descripción de la situación financiera de la compañía."
    )

    gerente_desempeno_operativo = models.TextField(
        "Desempeño operativo",
        null=True, blank=True,
        help_text="Análisis del desempeño operativo del ejercicio."
    )

    gerente_objeto_social = models.TextField(
        "Cumplimiento del objeto social",
        null=True, blank=True,
        help_text="Evaluación del cumplimiento del objeto social de la compañía."
    )

    gerente_decisiones = models.TextField(
        "Decisiones administrativas",
        null=True, blank=True,
        help_text="Principales decisiones administrativas adoptadas durante el ejercicio."
    )

    gerente_eventos_relevantes = models.TextField(
        "Eventos relevantes",
        null=True, blank=True,
        help_text="Eventos relevantes ocurridos durante el ejercicio fiscal."
    )

    gerente_riesgos = models.TextField(
        "Riesgos y contingencias",
        null=True, blank=True,
        help_text="Riesgos y contingencias identificados por la gerencia."
    )

    gerente_cumplimiento_legal = models.TextField(
        "Cumplimiento normativo",
        null=True, blank=True,
        help_text="Declaración de cumplimiento normativo y legal."
    )

    gerente_proyecciones = models.TextField(
        "Perspectivas futuras",
        null=True, blank=True,
        help_text="Perspectivas y proyecciones futuras de la compañía."
    )

    gerente_conclusion = models.TextField(
        "Conclusión",
        null=True, blank=True,
        help_text="Conclusión final del informe del gerente."
    )

    gerente_declaracion_responsabilidad = models.TextField(
        "Declaración de responsabilidad",
        null=True, blank=True,
        help_text="Declaración expresa de responsabilidad del gerente general."
    )

    gerente_firma = models.CharField(
        "Firma del gerente general",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del gerente general que firma el informe."
    )

    gerente_representante_legal = models.CharField(
        "Representante legal (informe gerente)",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del representante legal que suscribe el informe del gerente."
    )

    gerente_abogado = models.CharField(
        "Abogado patrocinador",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre del abogado patrocinador del informe del gerente."
    )

    gerente_fecha_emision = models.DateField(
        "Fecha de emisión del informe",
        null=True, blank=True,
        help_text="Fecha de emisión del informe del gerente."
    )

    acta_hash = models.CharField(max_length=255, blank=True, null=True)


    # =====================================================
    # METADATA
    # =====================================================
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True,null=True, blank=True)

    def get_document_name(self):
        return f"ActaJuntaSCVS_{self.fecha_asamblea.strftime('%Y%m%d') if self.fecha_asamblea else 'SIN_FECHA'}"

    def _generate_hash(self, doc_type: str) -> str:
        """
        Genera un hash SHA-256 único para cada documento.
        Incluye id del registro, tipo de documento, UUID y timestamp.
        """
        raw = f"{self.id}|{doc_type}|{uuid.uuid4()}|{timezone.now().isoformat()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate_hash_delegado(self):
        self.acta_hash = self._generate_hash("DPD")
        self.save(update_fields=["acta_hash"])
        return self.acta_hash

    class Meta:
        verbose_name = "Acta de Junta General SCVS"
        verbose_name_plural = "Actas de Junta General SCVS"

    def __str__(self):
        return self.get_document_name()



class ClausulaContrato(models.Model):

    CLAUSULA_CHOICES = [
        ('CLAUSULA_1', 'CLÁUSULA PRIMERA'),
        ('CLAUSULA_2', 'CLÁUSULA SEGUNDA'),
        ('CLAUSULA_3', 'CLÁUSULA TERCERA'),
        ('CLAUSULA_4', 'CLÁUSULA CUARTA'),
        ('CLAUSULA_5', 'CLÁUSULA QUINTA'),
        ('CLAUSULA_6', 'CLÁUSULA SEXTA'),
        ('CLAUSULA_7', 'CLÁUSULA SÉPTIMA'),
        ('CLAUSULA_8', 'CLÁUSULA OCTAVA'),
        ('CLAUSULA_9', 'CLÁUSULA NOVENA'),
        ('CLAUSULA_10', 'CLÁUSULA DÉCIMA'),
        ('CLAUSULA_11', 'CLÁUSULA UNDÉCIMA'),
        ('CLAUSULA_12', 'CLÁUSULA DUODÉCIMA'),
        ('CLAUSULA_13', 'CLÁUSULA DECIMOTERCERA'),
        ('CLAUSULA_14', 'CLÁUSULA DECIMOCUARTA'),
        ('CLAUSULA_15', 'CLÁUSULA DECIMOQUINTA'),
        ('CLAUSULA_16', 'CLÁUSULA DECIMOSEXTA'),
        ('CLAUSULA_17', 'CLÁUSULA DECIMOSÉPTIMA'),
        ('CLAUSULA_18', 'CLÁUSULA DECIMOCTAVA'),
        ('CLAUSULA_19', 'CLÁUSULA DECIMONOVENA'),
        ('CLAUSULA_20', 'CLÁUSULA VIGÉSIMA'),
        ('CLAUSULA_21', 'CLÁUSULA VIGESIMOPRIMERA'),
        ('CLAUSULA_22', 'CLÁUSULA VIGESIMOSEGUNDA'),
        ('CLAUSULA_23', 'CLÁUSULA VIGESIMOTERCERA'),
        ('CLAUSULA_24', 'CLÁUSULA VIGESIMOCUARTA'),
        ('CLAUSULA_25', 'CLÁUSULA VIGESIMOQUINTA'),
        ('CLAUSULA_26', 'CLÁUSULA VIGESIMOSEXTA'),
        ('CLAUSULA_27', 'CLÁUSULA VIGESIMOSÉPTIMA'),
        ('CLAUSULA_28', 'CLÁUSULA VIGESIMOCTAVA'),
        ('CLAUSULA_29', 'CLÁUSULA VIGESIMONOVENA'),
        ('CLAUSULA_30', 'CLÁUSULA TRIGÉSIMA'),
    ]

    titulo_clausura = models.CharField(
        max_length=260,
        verbose_name="titulo de clausura",
        null = 'True',
        blank = 'True',
    )

    contrato = models.ForeignKey(
        SCVS_ActasAsamblea,
        on_delete=models.CASCADE,
        related_name='clausulas',
        verbose_name="Contrato"
    )

    clausula = models.CharField(
        max_length=150,
        choices=CLAUSULA_CHOICES,
        verbose_name="CLÁUSULA",
        null = 'True',
        blank = 'True',
    )


    detalle = models.TextField(
        verbose_name="Detalle de la cláusula"
    )

    class Meta:
        verbose_name = "Cláusula de contrato"
        verbose_name_plural = "Cláusulas de contrato"



    def __str__(self):
        return f"Cláusula {self.clausula}"


# =================================================
# 🔧 VALIDATOR REUTILIZABLE (DJANGO STYLE)
# =================================================
def validar_cuadre_scvs(activos, pasivos, patrimonio):
    diferencia = activos - (pasivos + patrimonio)

    if diferencia != Decimal("0.00"):
        raise ValidationError(
            "❌ DESCUADRE SCVS: "
            f"Activos({activos}) != Pasivos({pasivos}) + Patrimonio({patrimonio}) | "
            f"Diferencia: {diferencia}"
        )

class SCVSFinancialReport(models.Model):
    # =========================
    # DATOS GENERALES
    # =========================
    ruc = models.CharField(
        "RUC",
        max_length=13,
        null=True, blank=True,
        help_text="Número de RUC de la compañía (13 dígitos). Es el identificador único tributario en Ecuador."
    )
    company_name = models.CharField(
        "Nombre de la compañía",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre legal completo de la compañía registrado ante la Superintendencia de Compañías."
    )
    nombre_contador = models.CharField(
        "Contador",
        max_length=255,
        null=True, blank=True,
        help_text="Nombre de contador responsable."
    )

    matricula_contador = models.CharField(
        "Numero de matricula",
        max_length=255,
        null=True, blank=True,
        help_text="Matrícula de contador"
    )

    fecha_incripcion = models.DateTimeField("Fecha de inscripción",null=True, blank=True)
    direccion =  models.CharField(
        "Dirección Administrativa",
        max_length=255,
        null=True, blank=True,
        help_text="Calle principal e interseción,Numeracion, referencia"
    )

    company_type = models.CharField(
        "Tipo de sociedad",
        max_length=250,  # Cambié el max_length a 2, ya que en el catálogo se indica que son 2 caracteres
        choices=[
            ('01', 'Sociedades en General'),
            ('02', 'Sociedades que Cotizan sus Acciones en Bolsa de Valores'),
            ('03', 'Fideicomisos'),
            ('04', 'Sociedades sin Fines de Lucro'),
            ('05', 'Sector Económico Popular y Solidario'),
            ('06', 'Sector Financiero Popular y Solidario'),
            ('07', 'Fondos de Inversión, Complementarios y Otros'),
            ('08', 'Sucesión Indivisa'),
            ('09', 'Junta de Agua'),
            ('10', 'Fideicomisos y Similares Extranjeros'),
        ],
        null=True,
        blank=True,
        help_text="Tipo de sociedad según el catálogo del SRI."
    )
    fiscal_year = models.PositiveIntegerField(
        "Año fiscal",
        help_text="Año al que corresponde el reporte financiero. Ejemplo: 2025"
    )
    economic_activity = models.TextField(
        "Actividad económica",
        max_length=2000,
        null=True, blank=True,
        help_text="Código CIIU (Clasificación Internacional Industrial Uniforme) de la actividad económica principal de la empresa."
    )
    currency = models.CharField(
        "Moneda",
        max_length=10,
        default='USD',
        null=True, blank=True,
        help_text="Moneda utilizada en los estados financieros. Normalmente USD para Ecuador."
    )

    valor_unitario = models.DecimalField(
            max_digits=20,
            decimal_places=2,
            null=True,
            blank=True,
            help_text="Valor unitario por acciones"
        )

    monto_total = models.DecimalField(
            max_digits=20,
            decimal_places=2,
            null=True,
            blank=True,
            help_text="Escriba el monto total suscrito"
        )

    def __str__(self):
        return f"{self.company_name} - {self.fiscal_year}"

    class Meta:
        #unique_together = ('ruc', 'fiscal_year')
        verbose_name = "Balance Financiero (SCVS)"
        verbose_name_plural = "Balances Financieros (SCVS)"


class SCVS_ESF(models.Model):
    report = models.OneToOneField(SCVSFinancialReport, on_delete=models.CASCADE)

    c_1 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVO"
    )

    c_101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVO CORRIENTE"
    )

    c_10101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EFECTIVO Y EQUIVALENTES DE EFECTIVO"
    )

    c_1010101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAJA"
    )

    c_1010102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INSTITUCIONES FINANCIERAS PÚBLICAS"
    )

    c_1010103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INSTITUCIONES FINANCIERAS PRIVADAS"
    )

    c_10102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS"
    )

    c_1010201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_101020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RENTA VARIABLE"
    )

    c_10102010101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACCIONES Y PARTICIPACIONES"
    )

    c_10102010102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUOTAS DE FONDOS COLECTIVOS"
    )

    c_10102010103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE  TITULARIZACIÓN DE PARTICIPACIÓN"
    )

    c_10102010104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="UNIDADES DE PARTICIPACIÓN"
    )

    c_10102010105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES EN EL EXTERIOR"
    )

    c_10102010106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_101020102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RENTA FIJA"
    )

    c_10102010201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AVALES"
    )

    c_10102010202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BONOS DEL ESTADO"
    )

    c_10102010203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BONOS DE PRENDA"
    )

    c_10102010204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CÉDULAS HIPOTECARIAS"
    )

    c_10102010205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS FINANCIEROS"
    )

    c_10102010206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE INVERSIÓN"
    )

    c_10102010207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE TESORERÍA"
    )

    c_10102010208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE DEPÓSITO"
    )

    c_10102010209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUPONES"
    )

    c_10102010210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPÓSITOS A PLAZO"
    )

    c_10102010211 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LETRAS DE CAMBIO"
    )

    c_10102010212 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="NOTAS DE CRÉDITO"
    )

    c_10102010213 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES"
    )

    c_10102010214 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FACTURAS COMERCIALES NEGOCIABLES"
    )

    c_10102010215 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OVERNIGHTS"
    )

    c_10102010216 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES CONVERTIBLES EN ACCIONES"
    )

    c_10102010217 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAPEL COMERCIAL"
    )

    c_10102010218 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAGARÉS"
    )

    c_10102010219 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PÓLIZAS DE ACUMULACIÓN"
    )

    c_10102010220 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TÍTULOS DEL BANCO CENTRAL"
    )

    c_10102010221 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE TITULARIZACIÓN"
    )

    c_10102010222 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES EN EL EXTERIOR"
    )

    c_10102010223 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_101020103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERIVADOS"
    )

    c_10102010301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FORWARD"
    )

    c_10102010302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FUTUROS"
    )

    c_10102010303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OPCIONES"
    )

    c_10102010304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_1010202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_101020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RENTA VARIABLE"
    )

    c_10102020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACCIONES Y PARTICIPACIONES"
    )

    c_10102020102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUOTAS DE FONDOS COLECTIVOS"
    )

    c_10102020103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="UNIDADES DE PARTICIPACIÓN"
    )

    c_10102020104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE  TITULARIZACIÓN DE PARTICIPACIÓN"
    )

    c_10102020105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES EN EL EXTERIOR"
    )

    c_10102020106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_101020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RENTA FIJA"
    )

    c_10102020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AVALES"
    )

    c_10102020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BONOS DEL ESTADO"
    )

    c_10102020203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BONOS DE PRENDA"
    )

    c_10102020204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CÉDULAS HIPOTECARIAS"
    )

    c_10102020205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS FINANCIEROS"
    )

    c_10102020206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE INVERSIÓN"
    )

    c_10102020207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE TESORERÍA"
    )

    c_10102020208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE DEPÓSITO"
    )

    c_10102020209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUPONES"
    )

    c_10102020210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPÓSITOS A PLAZO"
    )

    c_10102020211 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LETRAS DE CAMBIO"
    )

    c_10102020212 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="NOTAS DE CRÉDITO"
    )

    c_10102020213 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES"
    )

    c_10102020214 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FACTURAS COMERCIALES NEGOCIABLES"
    )

    c_10102020215 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OVERNIGHTS"
    )

    c_10102020216 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES CONVERTIBLES EN ACCIONES"
    )

    c_10102020217 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAPEL COMERCIAL"
    )

    c_10102020218 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAGARÉS"
    )

    c_10102020219 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PÓLIZAS DE ACUMULACIÓN"
    )

    c_10102020220 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TÍTULOS DEL BANCO CENTRAL"
    )

    c_10102020221 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE TITULARIZACIÓN"
    )

    c_10102020222 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES EN EL EXTERIOR"
    )

    c_10102020223 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS INVERSIONES EN EL EXTERIOR"
    )

    c_1010203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS AL COSTO AMORTIZADO"
    )

    c_101020302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RENTA FIJA"
    )

    c_10102030201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AVALES"
    )

    c_10102030202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BONOS DEL ESTADO"
    )

    c_10102030203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BONOS DE PRENDA"
    )

    c_10102030204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CÉDULAS HIPOTECARIAS"
    )

    c_10102030205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS FINANCIEROS"
    )

    c_10102030206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE INVERSIÓN"
    )

    c_10102030207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE TESORERÍA"
    )

    c_10102030208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CERTIFICADOS DE DEPÓSITO"
    )

    c_10102030209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUPONES"
    )

    c_10102030210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPÓSITOS A PLAZO"
    )

    c_10102030211 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LETRAS DE CAMBIO"
    )

    c_10102030212 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="NOTAS DE CRÉDITO"
    )

    c_10102030213 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES"
    )

    c_10102030214 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FACTURAS COMERCIALES NEGOCIABLES"
    )

    c_10102030215 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OVERNIGHTS"
    )

    c_10102030216 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES CONVERTIBLES EN ACCIONES"
    )

    c_10102030217 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAPEL COMERCIAL"
    )

    c_10102030218 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAGARÉS"
    )

    c_10102030219 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PÓLIZAS DE ACUMULACIÓN"
    )

    c_10102030220 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TÍTULOS DEL BANCO CENTRAL"
    )

    c_10102030221 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE TITULARIZACIÓN"
    )

    c_10102030222 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES EN EL EXTERIOR"
    )

    c_10102030223 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_1010204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVISIÓN POR DETERIORO DE ACTIVOS FINANCIEROS"
    )

    c_101020401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_101020402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS AL COSTO AMORTIZADO"
    )

    c_101020403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_1010205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEUDORES COMERCIALES Y OTRAS CUENTAS POR COBRAR NO RELACIONADOS"
    )

    c_101020501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DE ACTIVIDADES ORDINARIAS QUE GENEREN INTERESES"
    )

    c_10102050101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS A COBRAR  A CLIENTES"
    )

    c_10102050102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS A COBRAR  A TERCEROS"
    )

    c_101020502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DE ACTIVIDADES ORDINARIAS QUE NO GENEREN INTERESES"
    )

    c_10102050201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS A COBRAR  A CLIENTES"
    )

    c_10102050202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS A COBRAR  A TERCEROS"
    )

    c_10102050203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS POR COBRAR AL ORIGINADOR"
    )

    c_10102050204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES POR OPERACIONES  BURSÁTILES"
    )

    c_10102050207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CONTRATO DE UNDERWRITING"
    )

    c_10102050208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR  ADMINISTRACIÓN Y MANEJO DE PORTAFOLIOS DE TERCEROS"
    )

    c_10102050209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ADMINISTRACIÓN Y MANEJO DE FONDOS ADMINISTRADOS"
    )

    c_10102050210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ADMINISTRACIÓN Y MANEJO DE NEGOCIOS FIDUCIARIOS"
    )

    c_10102050211 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CUSTODIA Y CONSERVACIÓN DE VALORES MATERIALIZADOS"
    )

    c_10102050212 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CUSTODIA Y CONSERVACIÓN DE VALORES DESMATERIALIZADOS"
    )

    c_10102050213 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR MANEJO DE LIBRO DE ACCIONES Y ACCIONISTAS"
    )

    c_10102050214 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ASESORÍA"
    )

    c_10102050215 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DIVIDENDOS POR COBRAR"
    )

    c_10102050216 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES POR COBRAR"
    )

    c_10102050217 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEUDORES POR INTERMEDIACIÓN DE VALORES"
    )

    c_10102050218 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPO A COMITENTES"
    )

    c_10102050219 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPO A CONSTRUCTOR POR AVANCE DE OBRA"
    )

    c_10102050220 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHOS POR COMPROMISO DE RECOMPRA"
    )

    c_10102050221 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS CUENTAS POR COBRAR NO RELACIONADAS"
    )

    c_1010206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DOCUMENTOS Y CUENTAS POR COBRAR RELACIONADOS"
    )

    c_101020601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COBRAR A ACCIONISTAS"
    )

    c_101020602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COBRAR A COMPAÑÍAS RELACIONADAS"
    )

    c_101020603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COBRAR A CLIENTES"
    )

    c_101020604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS CUENTAS POR COBRAR RELACIONADAS"
    )

    c_1010207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVISIÓN POR CUENTAS INCOBRABLES Y DETERIORO"
    )

    c_10103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS"
    )

    c_1010301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS DE MATERIA PRIMA"
    )

    c_1010302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS DE PRODUCTOS EN PROCESO"
    )

    c_1010303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS DE SUMINISTROS O MATERIALES A SER CONSUMIDOS EN EL PROCESO DE PRODUCCION"
    )

    c_1010304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS DE SUMINISTROS O MATERIALES A SER CONSUMIDOS EN LA PRESTACION DEL SERVICIO"
    )

    c_1010305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS DE PROD. TERM. Y MERCAD. EN ALMACÉN - PRODUCIDO POR LA COMPAÑÍA"
    )

    c_1010306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS DE PROD. TERM. Y MERCAD. EN ALMACÉN - COMPRADO A  TERCEROS"
    )

    c_1010307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MERCADERÍAS EN TRÁNSITO"
    )

    c_1010308 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBRAS EN CONSTRUCCION"
    )

    c_1010309 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBRAS TERMINADAS"
    )

    c_1010310 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MATERIALES O BIENES PARA LA CONSTRUCCION"
    )

    c_1010311 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS REPUESTOS, HERRAMIENTAS Y ACCESORIOS"
    )

    c_1010312 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS INVENTARIOS"
    )

    c_1010313 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) PROVISIÓN POR VALOR NETO DE REALIZACIÓN Y OTRAS PERDIDAS EN INVENTARIO"
    )

    c_10104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SERVICIOS Y OTROS PAGOS ANTICIPADOS"
    )

    c_1010401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SEGUROS PAGADOS POR ANTICIPADO"
    )

    c_1010402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ARRIENDOS PAGADOS POR ANTICIPADO"
    )

    c_1010403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPOS A PROVEEDORES"
    )

    c_1010404 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ANTICIPOS ENTREGADOS"
    )

    c_10105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS POR IMPUESTOS CORRIENTES"
    )

    c_1010501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CRÉDITO TRIBUTARIO A FAVOR DE LA EMPRESA (IVA)"
    )

    c_1010502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CRÉDITO TRIBUTARIO A FAVOR DE LA EMPRESA ( I. R.)"
    )

    c_1010503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPO DE IMPUESTO A LA RENTA"
    )

    c_10106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS CORRIENTES MANTENIDOS PARA LA VENTA Y OPERACIONES DISCONTINUADAS"
    )

    c_10107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CONSTRUCCIONES EN PROCESO (NIC 11 Y SECC.23 PYMES)"
    )

    c_10108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS CORRIENTES"
    )

    c_102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS NO CORRIENTES"
    )

    c_10201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_1020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TERRENOS"
    )

    c_1020102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EDIFICIOS"
    )

    c_1020103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CONSTRUCCIONES EN CURSO"
    )

    c_1020104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INSTALACIONES"
    )

    c_1020105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MUEBLES Y ENSERES"
    )

    c_1020106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MAQUINARIA Y EQUIPO"
    )

    c_1020107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="NAVES, AEREONAVES, BARCAZAS Y SIMILARES"
    )

    c_1020108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EQUIPO DE COMPUTACIÓN"
    )

    c_1020109 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VEHÍCULOS, EQUIPOS DE TRASPORTE Y EQUIPO CAMINERO MÓVIL"
    )

    c_1020110 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_1020111 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="REPUESTOS Y HERRAMIENTAS"
    )

    c_1020112 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DEPRECIACIÓN ACUMULADA PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_1020113 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DETERIORO  ACUMULADO DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_1020114 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS DE EXPLORACION Y EXPLOTACION"
    )

    c_102011401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS DE EXPLORACION Y EXPLOTACION"
    )

    c_102011402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) AMORTIZACION ACUMULADA DE ACTIVOS DE EXPLORACIÓN Y EXPLOTACIÓN"
    )

    c_102011403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DETERIORO  ACUMULADO DE ACTIVOS DE EXPLORACIÓN Y EXPLOTACIÓN"
    )

    c_10202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES DE INVERSIÓN"
    )

    c_1020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TERRENOS"
    )

    c_102020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TERRENOS"
    )

    c_102020102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHOS DE USO SOBRE TERRENOS SUBARRENDADOS"
    )

    c_1020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EDIFICIOS"
    )

    c_102020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EDIFICIOS"
    )

    c_102020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHOS DE USO SOBRE EDIFICIOS SUBARRENDADOS"
    )

    c_1020203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DEPRECIACION ACUMULADA DE PROPIEDADES DE INVERSIÓN"
    )

    c_1020204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DETERIORO ACUMULADO DE PROPIEDADES DE INVERSIÓN"
    )

    c_10203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS BIOLOGICOS"
    )

    c_1020301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANIMALES VIVOS EN CRECIMIENTO"
    )

    c_1020302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANIMALES VIVOS EN PRODUCCION"
    )

    c_1020303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PLANTAS EN CRECIMIENTO"
    )

    c_1020304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PLANTAS EN PRODUCCION"
    )

    c_1020305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DEPRECIACION ACUMULADA DE ACTIVOS BIOLÓGICOS"
    )

    c_1020306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DETERIORO ACUMULADO DE ACTIVOS BIOLOGÍCOS"
    )

    c_10204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVO INTANGIBLE"
    )

    c_1020401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PLUSVALÍAS"
    )

    c_1020402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MARCAS, PATENTES, DERECHOS DE LLAVE , CUOTAS PATRIMONIALES Y OTROS SIMILARES"
    )

    c_1020403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CONCESIONES Y LICENCIAS"
    )

    c_1020404 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS DE EXPLORACION Y EXPLOTACION"
    )

    c_1020405 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) AMORTIZACIÓN ACUMULADA DE ACTIVOS INTANGIBLE"
    )

    c_1020406 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DETERIORO ACUMULADO DE ACTIVO INTANGIBLE"
    )

    c_1020407 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS INTANGIBLES"
    )

    c_10205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS POR IMPUESTOS DIFERIDOS"
    )

    c_10206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS NO CORRIENTES"
    )

    c_1020601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_1020602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) PROVISION POR DETERIORO DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_1020603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A COSTO AMORTIZADO"
    )

    c_1020604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) PROVISIÓN POR DETERIORO DE ACTIVOS FINANCIEROS A COSTO AMORTIZADO"
    )

    c_1020605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_1020606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-)PROVISIÓN POR DETERIORO DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_10207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHO DE USO POR ACTIVOS ARRENDADOS"
    )

    c_1020701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DEPRECIACIÓN ACUMULADA DE ACTIVOS PROVENIENTES POR DERECHOS DE USO"
    )

    c_1020702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DETERIORO ACUMULADO DE ACTIVOS PROVENIENTES POR DERECHOS DE USO"
    )

    c_1020703 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHO DE USO POR ACTIVOS ARRENDADOS"
    )

    c_10208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS NO CORRIENTES"
    )

    c_1020801 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHOS FIDUCIARIOS"
    )

    c_1020802 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPÓSITOS EN GARANTÍA"
    )

    c_1020803 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPÓSITOS EN GARANTÍA POR OPERACIONES BURSÁTILES"
    )

    c_1020805 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACCIONES DEL DEPÓSITO CENTRALIZADO DE VALORES"
    )

    c_1020806 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES SUBSIDIARIAS"
    )

    c_1020807 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES ASOCIADAS"
    )

    c_1020808 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVERSIONES NEGOCIOS CONJUNTOS"
    )

    c_1020809 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS INVERSIONES"
    )

    c_1020810 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) PROVISIÓN VALUACIÓN DE INVERSIONES"
    )

    c_1020811 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS NO CORRIENTES"
    )

    c_10209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DOCUMENTOS Y CUENTAS POR COBRAR NO RELACIONADOS"
    )

    c_1020901 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS A COBRAR  A CLIENTES"
    )

    c_1020902 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS A COBRAR  A TERCEROS"
    )

    c_1020903 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS CUENTAS POR COBRAR NO RELACIONADAS"
    )

    c_10210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DOCUMENTOS Y CUENTAS POR COBRAR RELACIONADOS"
    )

    c_1021001 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COBRAR A ACCIONISTAS"
    )

    c_1021002 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COBRAR A COMPAÑÍAS RELACIONADAS"
    )

    c_1021003 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COBRAR A CLIENTES"
    )

    c_1021004 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS CUENTAS POR COBRAR RELACIONADAS"
    )

    c_2 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVO"
    )

    c_201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVO CORRIENTE"
    )

    c_20101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_20102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVOS POR CONTRATOS DE ARRENDAMIENTO"
    )

    c_20103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS POR PAGAR"
    )

    c_2010301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_201030101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS"
    )

    c_201030102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_201030103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS"
    )

    c_2010302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_201030201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS"
    )

    c_201030202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_201030203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS"
    )

    c_20104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES CON INSTITUCIONES FINANCIERAS"
    )

    c_2010401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_2010402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_20105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVISIONES"
    )

    c_2010501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_2010502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_20106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PORCIÓN CORRIENTE DE VALORES EMITIDOS"
    )

    c_2010601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES"
    )

    c_2010602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAPEL COMERCIAL"
    )

    c_2010603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE TITULARIZACIÓN"
    )

    c_2010604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_2010605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES POR PAGAR"
    )

    c_20107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS OBLIGACIONES CORRIENTES"
    )

    c_2010701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CON LA ADMINISTRACIÓN TRIBUTARIA"
    )

    c_2010702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="IMPUESTO A LA RENTA POR PAGAR DEL EJERCICIO"
    )

    c_2010703 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CON EL IESS"
    )

    c_2010704 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR BENEFICIOS DE LEY A EMPLEADOS"
    )

    c_2010705 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PARTICIPACIÓN TRABAJADORES POR PAGAR DEL EJERCICIO"
    )

    c_2010706 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DIVIDENDOS POR PAGAR"
    )

    c_2010707 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_20108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS POR PAGAR A RELACIONADAS"
    )

    c_2010801 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_201080101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE ACCIONISTAS"
    )

    c_201080102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_201080103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_201080104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_2010802 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_201080201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE ACCIONISTAS"
    )

    c_201080202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_201080203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_201080204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_20109 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS PASIVOS FINANCIEROS"
    )

    c_20110 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPOS"
    )

    c_2011001 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPOS DE CLIENTES"
    )

    c_2011002 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ANTICIPOS RECIBIDOS"
    )

    c_20111 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVOS DIRECTAMENTE ASOCIADOS CON LOS ACTIVOS NO CORRIENTES Y OPERACIONES DISCONTINUADAS"
    )

    c_20112 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PORCION CORRIENTE DE PROVISIONES POR BENEFICIOS A EMPLEADOS"
    )

    c_2011201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="JUBILACION PATRONAL"
    )

    c_2011202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS BENEFICIOS PARA LOS EMPLEADOS"
    )

    c_20113 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS PASIVOS CORRIENTES"
    )

    c_2011301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES POR PAGAR"
    )

    c_2011302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR OPERACIONES BURSÁTILES"
    )

    c_2011303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CUSTODIA"
    )

    c_2011304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ADMINISTRACIÓN"
    )

    c_2011305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS COMISIONES"
    )

    c_2011306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SANCIONES Y MULTAS"
    )

    c_2011307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INDEMNIZACIONES"
    )

    c_2011308 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES JUDICIALES"
    )

    c_2011309 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACREEDORES POR INTERMEDIACIÓN"
    )

    c_2011310 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIÓN POR COMPROMISO DE RECOMPRA"
    )

    c_2011311 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CONTRATOS DE UNDERWRITING"
    )

    c_2011312 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_20114 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVOS FINANCIEROS AL COSTO AMORTIZADO"
    )

    c_202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVO NO CORRIENTE"
    )

    c_20201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVOS POR CONTRATOS DE ARRENDAMIENTO"
    )

    c_20202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS Y DOCUMENTOS POR PAGAR"
    )

    c_2020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_202020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS"
    )

    c_202020102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_202020103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS"
    )

    c_2020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_202020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS"
    )

    c_202020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_202020203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS"
    )

    c_20203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES CON INSTITUCIONES FINANCIERAS"
    )

    c_2020301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_2020302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_20204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS POR PAGAR A RELACIONADAS"
    )

    c_2020401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LOCALES"
    )

    c_202040101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE ACCIONISTAS"
    )

    c_202040102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_202040103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_202040104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_2020402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEL EXTERIOR"
    )

    c_202040201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE ACCIONISTAS"
    )

    c_202040202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_202040203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVEEDORES"
    )

    c_202040204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_20205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PORCIÓN NO CORRIENTE DE VALORES EMITIDOS"
    )

    c_2020501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OBLIGACIONES"
    )

    c_2020502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PAPEL COMERCIAL"
    )

    c_2020503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALORES DE TITULARIZACIÓN"
    )

    c_2020504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_2020505 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES POR PAGAR"
    )

    c_20206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPOS"
    )

    c_2020601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ANTICIPOS DE CLIENTES"
    )

    c_2020602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ANTICIPOS RECIBIDOS"
    )

    c_20207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROVISIONES POR BENEFICIOS A EMPLEADOS"
    )

    c_2020701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="JUBILACION PATRONAL"
    )

    c_2020702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS BENEFICIOS NO CORRIENTES PARA LOS EMPLEADOS"
    )

    c_20208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRAS PROVISIONES"
    )

    c_20209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVO DIFERIDO"
    )

    c_2020901 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS DIFERIDOS"
    )

    c_2020902 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PASIVOS POR IMPUESTOS DIFERIDOS"
    )

    c_20210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS PASIVOS NO CORRIENTES"
    )

    c_3 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PATRIMONIO NETO"
    )

    c_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PATRIMONIO NETO ATRIBUIBLE A LOS PROPIETARIOS DE LA CONTROLADORA"
    )

    c_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAPITAL"
    )

    c_30101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAPITAL SUSCRITO O  ASIGNADO"
    )

    c_30102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) CAPITAL SUSCRITO NO PAGADO, ACCIONES EN TESORERÍA"
    )

    c_30103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FONDO PATRIMONIAL"
    )

    c_30104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PATRIMONIO DE LOS NEGOCIOS FIDUCIARIOS"
    )

    c_30105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PATRIMONIO DE LOS FONDOS DE INVERSIÓN"
    )

    c_3010501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PATRIMONIO DEL FONDO ADMINISTRADO"
    )

    c_3010502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PATRIMONIO DEL FONDO COLECTIVO"
    )

    c_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESERVAS"
    )

    c_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESERVA LEGAL"
    )

    c_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS RESULTADOS INTEGRALES"
    )

    c_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS SUPERAVIT POR REVALUACION"
    )

    c_306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESULTADOS ACUMULADOS"
    )

    c_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIAS ACUMULADAS"
    )

    c_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) PÉRDIDAS ACUMULADAS"
    )

    c_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESERVA DE CAPITAL"
    )

    c_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESERVA POR DONACIONES"
    )

    c_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESERVA POR VALUACIÓN"
    )

    c_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESULTADOS DEL EJERCICIO"
    )

    c_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA NETA DEL PERIODO"
    )

    c_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) PÉRDIDA NETA DEL PERIODO"
    )

    c_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PARTICIPACIÓN CONTROLADORA"
    )


    # =========================
    # METADATA
    # =========================
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    class Meta:
        #unique_together = ('ruc', 'fiscal_year')
        verbose_name = "Estado Situación Financiera (ESF)"
        verbose_name_plural = "Estados de Situación Financiera (ESF)"

    def __str__(self):
        return f"Activo:${self.c_1}, Pasivo: ${self.c_2}, Patrimonio: ${self.c_3}"




    def _D(self, v):
        return v if v is not None else Decimal("0.00")

    # =========================
    # 🟢 ACTIVOS CORRIENTES
    # =========================
    def calc_activos_corrientes(self):
        return sum([
            self._D(self.c_101),
            self._D(self.c_10101),
            self._D(self.c_1010101),
            self._D(self.c_1010102),
            self._D(self.c_1010103),
            self._D(self.c_10102),
            self._D(self.c_1010201),
            self._D(self.c_101020101),
            self._D(self.c_10102010101),
            self._D(self.c_10102010102),
            self._D(self.c_10102010103),
            self._D(self.c_10102010104),
            self._D(self.c_10102010105),
            self._D(self.c_10102010106),
            self._D(self.c_101020102),
            self._D(self.c_10102010201),
            self._D(self.c_10102010202),
            self._D(self.c_10102010203),
            self._D(self.c_10102010204),
            self._D(self.c_10102010205),
            self._D(self.c_10102010206),
            self._D(self.c_10102010207),
            self._D(self.c_10102010208),
            self._D(self.c_10102010209),
            self._D(self.c_10102010210),
            self._D(self.c_10102010211),
            self._D(self.c_10102010212),
            self._D(self.c_10102010213),
            self._D(self.c_10102010214),
            self._D(self.c_10102010215),
            self._D(self.c_10102010216),
            self._D(self.c_10102010217),
            self._D(self.c_10102010218),
            self._D(self.c_10102010219),
            self._D(self.c_10102010220),
            self._D(self.c_10102010221),
            self._D(self.c_10102010222),
            self._D(self.c_10102010223),
            self._D(self.c_101020103),
            self._D(self.c_10102010301),
            self._D(self.c_10102010302),
            self._D(self.c_10102010303),
            self._D(self.c_10102010304),
            self._D(self.c_1010202),
            self._D(self.c_101020201),
            self._D(self.c_10102020101),
            self._D(self.c_10102020102),
            self._D(self.c_10102020103),
            self._D(self.c_10102020104),
            self._D(self.c_10102020105),
            self._D(self.c_10102020106),
            self._D(self.c_101020202),
            self._D(self.c_10102020201),
            self._D(self.c_10102020202),
            self._D(self.c_10102020203),
            self._D(self.c_10102020204),
            self._D(self.c_10102020205),
            self._D(self.c_10102020206),
            self._D(self.c_10102020207),
            self._D(self.c_10102020208),
            self._D(self.c_10102020209),
            self._D(self.c_10102020210),
            self._D(self.c_10102020211),
            self._D(self.c_10102020212),
            self._D(self.c_10102020213),
            self._D(self.c_10102020214),
            self._D(self.c_10102020215),
            self._D(self.c_10102020216),
            self._D(self.c_10102020217),
            self._D(self.c_10102020218),
            self._D(self.c_10102020219),
            self._D(self.c_10102020220),
            self._D(self.c_10102020221),
            self._D(self.c_10102020222),
            self._D(self.c_10102020223),
            self._D(self.c_1010203),
            self._D(self.c_101020302),
            self._D(self.c_10102030201),
            self._D(self.c_10102030202),
            self._D(self.c_10102030203),
            self._D(self.c_10102030204),
            self._D(self.c_10102030205),
            self._D(self.c_10102030206),
            self._D(self.c_10102030207),
            self._D(self.c_10102030208),
            self._D(self.c_10102030209),
            self._D(self.c_10102030210),
            self._D(self.c_10102030211),
            self._D(self.c_10102030212),
            self._D(self.c_10102030213),
            self._D(self.c_10102030214),
            self._D(self.c_10102030215),
            self._D(self.c_10102030216),
            self._D(self.c_10102030217),
            self._D(self.c_10102030218),
            self._D(self.c_10102030219),
            self._D(self.c_10102030220),
            self._D(self.c_10102030221),
            self._D(self.c_10102030222),
            self._D(self.c_10102030223),
            self._D(self.c_1010204),
            self._D(self.c_101020401),
            self._D(self.c_101020402),
            self._D(self.c_101020403),
            self._D(self.c_1010205),
            self._D(self.c_101020501),
            self._D(self.c_10102050101),
            self._D(self.c_10102050102),
            self._D(self.c_101020502),
            self._D(self.c_10102050201),
            self._D(self.c_10102050202),
            self._D(self.c_10102050203),
            self._D(self.c_10102050204),
            self._D(self.c_10102050207),
            self._D(self.c_10102050208),
            self._D(self.c_10102050209),
            self._D(self.c_10102050210),
            self._D(self.c_10102050211),
            self._D(self.c_10102050212),
            self._D(self.c_10102050213),
            self._D(self.c_10102050214),
            self._D(self.c_10102050215),
            self._D(self.c_10102050216),
            self._D(self.c_10102050217),
            self._D(self.c_10102050218),
            self._D(self.c_10102050219),
            self._D(self.c_10102050220),
            self._D(self.c_10102050221),
            self._D(self.c_1010206),
            self._D(self.c_101020601),
            self._D(self.c_101020602),
            self._D(self.c_101020603),
            self._D(self.c_101020604),
            self._D(self.c_1010207),
            self._D(self.c_10103),
            self._D(self.c_1010301),
            self._D(self.c_1010302),
            self._D(self.c_1010303),
            self._D(self.c_1010304),
            self._D(self.c_1010305),
            self._D(self.c_1010306),
            self._D(self.c_1010307),
            self._D(self.c_1010308),
            self._D(self.c_1010309),
            self._D(self.c_1010310),
            self._D(self.c_1010311),
            self._D(self.c_1010312),
            self._D(self.c_1010313),
            self._D(self.c_10104),
            self._D(self.c_1010401),
            self._D(self.c_1010402),
            self._D(self.c_1010403),
            self._D(self.c_1010404),
            self._D(self.c_10105),
            self._D(self.c_1010501),
            self._D(self.c_1010502),
            self._D(self.c_1010503),
            self._D(self.c_10106),
            self._D(self.c_10107),
            self._D(self.c_10108),
        ])

    # =========================
    # 🟢 ACTIVOS NO CORRIENTES
    # =========================
    def calc_activos_no_corrientes(self):
        return sum([
            self._D(self.c_102),
            self._D(self.c_10201),
            self._D(self.c_1020101),
            self._D(self.c_1020102),
            self._D(self.c_1020103),
            self._D(self.c_1020104),
            self._D(self.c_1020105),
            self._D(self.c_1020106),
            self._D(self.c_1020107),
            self._D(self.c_1020108),
            self._D(self.c_1020109),
            self._D(self.c_1020110),
            self._D(self.c_1020111),
            self._D(self.c_1020112),
            self._D(self.c_1020113),
            self._D(self.c_1020114),
            self._D(self.c_102011401),
            self._D(self.c_102011402),
            self._D(self.c_102011403),
            self._D(self.c_10202),
            self._D(self.c_1020201),
            self._D(self.c_102020101),
            self._D(self.c_102020102),
            self._D(self.c_1020202),
            self._D(self.c_102020201),
            self._D(self.c_102020202),
            self._D(self.c_1020203),
            self._D(self.c_1020204),
            self._D(self.c_10203),
            self._D(self.c_1020301),
            self._D(self.c_1020302),
            self._D(self.c_1020303),
            self._D(self.c_1020304),
            self._D(self.c_1020305),
            self._D(self.c_1020306),
            self._D(self.c_10204),
            self._D(self.c_1020401),
            self._D(self.c_1020402),
            self._D(self.c_1020403),
            self._D(self.c_1020404),
            self._D(self.c_1020405),
            self._D(self.c_1020406),
            self._D(self.c_1020407),
            self._D(self.c_10205),
            self._D(self.c_10206),
            self._D(self.c_1020601),
            self._D(self.c_1020602),
            self._D(self.c_1020603),
            self._D(self.c_1020604),
            self._D(self.c_1020605),
            self._D(self.c_1020606),
            self._D(self.c_10207),
            self._D(self.c_1020701),
            self._D(self.c_1020702),
            self._D(self.c_1020703),
            self._D(self.c_10208),
            self._D(self.c_1020801),
            self._D(self.c_1020802),
            self._D(self.c_1020803),
            self._D(self.c_1020805),
            self._D(self.c_1020806),
            self._D(self.c_1020807),
            self._D(self.c_1020808),
            self._D(self.c_1020809),
            self._D(self.c_1020810),
            self._D(self.c_1020811),
            self._D(self.c_10209),
            self._D(self.c_1020901),
            self._D(self.c_1020902),
            self._D(self.c_1020903),
            self._D(self.c_10210),
            self._D(self.c_1021001),
            self._D(self.c_1021002),
            self._D(self.c_1021003),
            self._D(self.c_1021004),
        ])

    # =========================
    # 🔴 PASIVOS
    # =========================
    def calc_pasivos(self):
        return self._D(self.c_2)

    # =========================
    # 🔴 PASIVOS CORRIENTES
    # =========================
    def calc_pasivos_corrientes(self):
        return sum([
            self._D(self.c_201),
            self._D(self.c_20101),
            self._D(self.c_20102),
            self._D(self.c_20103),
            self._D(self.c_2010301),
            self._D(self.c_201030101),
            self._D(self.c_201030102),
            self._D(self.c_201030103),
            self._D(self.c_2010302),
            self._D(self.c_201030201),
            self._D(self.c_201030202),
            self._D(self.c_201030203),
            self._D(self.c_20104),
            self._D(self.c_2010401),
            self._D(self.c_2010402),
            self._D(self.c_20105),
            self._D(self.c_2010501),
            self._D(self.c_2010502),
            self._D(self.c_20106),
            self._D(self.c_2010601),
            self._D(self.c_2010602),
            self._D(self.c_2010603),
            self._D(self.c_2010604),
            self._D(self.c_2010605),
            self._D(self.c_20107),
            self._D(self.c_2010701),
            self._D(self.c_2010702),
            self._D(self.c_2010703),
            self._D(self.c_2010704),
            self._D(self.c_2010705),
            self._D(self.c_2010706),
            self._D(self.c_2010707),
            self._D(self.c_20108),
            self._D(self.c_2010801),
            self._D(self.c_201080101),
            self._D(self.c_201080102),
            self._D(self.c_201080103),
            self._D(self.c_201080104),
            self._D(self.c_2010802),
            self._D(self.c_201080201),
            self._D(self.c_201080202),
            self._D(self.c_201080203),
            self._D(self.c_201080204),
            self._D(self.c_20109),
            self._D(self.c_20110),
            self._D(self.c_2011001),
            self._D(self.c_2011002),
            self._D(self.c_20111),
            self._D(self.c_20112),
            self._D(self.c_2011201),
            self._D(self.c_2011202),
            self._D(self.c_20113),
            self._D(self.c_2011301),
            self._D(self.c_2011302),
            self._D(self.c_2011303),
            self._D(self.c_2011304),
            self._D(self.c_2011305),
            self._D(self.c_2011306),
            self._D(self.c_2011307),
            self._D(self.c_2011308),
            self._D(self.c_2011309),
            self._D(self.c_2011310),
            self._D(self.c_2011311),
            self._D(self.c_2011312),
            self._D(self.c_20114),
        ])

    # =========================
    # 🔴 PASIVOS NO CORRIENTES
    # =========================
    def calc_pasivos_no_corrientes(self):
        return sum([
            self._D(self.c_202),
            self._D(self.c_20201),
            self._D(self.c_20202),
            self._D(self.c_2020201),
            self._D(self.c_202020101),
            self._D(self.c_202020102),
            self._D(self.c_202020103),
            self._D(self.c_2020202),
            self._D(self.c_202020201),
            self._D(self.c_202020202),
            self._D(self.c_202020203),
            self._D(self.c_20203),
            self._D(self.c_2020301),
            self._D(self.c_2020302),
            self._D(self.c_20204),
            self._D(self.c_2020401),
            self._D(self.c_202040101),
            self._D(self.c_202040102),
            self._D(self.c_202040103),
            self._D(self.c_202040104),
            self._D(self.c_2020402),
            self._D(self.c_202040201),
            self._D(self.c_202040202),
            self._D(self.c_202040203),
            self._D(self.c_202040204),
            self._D(self.c_20205),
            self._D(self.c_2020501),
            self._D(self.c_2020502),
            self._D(self.c_2020503),
            self._D(self.c_2020504),
            self._D(self.c_2020505),
            self._D(self.c_20206),
            self._D(self.c_2020601),
            self._D(self.c_2020602),
            self._D(self.c_20207),
            self._D(self.c_2020701),
            self._D(self.c_2020702),
            self._D(self.c_20208),
            self._D(self.c_20209),
            self._D(self.c_2020901),
            self._D(self.c_2020902),
            self._D(self.c_20210),
        ])

    # =========================
    # 🔵 PATRIMONIO
    # =========================
    def calc_patrimonio(self):
        return sum([
            self._D(self.c_3),
            self._D(self.c_30),
            self._D(self.c_301),
            self._D(self.c_30101),
            self._D(self.c_30102),
            self._D(self.c_30103),
            self._D(self.c_30104),
            self._D(self.c_30105),
            self._D(self.c_3010501),
            self._D(self.c_3010502),
            self._D(self.c_302),
            self._D(self.c_303),
            self._D(self.c_304),
            self._D(self.c_30401),
            self._D(self.c_30402),
            self._D(self.c_305),
            self._D(self.c_30501),
            self._D(self.c_30502),
            self._D(self.c_30503),
            self._D(self.c_30504),
            self._D(self.c_306),
            self._D(self.c_30601),
            self._D(self.c_30602),
            self._D(self.c_30603),
            self._D(self.c_30604),
            self._D(self.c_30605),
            self._D(self.c_30606),
            self._D(self.c_30607),
            self._D(self.c_307),
            self._D(self.c_30701),
            self._D(self.c_30702),
            self._D(self.c_31),
        ])

    # =========================
    # ⚖️ VALIDACIÓN AUDITOR SCVS
    # =========================
    def validar_balance_general(self):
        activos = self.calc_activos_corrientes() + self.calc_activos_no_corrientes()
        pasivos = self.calc_pasivos() + self.calc_pasivos_corrientes() + self.calc_pasivos_no_corrientes()
        patrimonio = self.calc_patrimonio()

        diferencia = activos - (pasivos + patrimonio)

        return {
            "activos": str(activos),
            "pasivos": str(pasivos),
            "patrimonio": str(patrimonio),
            "diferencia": str(diferencia),
            "cuadra": diferencia == Decimal("0.00"),
        }


    def clean(self):

        activos = (
            self.calc_activos_corrientes() +
            self.calc_activos_no_corrientes()
        )

        pasivos = (
            self.calc_pasivos() +
            self.calc_pasivos_corrientes() +
            self.calc_pasivos_no_corrientes()
        )

        patrimonio = self.calc_patrimonio()

        validar_cuadre_scvs(activos, pasivos, patrimonio)

    # =========================
    # 💾 SAVE (FORZAR VALIDACIÓN)
    # =========================
    def save(self, *args, **kwargs):

        # 🔥 fuerza ejecución de clean()
        self.full_clean()

        # =========================
        # 🟢 ACTIVOS
        # =========================
        self.c_1 = (
            self.calc_activos_corrientes() +
            self.calc_activos_no_corrientes()
        )

        # =========================
        # 🔴 PASIVOS
        # =========================
        self.c_2 = (
            self.calc_pasivos() +
            self.calc_pasivos_corrientes() +
            self.calc_pasivos_no_corrientes()
        )

        # =========================
        # 🔵 PATRIMONIO
        # =========================
        self.c_3 = self.calc_patrimonio()

        super().save(*args, **kwargs)


class SCVS_EIR(models.Model):
    report = models.OneToOneField(SCVSFinancialReport, on_delete=models.CASCADE)

    c_401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS DE ACTIVIDADES ORDINARIAS"
    )

    c_40101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VENTA DE BIENES"
    )

    c_40102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PRESTACION DE SERVICIOS"
    )

    c_4010201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS POR ASESORÍA"
    )

    c_4010202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS POR ESTRUCTURACIÓN DE OFERTA PÚBLICA DE VALORES"
    )

    c_4010203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS POR ESTRUCTURACIÓN DE NEGOCIOS FIDUCIARIOS"
    )

    c_4010204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_40103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CONTRATOS DE CONSTRUCCION"
    )

    c_40104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUBVENCIONES DEL GOBIERNO"
    )

    c_40105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="REGALÍAS"
    )

    c_40106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES"
    )

    c_4010601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES GENERADOS POR VENTAS A CREDITO"
    )

    c_4010602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES Y RENDIMIENTOS FINANCIEROS"
    )

    c_4010603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS INTERESES GENERADOS"
    )

    c_40107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DIVIDENDOS"
    )

    c_40108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA POR MEDICION A VALOR RAZONABLE  DE ACTIVOS BIOLOGICOS"
    )

    c_40109 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS POR COMISIONES, PRESTACIÓN DE SERVICIOS, CUSTODIA, REGISTRO, COMPENSACIÓN Y LIQUIDACIÓN"
    )

    c_4010901 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES GANADAS POR INTERMEDIACIÓN DE VALORES"
    )

    c_401090101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR OPERACIONES BURSATILES"
    )

    c_401090103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CONTRATOS DE UNDERWRITING"
    )

    c_401090104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COMISIÓN EN OPERACIONES"
    )

    c_401090105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR INSCRIPCIONES"
    )

    c_401090106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR MANTENIMIENTO DE INSCRIPCIÓN"
    )

    c_4010902 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR PRESTACIÓN DE SERVICIOS DE ADMINISTRACIÓN Y MANEJO"
    )

    c_401090201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PORTAFOLIO DE TERCEROS"
    )

    c_401090202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FONDOS ADMINISTRADOS"
    )

    c_401090203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FONDOS COLECTIVOS"
    )

    c_401090204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TITULARIZACIÓN"
    )

    c_401090205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FIDEICOMISOS MERCANTILES"
    )

    c_401090206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ENCARGOS FIDUCIARIOS"
    )

    c_401090207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CALIFICACION DE RIESGO"
    )

    c_401090208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR REPRESENTACION DE OBLIGACIONISTAS"
    )

    c_4010903 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUSTODIA, REGISTRO, COMPENSACIÓN Y LIQUIDACIÓN"
    )

    c_401090301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUSTODIA VALORES MATERIALIZADOS"
    )

    c_401090302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUSTODIA VALORES DESMATERIALIZADOS"
    )

    c_401090303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMPENSACIÓN Y LIQUIDACIÓN DE VALORES"
    )

    c_401090304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_40110 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS  FINANCIEROS"
    )

    c_4011001 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DIVIDENDOS"
    )

    c_4011002 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES FINANCIEROS"
    )

    c_4011003 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA EN INVERSIONES EN ASOCIADAS / SUBSIDIARIAS Y OTRAS"
    )

    c_4011004 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALUACION DE INSTRUMENTOS FINANCIEROS A VALOR RAZONABLE CON CAMBIO EN RESULTADOS"
    )

    c_4011005 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA EN VENTA DE TITULOS VALORES"
    )

    c_4011006 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS INGRESOS  FINANCIEROS"
    )

    c_40112 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DESCUENTO EN VENTAS"
    )

    c_40113 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) DEVOLUCIONES EN VENTAS"
    )

    c_40114 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) BONIFICACIÓN EN PRODUCTO"
    )

    c_40115 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) OTRAS REBAJAS COMERCIALES"
    )

    c_40116 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="UTILIDAD EN CAMBIO"
    )

    c_402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA BRUTA"
    )

    c_403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS INGRESOS"
    )

    c_40301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA EN VENTA DE PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_40302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA EN VENTA DE ACTIVOS BIOLÓGICOS"
    )

    c_40303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COSTO DE VENTAS Y PRODUCCIÓN"
    )

    c_50101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MATERIALES UTILIZADOS O PRODUCTOS VENDIDOS"
    )

    c_5010101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) INVENTARIO INICIAL DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) COMPRAS NETAS LOCALES DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) IMPORTACIONES DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) INVENTARIO FINAL DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) INVENTARIO INICIAL DE MATERIA PRIMA"
    )

    c_5010106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) COMPRAS NETAS LOCALES DE MATERIA PRIMA"
    )

    c_5010107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) IMPORTACIONES DE MATERIA PRIMA"
    )

    c_5010108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) INVENTARIO FINAL DE MATERIA PRIMA"
    )

    c_5010109 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) INVENTARIO INICIAL DE PRODUCTOS EN PROCESO"
    )

    c_5010110 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) INVENTARIO FINAL DE PRODUCTOS EN PROCESO"
    )

    c_5010111 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) INVENTARIO INICIAL PRODUCTOS TERMINADOS"
    )

    c_5010112 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) INVENTARIO FINAL DE PRODUCTOS TERMINADOS"
    )

    c_50102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) MANO DE OBRA DIRECTA"
    )

    c_5010201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUELDOS Y BENEFICIOS SOCIALES"
    )

    c_5010202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_50103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) MANO DE OBRA INDIRECTA"
    )

    c_5010301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUELDOS Y BENEFICIOS SOCIALES"
    )

    c_5010302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_50104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) OTROS COSTOS INDIRECTOS DE FABRICACION"
    )

    c_5010401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPRECIACIÓN PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_5010402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DETERIORO O PERDIDAS DE ACTIVOS BIOLOGICOS"
    )

    c_5010403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DETERIORO DE PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_5010404 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EFECTO VALOR NETO DE REALIZACION DE INVENTARIOS"
    )

    c_5010405 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO POR GARANTIAS EN VENTA DE PRODUCTOS O SERVICIOS"
    )

    c_5010406 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MANTENIMIENTO Y REPARACIONES"
    )

    c_5010407 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUMINISTROS MATERIALES Y REPUESTOS"
    )

    c_5010408 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS COSTOS DE PRODUCCIÓN"
    )

    c_50105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COSTOS DE CONTRATOS DE CONSTRUCCIONES"
    )

    c_5010501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COSTOS DE ACUERDO A PORCENTAJES O GRADOS DE TERMINACIÓN"
    )

    c_502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS"
    )

    c_50201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS DE VENTA"
    )

    c_5020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUELDOS, SALARIOS Y DEMÁS REMUNERACIONES"
    )

    c_5020102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="APORTES A LA SEGURIDAD SOCIAL (INCLUIDO FONDO DE RESERVA)"
    )

    c_5020103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BENEFICIOS SOCIALES E INDEMNIZACIONES"
    )

    c_5020104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_5020105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="HONORARIOS, COMISIONES Y DIETAS A PERSONAS NATURALES"
    )

    c_5020106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="REMUNERACIONES A OTROS TRABAJADORES AUTÓNOMOS"
    )

    c_5020107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="HONORARIOS A EXTRANJEROS POR SERVICIOS OCASIONALES"
    )

    c_5020108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MANTENIMIENTO Y REPARACIONES"
    )

    c_5020109 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ARRENDAMIENTO"
    )

    c_5020110 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES"
    )

    c_5020111 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROMOCIÓN Y PUBLICIDAD"
    )

    c_5020112 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMBUSTIBLES"
    )

    c_5020113 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LUBRICANTES"
    )

    c_5020114 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SEGUROS Y REASEGUROS (PRIMAS Y CESIONES)"
    )

    c_5020115 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TRANSPORTE"
    )

    c_5020116 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS DE GESTIÓN (AGASAJOS A ACCIONISTAS, TRABAJADORES Y CLIENTES)"
    )

    c_5020117 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS DE VIAJE"
    )

    c_5020118 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AGUA, ENERGÍA, LUZ, Y TELECOMUNICACIONES"
    )

    c_5020119 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="NOTARIOS Y REGISTRADORES DE LA PROPIEDAD O MERCANTILES"
    )

    c_5020120 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPRECIACIONES:"
    )

    c_502012001 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502012002 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES DE INVERSIÓN"
    )

    c_502012003 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS POR DERECHO DE USO"
    )

    c_5020121 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AMORTIZACIONES"
    )

    c_502012101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTANGIBLES"
    )

    c_502012102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS"
    )

    c_5020122 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO DETERIORO"
    )

    c_502012201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502012202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS"
    )

    c_502012203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INSTRUMENTOS FINANCIEROS"
    )

    c_502012204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTANGIBLES"
    )

    c_502012205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS POR COBRAR"
    )

    c_502012206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS"
    )

    c_502012207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHOS DE USO POR ACTIVOS ARRENDADOS"
    )

    c_5020123 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS POR CANTIDADES ANORMALES DE UTILIZACION EN EL PROCESO DE PRODUCCIÓN:"
    )

    c_502012301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MANO DE OBRA"
    )

    c_502012302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MATERIALES"
    )

    c_502012303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COSTOS DE PRODUCCION"
    )

    c_5020124 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO POR REESTRUCTURACION"
    )

    c_5020125 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALOR NETO DE REALIZACION DE INVENTARIOS"
    )

    c_5020126 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO IMPUESTO A LA RENTA (ACTIVOS Y PASIVOS DIFERIDOS)"
    )

    c_5020127 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUMINISTROS Y MATERIALES"
    )

    c_5020128 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS GASTOS"
    )

    c_50202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS ADMINISTRATIVOS"
    )

    c_5020201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUELDOS, SALARIOS Y DEMÁS REMUNERACIONES"
    )

    c_5020202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="APORTES A LA SEGURIDAD SOCIAL (INCLUIDO FONDO DE RESERVA)"
    )

    c_5020203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="BENEFICIOS SOCIALES E INDEMNIZACIONES"
    )

    c_5020204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_5020205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="HONORARIOS, COMISIONES Y DIETAS A PERSONAS NATURALES"
    )

    c_5020206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="REMUNERACIONES A OTROS TRABAJADORES AUTÓNOMOS"
    )

    c_5020207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="HONORARIOS A EXTRANJEROS POR SERVICIOS OCASIONALES"
    )

    c_5020208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MANTENIMIENTO Y REPARACIONES"
    )

    c_5020209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ARRENDAMIENTO"
    )

    c_5020210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES"
    )

    c_5020211 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROMOCIÓN Y PUBLICIDAD"
    )

    c_5020212 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMBUSTIBLES"
    )

    c_5020213 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="LUBRICANTES"
    )

    c_5020214 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SEGUROS Y REASEGUROS (PRIMAS Y CESIONES)"
    )

    c_5020215 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TRANSPORTE"
    )

    c_5020216 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS DE GESTIÓN (AGASAJOS A ACCIONISTAS, TRABAJADORES Y CLIENTES)"
    )

    c_5020217 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS DE VIAJE"
    )

    c_5020218 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AGUA, ENERGÍA, LUZ, Y TELECOMUNICACIONES"
    )

    c_5020219 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="NOTARIOS Y REGISTRADORES DE LA PROPIEDAD O MERCANTILES"
    )

    c_5020220 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="IMPUESTOS, CONTRIBUCIONES Y OTROS"
    )

    c_5020221 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DEPRECIACIONES"
    )

    c_502022101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502022102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES DE INVERSIÓN"
    )

    c_502022103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ACTIVOS POR DERECHO DE USO"
    )

    c_5020222 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AMORTIZACIONES"
    )

    c_502022201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTANGIBLES"
    )

    c_502022202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS"
    )

    c_5020223 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO DETERIORO:"
    )

    c_502022301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502022302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INVENTARIOS"
    )

    c_502022303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INSTRUMENTOS FINANCIEROS"
    )

    c_502022304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTANGIBLES"
    )

    c_502022305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUENTAS POR COBRAR"
    )

    c_502022306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS ACTIVOS"
    )

    c_502022307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DERECHOS DE USO POR ACTIVOS ARRENDADOS"
    )

    c_5020224 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS POR CANTIDADES ANORMALES DE UTILIZACION EN EL PROCESO DE PRODUCCIÓN"
    )

    c_502022401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MANO DE OBRA"
    )

    c_502022402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="MATERIALES"
    )

    c_502022403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COSTOS DE PRODUCCION"
    )

    c_5020225 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO POR REESTRUCTURACION"
    )

    c_5020226 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALOR NETO DE REALIZACION DE INVENTARIOS"
    )

    c_5020227 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTO IMPUESTO A LA RENTA (ACTIVOS Y PASIVOS DIFERIDOS)"
    )

    c_5020228 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SUMINISTROS Y MATERIALES"
    )

    c_5020229 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS GASTOS"
    )

    c_50203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS FINANCIEROS"
    )

    c_5020301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES"
    )

    c_502030101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES POR PRESTAMOS"
    )

    c_502030102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES POR ARRENDAMIENTOS"
    )

    c_502030103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INTERESES POR VALORES EMITIDOS"
    )

    c_502030104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS INTERESES"
    )

    c_5020302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES"
    )

    c_502030201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMISIONES PAGADAS POR INTERMEDIACIÓN DE VALORES:"
    )

    c_50203020101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR OPERACIONES BURSATILES"
    )

    c_50203020103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CONTRATOS DE UNDERWRITING"
    )

    c_50203020104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR COMISIÓN EN OPERACIONES"
    )

    c_50203020105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR INSCRIPCIONES"
    )

    c_50203020106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR MANTENIMIENTO DE INSCRIPCIÓN"
    )

    c_5020303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR PRESTACIÓN DE SERVICIOS DE ADMINISTRACIÓN Y MANEJO"
    )

    c_502030301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PORTAFOLIO DE TERCEROS"
    )

    c_502030302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FONDOS ADMINISTRADOS"
    )

    c_502030303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FONDOS COLECTIVOS"
    )

    c_502030304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="TITULARIZACIÓN"
    )

    c_502030305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FIDEICOMISOS MERCANTILES"
    )

    c_502030306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="ENCARGOS FIDUCIARIOS"
    )

    c_502030307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR CALIFICACION DE RIESGO"
    )

    c_502030308 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR REPRESENTACION DE OBLIGACIONISTAS"
    )

    c_5020304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUSTODIA, REGISTRO, COMPENSACIÓN Y LIQUIDACIÓN"
    )

    c_502030401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUSTODIA VALORES MATERIALIZADOS"
    )

    c_502030402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CUSTODIA VALORES DESMATERIALIZADOS"
    )

    c_502030403 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMPENSACIÓN Y LIQUIDACIÓN DE VALORES"
    )

    c_502030404 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_5020305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS POR SERVICIOS DE ASESORIA Y ESTRUCTURACION"
    )

    c_502030501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ASESORÍA"
    )

    c_502030502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ESTRUCTURACIÓN DE OFERTA PÚBLICA DE VALORES"
    )

    c_502030503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="POR ESTRUCTURACIÓN DE NEGOCIOS FIDUCIARIOS"
    )

    c_502030504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_5020306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS DE FINANCIAMIENTO DE ACTIVOS"
    )

    c_5020307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DIFERENCIA EN CAMBIO"
    )

    c_5020308 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALUACION DE INSTRUMENTOS FINANCIEROS A VALOR RAZONABLE CON CAMBIO EN RESULTADOS"
    )

    c_5020309 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PERDIDA EN VENTA DE TITULOS VALORES"
    )

    c_5020310 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PERDIDA EN VENTA DE PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_5020311 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PERDIDA EN VENTA DE ACTIVOS BIOLOGICOS"
    )

    c_5020312 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS GASTOS FINANCIEROS"
    )

    c_50204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS GASTOS"
    )

    c_5020401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PERDIDA EN INVERSIONES EN ASOCIADAS / SUBSIDIARIAS Y OTRAS"
    )

    c_5020402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS"
    )

    c_600 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) ANTES DE 15% A TRABAJADORES E IMPUESTO A LA RENTA DE OPERACIONES CONTINUADAS"
    )

    c_601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="15% PARTICIPACIÓN TRABAJADORES"
    )

    c_602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) ANTES DE IMPUESTOS"
    )

    c_603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="IMPUESTO A LA RENTA CAUSADO"
    )

    c_604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) DE OPERACIONES CONTINUADAS ANTES DEL IMPUESTO DIFERIDO"
    )

    c_605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(-) GASTO POR IMPUESTO DIFERIDO"
    )

    c_606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(+) INGRESO POR IMPUESTO DIFERIDO"
    )

    c_607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PERDIDA) DE OPERACIONES CONTINUADAS"
    )

    c_700 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INGRESOS POR OPERACIONES DISCONTINUADAS"
    )

    c_701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GASTOS POR OPERACIONES DISCONTINUADAS"
    )

    c_702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) ANTES DE 15% A TRABAJADORES E IMPUESTO A LA RENTA DE OPERACIONES DISCONTINUADAS"
    )

    c_703 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="15% PARTICIPACIÓN TRABAJADORES"
    )

    c_704 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) ANTES DE IMPUESTOS DE OPERACIONES DISCONTINUADAS"
    )

    c_705 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="IMPUESTO A LA RENTA CAUSADO"
    )

    c_706 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) DE OPERACIONES DISCONTINUADAS"
    )

    c_707 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) NETA DEL PERIODO"
    )

    c_800 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTRO RESULTADO INTEGRAL"
    )

    c_80001 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="COMPONENTES DEL OTRO RESULTADO INTEGRAL"
    )

    c_80002 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="DIFERENCIA DE CAMBIO POR CONVERSIÓN"
    )

    c_80003 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="VALUACIÓN DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIO EN OTRO RESULTADO INTEGRAL"
    )

    c_80004 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIAS POR REVALUACIÓN DE PROPIEDADES, PLANTA  Y EQUIPO"
    )

    c_80005 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIAS (PÉRDIDAS) ACTUARIALES POR PLANES DE BENEFICIOS DEFINIDOS"
    )

    c_80006 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="REVERSION DEL DETERIORO (PÉRDIDA POR DETERIORO) DE UN ACTIVO REVALUADO"
    )

    c_80007 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PARTICIPACION DE OTRO RESULTADO INTEGRAL DE ASOCIADAS"
    )

    c_80008 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="IMPUESTO SOBRE LAS GANANCIAS RELATIVO A OTRO RESULTADO INTEGRAL"
    )

    c_80009 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="OTROS (DETALLAR EN NOTAS)"
    )

    c_801 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="RESULTADO INTEGRAL TOTAL DEL AÑO"
    )

    c_80101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PROPIETARIOS DE LA CONTROLADORA"
    )

    c_80102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="PARTICIPACION NO CONTROLADORA (INFORMATIVO)"
    )


    def _D(self, v):
        return v if v is not None else Decimal("0.00")

    # =====================================================
    # 📊 INGRESOS
    # =====================================================
    def calc_c_401(self):
        return (
            self._D(self.c_40101) +

            self._D(self.c_40102) +
            self._D(self.c_4010201) +
            self._D(self.c_4010202) +
            self._D(self.c_4010203) +
            self._D(self.c_4010204) +

            self._D(self.c_40103) +
            self._D(self.c_40104) +
            self._D(self.c_40105) +

            self._D(self.c_40106) +
            self._D(self.c_4010601) +
            self._D(self.c_4010602) +
            self._D(self.c_4010603) +

            self._D(self.c_40107) +
            self._D(self.c_40108) +

            self._D(self.c_40109) +
            self._D(self.c_4010901) +
            self._D(self.c_401090101) +
            self._D(self.c_401090103) +
            self._D(self.c_401090104) +
            self._D(self.c_401090105) +
            self._D(self.c_401090106) +

            self._D(self.c_4010902) +
            self._D(self.c_401090201) +
            self._D(self.c_401090202) +
            self._D(self.c_401090203) +
            self._D(self.c_401090204) +
            self._D(self.c_401090205) +
            self._D(self.c_401090206) +
            self._D(self.c_401090207) +
            self._D(self.c_401090208) +

            self._D(self.c_4010903) +
            self._D(self.c_401090301) +
            self._D(self.c_401090302) +
            self._D(self.c_401090303) +
            self._D(self.c_401090304) +

            self._D(self.c_40110) +
            self._D(self.c_4011001) +
            self._D(self.c_4011002) +
            self._D(self.c_4011003) +
            self._D(self.c_4011004) +
            self._D(self.c_4011005) +
            self._D(self.c_4011006) +

            self._D(self.c_40112) +
            self._D(self.c_40113) +
            self._D(self.c_40114) +
            self._D(self.c_40115) -

            self._D(self.c_40116) +

            self._D(self.c_402) +
            self._D(self.c_403) +
            self._D(self.c_40301) +
            self._D(self.c_40302) +
            self._D(self.c_40303)
        )

    # =====================================================
    # 📉 COSTOS
    # =====================================================
    def calc_c_501(self):
        return (
            self._D(self.c_50101) +
            self._D(self.c_5010101) +
            self._D(self.c_5010102) +
            self._D(self.c_5010103) +
            self._D(self.c_5010104) +
            self._D(self.c_5010105) +
            self._D(self.c_5010106) +
            self._D(self.c_5010107) +
            self._D(self.c_5010108) +
            self._D(self.c_5010109) +
            self._D(self.c_5010110) +
            self._D(self.c_5010111) +
            self._D(self.c_5010112) +

            self._D(self.c_50102) +
            self._D(self.c_5010201) +
            self._D(self.c_5010202) +

            self._D(self.c_50103) +
            self._D(self.c_5010301) +
            self._D(self.c_5010302) +

            self._D(self.c_50104) +
            self._D(self.c_5010401) +
            self._D(self.c_5010402) +
            self._D(self.c_5010403) +
            self._D(self.c_5010404) +
            self._D(self.c_5010405) +
            self._D(self.c_5010406) +
            self._D(self.c_5010407) +
            self._D(self.c_5010408) +

            self._D(self.c_50105) +
            self._D(self.c_5010501)
        )

    # =====================================================
    # 💸 GASTOS
    # =====================================================
    def calc_c_502(self):
        return (
            self._D(self.c_50201) +
            self._D(self.c_50202) +
            self._D(self.c_50203) +
            self._D(self.c_50204)
        )

    # =====================================================
    # 📊 RESULTADOS
    # =====================================================
    def calc_c_600(self):
        return self.calc_c_401() - self.calc_c_501()

    def calc_c_602(self):
        return self.calc_c_600() + self._D(self.c_403)

    def calc_c_607(self):
        return self.calc_c_602() - self.calc_c_502()

    def calc_c_707(self):
        return self.calc_c_607() - self._D(self.c_601) - self._D(self.c_603)

    def calc_c_801(self):
        return self.calc_c_707() + self._D(self.c_800)

    # =====================================================
    # ⚖️ AUDITOR (VALIDACIÓN SCVS)
    # =====================================================
    def clean(self):
        calculated = self.calc_c_801()
        reported = self._D(self.c_801)

        difference = calculated - reported

        if difference != Decimal("0.00"):
            raise ValidationError(
                f"DESCUADRE EIR SCVS: Calculado({calculated}) != Reportado({reported}) | Diferencia: {difference}"
            )

    # =====================================================
    # 💾 SAVE AUTOMÁTICO
    # =====================================================
    def save(self, *args, **kwargs):

        # INGRESOS
        self.c_401 = self.calc_c_401()

        # COSTOS
        self.c_501 = self.calc_c_501()

        # GASTOS
        self.c_502 = self.calc_c_502()

        # RESULTADOS
        self.c_600 = self.calc_c_600()
        self.c_602 = self.calc_c_602()
        self.c_607 = self.calc_c_607()
        self.c_707 = self.calc_c_707()
        self.c_801 = self.calc_c_801()

        # VALIDACIÓN FINAL
        self.full_clean()

        super().save(*args, **kwargs)

    class Meta:
        #unique_together = ('ruc', 'fiscal_year')
        verbose_name = "Estado Integral de Resultados(EIR)"
        verbose_name_plural = "Estados Integral de Resultados(EIR)"

    def __str__(self):
        return f"Ingresos:${self.c_401}, Costos: ${self.c_501}, Gastos: ${self.c_502}, Resultados: ${self.c_600}/$ {self.c_602}/ ${self.c_607}/${slef.c_707}/${self.c_801}"




class SCVS_EFE(models.Model):
    report = models.OneToOneField(SCVSFinancialReport, on_delete=models.CASCADE)

    c_95 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INCREMENTO NETO (DISMINUCIÓN) EN EL EFECTIVO Y EQUIVALENTES AL EFECTIVO, ANTES DEL EFECTO DE LOS CAMBIOS EN LA TASA DE CAMBIO"
    )

    c_9501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FLUJOS DE EFECTIVO PROCEDENTES DE (UTILIZADOS EN) ACTIVIDADES DE OPERACIÓN"
    )

    c_950101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Clases de cobros por actividades de operación"
    )

    c_95010101 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cobros procedentes de las ventas de bienes y prestación de servicios"
    )

    c_95010102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cobros procedentes de regalías, cuotas, comisiones y otros ingresos de actividades ordinarias"
    )

    c_95010103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cobros procedentes de contratos mantenidos con propósitos de intermediación o para negociar"
    )

    c_95010104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cobros procedentes de primas y prestaciones, anualidades y otros beneficios de pólizas suscritas"
    )

    c_95010105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cobros por actividades de operación"
    )

    c_950102 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Clases de pagos por actividades de operación"
    )

    c_95010201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos a proveedores por el suministro de bienes y servicios"
    )

    c_95010202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos procedentes de contratos mantenidos para intermediación o para negociar"
    )

    c_95010203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos a y por cuenta de los empleados"
    )

    c_95010204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos por primas y prestaciones, anualidades y otras obligaciones derivadas de las pólizas suscritas"
    )

    c_95010205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros pagos por actividades de operación"
    )

    c_950103 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos pagados"
    )

    c_950104 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos recibidos"
    )

    c_950105 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Intereses pagados"
    )

    c_950106 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Intereses recibidos"
    )

    c_950107 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Impuestos a las ganancias pagados"
    )

    c_950108 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otras entradas (salidas) de efectivo"
    )

    c_9502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FLUJOS DE EFECTIVO PROCEDENTES DE (UTILIZADOS EN) ACTIVIDADES DE INVERSIÓN"
    )

    c_950201 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Efectivo procedentes de la venta de acciones en subsidiarias u otros negocios"
    )

    c_950202 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Efectivo utilizado para adquirir acciones en subsidiarias u otros negocios para tener el control"
    )

    c_950203 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Efectivo utilizado en la compra de participaciones no controladoras"
    )

    c_950204 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cobros por la venta de acciones o instrumentos de deuda de otras entidades"
    )

    c_950205 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros pagos para adquirir acciones o instrumentos de deuda de otras entidades"
    )

    c_950206 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cobros por la venta de participaciones en negocios conjuntos"
    )

    c_950207 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros pagos para adquirir participaciones en negocios conjuntos"
    )

    c_950208 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Importes procedentes por la venta de propiedades, planta y equipo"
    )

    c_950209 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Adquisiciones de propiedades, planta y equipo"
    )

    c_950210 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Importes procedentes de ventas de activos intangibles"
    )

    c_950211 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Compras de activos intangibles"
    )

    c_950212 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Importes procedentes de otros activos a largo plazo"
    )

    c_950213 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Compras de otros activos a largo plazo"
    )

    c_950214 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Importes procedentes de subvenciones del gobierno"
    )

    c_950215 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Anticipos de efectivo efectuados a terceros"
    )

    c_950216 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cobros procedentes del reembolso de anticipos y préstamos concedidos a terceros"
    )

    c_950217 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos derivados de contratos de futuro, a término, de opciones y de permuta financiera"
    )

    c_950218 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Cobros procedentes de contratos de futuro, a término, de opciones y de permuta financiera"
    )

    c_950219 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos recibidos"
    )

    c_950220 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Intereses recibidos"
    )

    c_950221 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otras entradas (salidas) de efectivo"
    )

    c_9503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="FLUJOS DE EFECTIVO PROCEDENTES DE (UTILIZADOS EN) ACTIVIDADES DE FINANCIACIÓN"
    )

    c_950301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aporte en efectivo por aumento de capital"
    )

    c_950302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Financiamiento por emisión de títulos valores"
    )

    c_950303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos por adquirir o rescatar las acciones de la entidad"
    )

    c_950304 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Financiación por préstamos a largo plazo"
    )

    c_950305 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos de préstamos"
    )

    c_950306 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pagos de pasivos por arrendamientos financieros"
    )

    c_950307 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Importes procedentes de subvenciones del gobierno"
    )

    c_950308 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos pagados"
    )

    c_950309 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Intereses recibidos"
    )

    c_950310 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otras entradas (salidas) de efectivo"
    )

    c_9504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EFECTOS DE LA VARIACION EN LA TASA DE CAMBIO SOBRE EL EFECTIVO Y EQUIVALENTES AL EFECTIVO"
    )

    c_950401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Efectos de la variación en la tasa de cambio sobre el efectivo y equivalentes al efectivo"
    )

    c_9505 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="INCREMENTO (DISMINUCIÓN) NETO DE EFECTIVO Y EQUIVALENTES AL EFECTIVO"
    )

    c_9506 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EFECTIVO Y EQUIVALENTES AL EFECTIVO AL PRINCIPIO DEL PERIODO"
    )

    c_9507 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="EFECTIVO Y EQUIVALENTES AL EFECTIVO AL FINAL DEL PERIODO"
    )

    c_96 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="GANANCIA (PÉRDIDA) ANTES DE 15% A TRABAJADORES E IMPUESTO A LA RENTA"
    )

    c_97 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="AJUSTE POR PARTIDAS DISTINTAS AL EFECTIVO"
    )

    c_9701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajustes por gasto de depreciación y amortización"
    )

    c_9702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajustes por gastos por deterioro (reversiones por deterioro) reconocidas en los resultados del periodo"
    )

    c_9703 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pérdida (ganancia) de moneda extranjera no realizada"
    )

    c_9704 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Pérdidas en cambio de moneda extranjera"
    )

    c_9705 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajustes por gastos en provisiones"
    )

    c_9706 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajuste por participaciones no controladoras"
    )

    c_9707 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajuste por pagos basados en acciones"
    )

    c_9708 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajustes por ganancias (pérdidas) en valor razonable"
    )

    c_9709 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajustes por gasto por impuesto a la renta"
    )

    c_9710 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ajustes por gasto por participación trabajadores"
    )

    c_9711 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros ajustes por partidas distintas al efectivo"
    )

    c_98 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN ACTIVOS Y PASIVOS"
    )

    c_9801 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(Incremento) disminución en cuentas por cobrar clientes"
    )

    c_9802 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(Incremento) disminución en otras cuentas por cobrar"
    )

    c_9803 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(Incremento) disminución en anticipos de proveedores"
    )

    c_9804 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(Incremento) disminución en inventarios"
    )

    c_9805 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="(Incremento) disminución en otros activos"
    )

    c_9806 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Incremento  (disminución) en cuentas por pagar comerciales"
    )

    c_9807 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Incremento  (disminución) en otras cuentas por pagar"
    )

    c_9808 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Incremento  (disminución) en beneficios empleados"
    )

    c_9809 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Incremento  (disminución) en anticipos de clientes"
    )

    c_9810 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Incremento  (disminución) en otros pasivos"
    )

    c_9820 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Flujos de efectivo netos procedentes de (utilizados en) actividades de operación"
    )


    def _D(self, v):
        return v if v is not None else Decimal("0.00")

    # =====================================================
    # 💼 ACTIVIDADES DE OPERACIÓN
    # =====================================================
    def calc_operacion(self):
        return (
            self._D(self.c_9501) +
            self._D(self.c_950101) +
            self._D(self.c_95010101) +
            self._D(self.c_95010102) +
            self._D(self.c_95010103) +
            self._D(self.c_95010104) +
            self._D(self.c_95010105) +

            self._D(self.c_950102) +
            self._D(self.c_95010201) +
            self._D(self.c_95010202) +
            self._D(self.c_95010203) +
            self._D(self.c_95010204) +
            self._D(self.c_95010205) +

            self._D(self.c_950103) +
            self._D(self.c_950104) +
            self._D(self.c_950105) +
            self._D(self.c_950106) +
            self._D(self.c_950107) +
            self._D(self.c_950108)
        )

    # =====================================================
    # 🏗 ACTIVIDADES DE INVERSIÓN
    # =====================================================
    def calc_inversion(self):
        return (
            self._D(self.c_9502) +
            self._D(self.c_950201) +
            self._D(self.c_950202) +
            self._D(self.c_950203) +
            self._D(self.c_950204) +
            self._D(self.c_950205) +
            self._D(self.c_950206) +
            self._D(self.c_950207) +
            self._D(self.c_950208) +
            self._D(self.c_950209) +
            self._D(self.c_950210) +
            self._D(self.c_950211) +
            self._D(self.c_950212) +
            self._D(self.c_950213) +
            self._D(self.c_950214) +
            self._D(self.c_950215) +
            self._D(self.c_950216) +
            self._D(self.c_950217) +
            self._D(self.c_950218) +
            self._D(self.c_950219) +
            self._D(self.c_950220) +
            self._D(self.c_950221)
        )

    # =====================================================
    # 🏦 ACTIVIDADES DE FINANCIACIÓN
    # =====================================================
    def calc_financiacion(self):
        return (
            self._D(self.c_9503) +
            self._D(self.c_950301) +
            self._D(self.c_950302) +
            self._D(self.c_950303) +
            self._D(self.c_950304) +
            self._D(self.c_950305) +
            self._D(self.c_950306) +
            self._D(self.c_950307) +
            self._D(self.c_950308) +
            self._D(self.c_950309) +
            self._D(self.c_950310)
        )

    # =====================================================
    # 💱 EFECTO TIPO DE CAMBIO / OTROS
    # =====================================================
    def calc_otros(self):
        return (
            self._D(self.c_9504) +
            self._D(self.c_950401) +
            self._D(self.c_9505) +
            self._D(self.c_9506) +
            self._D(self.c_9507)
        )

    # =====================================================
    # 📈 CONCILIACIÓN (MÉTODO INDIRECTO)
    # =====================================================
    def calc_conciliacion(self):
        return (
            self._D(self.c_96) +
            self._D(self.c_97) +
            self._D(self.c_9701) +
            self._D(self.c_9702) +
            self._D(self.c_9703) +
            self._D(self.c_9704) +
            self._D(self.c_9705) +
            self._D(self.c_9706) +
            self._D(self.c_9707) +
            self._D(self.c_9708) +
            self._D(self.c_9709) +
            self._D(self.c_9710) +
            self._D(self.c_9711)
        )

    # =====================================================
    # 🔄 CAMBIOS EN ACTIVOS Y PASIVOS
    # =====================================================
    def calc_cambios(self):
        return (
            self._D(self.c_98) +
            self._D(self.c_9801) +
            self._D(self.c_9802) +
            self._D(self.c_9803) +
            self._D(self.c_9804) +
            self._D(self.c_9805) +
            self._D(self.c_9806) +
            self._D(self.c_9807) +
            self._D(self.c_9808) +
            self._D(self.c_9809) +
            self._D(self.c_9810) +
            self._D(self.c_9820)
        )

    # =====================================================
    # 📊 RESULTADO GENERAL (FLUJO NETO)
    # =====================================================
    def calc_c_95(self):
        return (
            self.calc_operacion() +
            self.calc_inversion() +
            self.calc_financiacion() +
            self.calc_otros()
        )

    # =====================================================
    # ⚖️ AUDITOR SCVS (CUADRE AUTOMÁTICO)
    # =====================================================
    def clean(self):
        errores = {}

        # 1. Validación: incremento neto vs efectivo inicial/final
        if self.c_9505 is not None and self.c_9506 is not None and self.c_9507 is not None:
            calculado = self.c_9507 - self.c_9506
            diferencia = calculado - self.c_9505

            if abs(diferencia) >= 0.01:
                errores['c_9505'] = (
                    f"El incremento neto ({self.c_9505}) no cuadra con "
                    f"efectivo final - inicial ({calculado}). Diferencia: {diferencia}"
                )

        # 2. Validación: suma de actividades
        suma_actividades = (
            (self.c_9501 or 0) +
            (self.c_9502 or 0) +
            (self.c_9503 or 0)
        )

        if self.c_9505 is not None:
            diferencia = suma_actividades - self.c_9505

            if abs(diferencia) >= 0.01:
                errores['c_9505'] = (
                    f"La suma de actividades ({suma_actividades}) no coincide con "
                    f"el incremento neto ({self.c_9505}). Diferencia: {diferencia}"
                )

        # 3. Validación: incluyendo tipo de cambio
        if all(v is not None for v in [self.c_9501, self.c_9502, self.c_9503, self.c_9504, self.c_9505]):
            total = self.c_9501 + self.c_9502 + self.c_9503 + self.c_9504
            diferencia = total - self.c_9505

            if abs(diferencia) >= 0.01:
                errores['c_9504'] = (
                    f"El total incluyendo variación en tipo de cambio ({total}) "
                    f"no coincide con el incremento neto ({self.c_9505}). "
                    f"Diferencia: {diferencia}"
                )

        if errores:
            raise ValidationError(errores)
    # =====================================================
    # 💾 SAVE AUTOMÁTICO
    # =====================================================
    def save(self, *args, **kwargs):

        # BLOQUES
        self.c_95 = self.calc_c_95()

        # VALIDACIÓN FINAL (OBLIGATORIA)
        self.full_clean()

        super().save(*args, **kwargs)

    class Meta:
        #unique_together = ('ruc', 'fiscal_year')
        verbose_name = "Estado Flujo Efectivo (EFE)"
        verbose_name_plural = "Estados Flujo Efectivo (EFE)"

    def __str__(self):
        return f"Resultado General :${self.c_95}"


class SCVS_ECP(models.Model):
    report = models.OneToOneField   (SCVSFinancialReport, on_delete=models.CASCADE)

    c_99_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / CAPITAL"
    )

    c_99_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_99_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_99_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / RESERVA LEGAL"
    )

    c_99_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_99_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_99_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_99_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_99_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / OTROS SUPERAVIT POR REVALUACION"
    )

    c_99_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / GANANCIAS ACUMULADAS"
    )

    c_99_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / (-) PÉRDIDAS ACUMULADAS"
    )

    c_99_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_99_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERÍODO / RESERVA DE CAPITAL"
    )

    c_99_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERÍODO / RESERVA POR DONACIONES"
    )

    c_99_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERÍODO / RESERVA POR VALUACIÓN"
    )

    c_99_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_99_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / GANANCIA NETA DEL PERIODO"
    )

    c_99_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERIODO / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_99_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERÍODO"
    )

    c_99_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO AL FINAL DEL PERÍODO"
    )

    c_9901_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / CAPITAL"
    )

    c_9901_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_9901_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_9901_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / / RESERVA LEGAL"
    )

    c_9901_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_9901_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_9901_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_9901_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_9901_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_9901_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / GANANCIAS ACUMULADAS"
    )

    c_9901_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / (-) PÉRDIDAS ACUMULADAS"
    )

    c_9901_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_9901_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / RESERVA DE CAPITAL"
    )

    c_9901_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / RESERVA POR DONACIONES"
    )

    c_9901_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / RESERVA POR VALUACIÓN"
    )

    c_9901_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_9901_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / GANANCIA NETA DEL PERIODO"
    )

    c_9901_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_9901_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR"
    )

    c_9901_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR"
    )

    c_990101_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / CAPITAL"
    )

    c_990101_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990101_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990101_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / RESERVA LEGAL"
    )

    c_990101_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990101_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990101_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990101_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990101_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990101_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / GANANCIAS ACUMULADAS"
    )

    c_990101_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990101_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990101_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / RESERVA DE CAPITAL"
    )

    c_990101_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR / RESERVA POR DONACIONES"
    )

    c_990101_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / RESERVA POR VALUACIÓN"
    )

    c_990101_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990101_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / GANANCIA NETA DEL PERIODO"
    )

    c_990101_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990101_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR"
    )

    c_990101_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="SALDO DEL PERÍODO INMEDIATO ANTERIOR"
    )

    c_990102_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / CAPITAL"
    )

    c_990102_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990102_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990102_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / RESERVA LEGAL"
    )

    c_990102_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990102_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990102_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990102_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990102_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990102_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / GANANCIAS ACUMULADAS"
    )

    c_990102_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990102_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990102_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / RESERVA DE CAPITAL"
    )

    c_990102_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES: / RESERVA POR DONACIONES"
    )

    c_990102_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / RESERVA POR VALUACIÓN"
    )

    c_990102_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990102_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / GANANCIA NETA DEL PERIODO"
    )

    c_990102_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990102_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:"
    )

    c_990102_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS EN POLITICAS CONTABLES:"
    )

    c_990103_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / CAPITAL"
    )

    c_990103_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990103_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990103_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / RESERVA LEGAL"
    )

    c_990103_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990103_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990103_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990103_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990103_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990103_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / GANANCIAS ACUMULADAS"
    )

    c_990103_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990103_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990103_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / RESERVA DE CAPITAL"
    )

    c_990103_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES / RESERVA POR DONACIONES"
    )

    c_990103_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / RESERVA POR VALUACIÓN"
    )

    c_990103_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990103_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / GANANCIA NETA DEL PERIODO"
    )

    c_990103_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCIÓN DE ERRORES  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990103_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCION DE ERRORES"
    )

    c_990103_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CORRECCION DE ERRORES"
    )

    c_9902_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / CAPITAL"
    )

    c_9902_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_9902_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_9902_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / RESERVA LEGAL"
    )

    c_9902_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_9902_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_9902_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_9902_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:   / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_9902_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_9902_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / GANANCIAS ACUMULADAS"
    )

    c_9902_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / (-) PÉRDIDAS ACUMULADAS"
    )

    c_9902_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_9902_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / RESERVA DE CAPITAL"
    )

    c_9902_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO: / RESERVA POR DONACIONES"
    )

    c_9902_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / RESERVA POR VALUACIÓN"
    )

    c_9902_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_9902_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / GANANCIA NETA DEL PERIODO"
    )

    c_9902_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_9902_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:"
    )

    c_9902_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="CAMBIOS DEL AÑO EN EL PATRIMONIO:"
    )

    c_990201_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / CAPITAL"
    )

    c_990201_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990201_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990201_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / RESERVA LEGAL"
    )

    c_990201_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990201_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990201_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990201_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990201_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990201_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / GANANCIAS ACUMULADAS"
    )

    c_990201_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990201_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990201_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / RESERVA DE CAPITAL"
    )

    c_990201_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social / RESERVA POR DONACIONES"
    )

    c_990201_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / RESERVA POR VALUACIÓN"
    )

    c_990201_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990201_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / GANANCIA NETA DEL PERIODO"
    )

    c_990201_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990201_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social"
    )

    c_990201_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aumento (disminución) de capital social"
    )

    c_990202_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / CAPITAL"
    )

    c_990202_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990202_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990202_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / RESERVA LEGAL"
    )

    c_990202_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990202_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990202_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990202_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990202_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990202_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / GANANCIAS ACUMULADAS"
    )

    c_990202_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990202_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990202_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / RESERVA DE CAPITAL"
    )

    c_990202_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones / RESERVA POR DONACIONES"
    )

    c_990202_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / RESERVA POR VALUACIÓN"
    )

    c_990202_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990202_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / GANANCIA NETA DEL PERIODO"
    )

    c_990202_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990202_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones"
    )

    c_990202_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Aportes para futuras capitalizaciones"
    )

    c_990203_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / CAPITAL"
    )

    c_990203_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990203_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990203_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / RESERVA LEGAL"
    )

    c_990203_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990203_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990203_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990203_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990203_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990203_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / GANANCIAS ACUMULADAS"
    )

    c_990203_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990203_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990203_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / RESERVA DE CAPITAL"
    )

    c_990203_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones / RESERVA POR DONACIONES"
    )

    c_990203_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / RESERVA POR VALUACIÓN"
    )

    c_990203_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990203_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / GANANCIA NETA DEL PERIODO"
    )

    c_990203_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990203_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones"
    )

    c_990203_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Prima por emisión primaria de acciones"
    )

    c_990204_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / CAPITAL"
    )

    c_990204_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990204_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990204_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / RESERVA LEGAL"
    )

    c_990204_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990204_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990204_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990204_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990204_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990204_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / GANANCIAS ACUMULADAS"
    )

    c_990204_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990204_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990204_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / RESERVA DE CAPITAL"
    )

    c_990204_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos / RESERVA POR DONACIONES"
    )

    c_990204_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / RESERVA POR VALUACIÓN"
    )

    c_990204_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990204_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / GANANCIA NETA DEL PERIODO"
    )

    c_990204_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990204_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos"
    )

    c_990204_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Dividendos"
    )

    c_990205_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / CAPITAL"
    )

    c_990205_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990205_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990205_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / RESERVA LEGAL"
    )

    c_990205_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990205_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990205_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990205_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990205_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990205_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / GANANCIAS ACUMULADAS"
    )

    c_990205_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990205_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990205_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / RESERVA DE CAPITAL"
    )

    c_990205_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales / RESERVA POR DONACIONES"
    )

    c_990205_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / RESERVA POR VALUACIÓN"
    )

    c_990205_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990205_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / GANANCIA NETA DEL PERIODO"
    )

    c_990205_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990205_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales"
    )

    c_990205_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Transferencia de Resultados a otras cuentas patrimoniales"
    )

    c_990206_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / CAPITAL"
    )

    c_990206_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990206_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990206_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / RESERVA LEGAL"
    )

    c_990206_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990206_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990206_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990206_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990206_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990206_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / GANANCIAS ACUMULADAS"
    )

    c_990206_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990206_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990206_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / RESERVA DE CAPITAL"
    )

    c_990206_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / RESERVA POR DONACIONES"
    )

    c_990206_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / RESERVA POR VALUACIÓN"
    )

    c_990206_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990206_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / GANANCIA NETA DEL PERIODO"
    )

    c_990206_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990206_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta"
    )

    c_990206_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta"
    )

    c_990207_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / CAPITAL"
    )

    c_990207_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990207_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990207_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / RESERVA LEGAL"
    )

    c_990207_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990207_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990207_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990207_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990207_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990207_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / GANANCIAS ACUMULADAS"
    )

    c_990207_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990207_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990207_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / RESERVA DE CAPITAL"
    )

    c_990207_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo / RESERVA POR DONACIONES"
    )

    c_990207_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / RESERVA POR VALUACIÓN"
    )

    c_990207_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990207_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / GANANCIA NETA DEL PERIODO"
    )

    c_990207_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990207_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo"
    )

    c_990207_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Propiedades, planta y equipo"
    )

    c_990208_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / CAPITAL"
    )

    c_990208_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990208_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990208_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / RESERVA LEGAL"
    )

    c_990208_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990208_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990208_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990208_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990208_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990208_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / GANANCIAS ACUMULADAS"
    )

    c_990208_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990208_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990208_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / RESERVA DE CAPITAL"
    )

    c_990208_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles / RESERVA POR DONACIONES"
    )

    c_990208_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / RESERVA POR VALUACIÓN"
    )

    c_990208_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990208_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / GANANCIA NETA DEL PERIODO"
    )

    c_990208_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990208_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles"
    )

    c_990208_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Realización de la Reserva por Valuación de Activos Intangibles"
    )

    c_990209_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / CAPITAL"
    )

    c_990209_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990209_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990209_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / RESERVA LEGAL"
    )

    c_990209_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990209_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990209_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990209_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990209_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990209_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / GANANCIAS ACUMULADAS"
    )

    c_990209_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990209_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990209_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / RESERVA DE CAPITAL"
    )

    c_990209_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar) / RESERVA POR DONACIONES"
    )

    c_990209_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / RESERVA POR VALUACIÓN"
    )

    c_990209_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990209_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / GANANCIA NETA DEL PERIODO"
    )

    c_990209_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990209_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)"
    )

    c_990209_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Otros cambios (detallar)"
    )

    c_990210_301 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / CAPITAL"
    )

    c_990210_302 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990210_303 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990210_30401 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / RESERVA LEGAL"
    )

    c_990210_30402 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990210_30501 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990210_30502 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990210_30503 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990210_30504 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990210_30601 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / GANANCIAS ACUMULADAS"
    )

    c_990210_30602 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990210_30603 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990210_30604 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / RESERVA DE CAPITAL"
    )

    c_990210_30605 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / RESERVA POR DONACIONES"
    )

    c_990210_30606 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / RESERVA POR VALUACIÓN"
    )

    c_990210_30607 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990210_30701 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / GANANCIA NETA DEL PERIODO"
    )

    c_990210_30702 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990210_30 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)"
    )

    c_990210_31 = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)"
    )


    def __str__(self):
        return f"Saldo Final del Período:${self.c_99_30 }"

    # =========================
    # 🔧 UTILIDAD
    # =========================
    def _D(self, v):
        return v if v is not None else Decimal("0.00")

    # =====================================================
    # 💰 SALDO FINAL DEL PERIODO
    # =====================================================
    def calc_99(self):
        return (
            self._D(self.c_99_301) +
            self._D(self.c_99_302) +
            self._D(self.c_99_303) +
            self._D(self.c_99_30401) +
            self._D(self.c_99_30402) +
            self._D(self.c_99_30501) +
            self._D(self.c_99_30502) +
            self._D(self.c_99_30503) +
            self._D(self.c_99_30504) +
            self._D(self.c_99_30601) +
            self._D(self.c_99_30602) +
            self._D(self.c_99_30603) +
            self._D(self.c_99_30604) +
            self._D(self.c_99_30605) +
            self._D(self.c_99_30606) +
            self._D(self.c_99_30607) +
            self._D(self.c_99_30701) +
            self._D(self.c_99_30702) +
            self._D(self.c_99_30) +
            self._D(self.c_99_31)
        )

    # =====================================================
    # 📊 SALDO REEXPRESADO
    # =====================================================
    def calc_9901(self):
        return (
            self._D(self.c_9901_301) +
            self._D(self.c_9901_302) +
            self._D(self.c_9901_303) +
            self._D(self.c_9901_30401) +
            self._D(self.c_9901_30402) +
            self._D(self.c_9901_30501) +
            self._D(self.c_9901_30502) +
            self._D(self.c_9901_30503) +
            self._D(self.c_9901_30504) +
            self._D(self.c_9901_30601) +
            self._D(self.c_9901_30602) +
            self._D(self.c_9901_30603) +
            self._D(self.c_9901_30604) +
            self._D(self.c_9901_30605) +
            self._D(self.c_9901_30606) +
            self._D(self.c_9901_30607) +
            self._D(self.c_9901_30701) +
            self._D(self.c_9901_30702) +
            self._D(self.c_9901_30) +
            self._D(self.c_9901_31)
        )

    # =====================================================
    # 📄 SALDO PERIODO ANTERIOR
    # =====================================================
    def calc_990101(self):
        return (
            self._D(self.c_990101_301) +
            self._D(self.c_990101_302) +
            self._D(self.c_990101_303) +
            self._D(self.c_990101_30401) +
            self._D(self.c_990101_30402) +
            self._D(self.c_990101_30501) +
            self._D(self.c_990101_30502) +
            self._D(self.c_990101_30503) +
            self._D(self.c_990101_30504) +
            self._D(self.c_990101_30601) +
            self._D(self.c_990101_30602) +
            self._D(self.c_990101_30603) +
            self._D(self.c_990101_30604) +
            self._D(self.c_990101_30605) +
            self._D(self.c_990101_30606) +
            self._D(self.c_990101_30607) +
            self._D(self.c_990101_30701) +
            self._D(self.c_990101_30702) +
            self._D(self.c_990101_30) +
            self._D(self.c_990101_31)
        )

    # =====================================================
    # ⚙️ CAMBIOS POLÍTICAS CONTABLES
    # =====================================================
    def calc_990102(self):
        return (
            self._D(self.c_990102_301) +
            self._D(self.c_990102_302) +
            self._D(self.c_990102_303) +
            self._D(self.c_990102_30401) +
            self._D(self.c_990102_30402) +
            self._D(self.c_990102_30501) +
            self._D(self.c_990102_30502) +
            self._D(self.c_990102_30503) +
            self._D(self.c_990102_30504) +
            self._D(self.c_990102_30601) +
            self._D(self.c_990102_30602) +
            self._D(self.c_990102_30603) +
            self._D(self.c_990102_30604) +
            self._D(self.c_990102_30605) +
            self._D(self.c_990102_30606) +
            self._D(self.c_990102_30607) +
            self._D(self.c_990102_30701) +
            self._D(self.c_990102_30702) +
            self._D(self.c_990102_30) +
            self._D(self.c_990102_31)
        )

    # =====================================================
    # 🚨 CORRECCIÓN ERRORES
    # =====================================================
    def calc_990103(self):
        return (
            self._D(self.c_990103_301) +
            self._D(self.c_990103_302) +
            self._D(self.c_990103_303) +
            self._D(self.c_990103_30401) +
            self._D(self.c_990103_30402) +
            self._D(self.c_990103_30501) +
            self._D(self.c_990103_30502) +
            self._D(self.c_990103_30503) +
            self._D(self.c_990103_30504) +
            self._D(self.c_990103_30601) +
            self._D(self.c_990103_30602) +
            self._D(self.c_990103_30603) +
            self._D(self.c_990103_30604) +
            self._D(self.c_990103_30605) +
            self._D(self.c_990103_30606) +
            self._D(self.c_990103_30607) +
            self._D(self.c_990103_30701) +
            self._D(self.c_990103_30702) +
            self._D(self.c_990103_30) +
            self._D(self.c_990103_31)
        )

    # =====================================================
    # 📈 CAMBIOS DEL AÑO
    # =====================================================
    def calc_9902(self):
        return (
            self._D(self.c_9902_301) +
            self._D(self.c_9902_302) +
            self._D(self.c_9902_303) +
            self._D(self.c_9902_30401) +
            self._D(self.c_9902_30402) +
            self._D(self.c_9902_30501) +
            self._D(self.c_9902_30502) +
            self._D(self.c_9902_30503) +
            self._D(self.c_9902_30504) +
            self._D(self.c_9902_30601) +
            self._D(self.c_9902_30602) +
            self._D(self.c_9902_30603) +
            self._D(self.c_9902_30604) +
            self._D(self.c_9902_30605) +
            self._D(self.c_9902_30606) +
            self._D(self.c_9902_30607) +
            self._D(self.c_9902_30701) +
            self._D(self.c_9902_30702) +
            self._D(self.c_9902_30) +
            self._D(self.c_9902_31)
        )

    # =====================================================
    # 📊 AUMENTO / DISMINUCIÓN CAPITAL
    # =====================================================
    def calc_990201(self):
        return (
            self._D(self.c_990201_301) +
            self._D(self.c_990201_302) +
            self._D(self.c_990201_303) +
            self._D(self.c_990201_30401) +
            self._D(self.c_990201_30402) +
            self._D(self.c_990201_30501) +
            self._D(self.c_990201_30502) +
            self._D(self.c_990201_30503) +
            self._D(self.c_990201_30504) +
            self._D(self.c_990201_30601) +
            self._D(self.c_990201_30602) +
            self._D(self.c_990201_30603) +
            self._D(self.c_990201_30604) +
            self._D(self.c_990201_30605) +
            self._D(self.c_990201_30606) +
            self._D(self.c_990201_30607) +
            self._D(self.c_990201_30701) +
            self._D(self.c_990201_30702) +
            self._D(self.c_990201_30) +
            self._D(self.c_990201_31)
        )

    # =====================================================
    # 💸 DIVIDENDOS
    # =====================================================
    def calc_990204(self):
        return (
            self._D(self.c_990204_301) +
            self._D(self.c_990204_302) +
            self._D(self.c_990204_303) +
            self._D(self.c_990204_30401) +
            self._D(self.c_990204_30402) +
            self._D(self.c_990204_30501) +
            self._D(self.c_990204_30502) +
            self._D(self.c_990204_30503) +
            self._D(self.c_990204_30504) +
            self._D(self.c_990204_30601) +
            self._D(self.c_990204_30602) +
            self._D(self.c_990204_30603) +
            self._D(self.c_990204_30604) +
            self._D(self.c_990204_30605) +
            self._D(self.c_990204_30606) +
            self._D(self.c_990204_30607) +
            self._D(self.c_990204_30701) +
            self._D(self.c_990204_30702) +
            self._D(self.c_990204_30) +
            self._D(self.c_990204_31)
        )

    # =====================================================
    # 📊 TOTAL PATRIMONIO (CONTROL FINAL)
    # =====================================================
    def calc_total_ecp(self):
        return (
            self.calc_99() +
            self.calc_9901() +
            self.calc_990101() +
            self.calc_990102() +
            self.calc_990103() +
            self.calc_9902() +
            self.calc_990201() +
            self.calc_990204()
        )





    # -------------------------
    # AUDITOR PRINCIPAL SCVS
    # -------------------------
    def clean(self):
        errors = {}
        calculado = self.calc_total_ecp()
        reportado = self._D(self.c_99_30)  # control final (ajustable si usas otro campo)

        diferencia = calculado - reportado

        if diferencia != Decimal("0.00"):
            raise ValidationError(
                f"DESCUADRE ECP SCVS: Calculado({calculado}) != Reportado({reportado}) | Diferencia: {diferencia}"
            )


        # =========================================================
        # 1. VALIDACIÓN DE TOTALES POR BLOQUES (SUMATORIAS)
        # =========================================================

        def check_block(prefix, fields, total_field, label):
            total_calc = sum(self._v(getattr(self, f)) for f in fields)
            total_db = self._v(getattr(self, total_field))

            if abs(total_calc - total_db) > Decimal("0.01"):
                errors[total_field] = f"Inconsistencia en {label}: calculado={total_calc} vs registrado={total_db}"

        # =========================
        # SALDO FINAL DEL PERIODO
        # =========================
        check_block("c_99",
            [
                "c_99_301","c_99_302","c_99_303",
                "c_99_30401","c_99_30402",
                "c_99_30501","c_99_30502","c_99_30503","c_99_30504",
                "c_99_30601","c_99_30602","c_99_30603",
                "c_99_30604","c_99_30605","c_99_30606","c_99_30607",
                "c_99_30701","c_99_30702",
            ],
            "c_99_30",
            "SALDO FINAL DEL PERIODO"
        )

        # =========================
        # CAMBIOS DEL AÑO EN EL PATRIMONIO
        # =========================
        check_block("c_9902",
            [
                "c_9902_301","c_9902_302","c_9902_303",
                "c_9902_30401","c_9902_30402",
                "c_9902_30501","c_9902_30502","c_9902_30503","c_9902_30504",
                "c_9902_30601","c_9902_30602","c_9902_30603",
                "c_9902_30604","c_9902_30605","c_9902_30606","c_9902_30607",
                "c_9902_30701","c_9902_30702",
            ],
            "c_9902_30",
            "CAMBIOS DEL AÑO EN EL PATRIMONIO"
        )

        # =========================================================
        # 2. VALIDACIÓN DE DIVIDENDOS (REGLA CONTABLE REAL)
        # =========================================================
        dividendos = self._v(self.c_990204_30)

        utilidades = self._v(self.c_9902_30701) - self._v(self.c_9902_30702)

        if dividendos > utilidades and utilidades > 0:
            errors["c_990204_30"] = "Dividendos no pueden exceder utilidades disponibles."

        # =========================================================
        # 3. VALIDACIÓN CAPITAL (NO NEGATIVO)
        # =========================================================
        if self._v(self.c_99_301) < 0:
            errors["c_99_301"] = "El capital no puede ser negativo."

        # =========================================================
        # 4. VALIDACIÓN DE CONSISTENCIA ENTRE PERIODOS
        # =========================================================
        def compare(a, b, field):
            if abs(self._v(a) - self._v(b)) > Decimal("0.01"):
                errors[field] = f"Inconsistencia entre periodos en {field}"

        compare(self.c_9901_30, self.c_990101_30, "totales_periodo_anterior")

        # =========================================================
        # 5. VALIDACIÓN DE CAMBIOS EN POLÍTICAS CONTABLES
        # =========================================================
        cambio_politicas_total = self._v(self.c_990102_30)
        if cambio_politicas_total != 0:
            # regla auditor: debe existir soporte
            if cambio_politicas_total != sum([
                self._v(self.c_990102_30701),
                -self._v(self.c_990102_30702),
            ]):
                errors["c_990102_30"] = "Cambios en políticas contables no cuadran con resultados."

        # =========================================================
        # 6. CORRECCIÓN DE ERRORES (CONTROL AUDITORIAL)
        # =========================================================
        if self._v(self.c_990103_30) != sum([
            self._v(self.c_990103_30701),
            -self._v(self.c_990103_30702),
        ]):
            errors["c_990103_30"] = "Corrección de errores no cuadra con resultados."

        # =========================================================
        # 7. VALIDACIÓN DE RECONCILIACIÓN GLOBAL (PRINCIPAL)
        # =========================================================
        saldo_final = self._v(self.c_99_30)
        saldo_inicial = self._v(self.c_990101_30)
        cambios = self._v(self.c_9902_30)

        if abs((saldo_inicial + cambios) - saldo_final) > Decimal("0.01"):
            errors["__all__"] = "El patrimonio no cuadra: inicial + cambios != final."

        # =========================================================
        # 8. VALIDACIÓN DE INTEGRIDAD GENERAL
        # =========================================================
        if saldo_final <= 0:
            errors["__all__"] = "El patrimonio final no puede ser cero o negativo."

        # =========================================================
        # LANZAR ERRORES
        # =========================================================
        if errors:
            raise ValidationError(errors)

    # =====================================================
    # 💾 SAVE
    # =====================================================
    def save(self, *args, **kwargs):

        # puedes recalcular aquí si tienes campos padre automáticos
        self.c_99_30 = self.calc_99()

        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Estado de Cambio de Patrimonio (ECP)"
        verbose_name_plural = "Estados de Cambio de Patrimonio (ECP)"


# ===========================
# SPDP - Superintendencia de Protección de Datos Personales
# ===========================
class SPDP_Consentimiento(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_consentimientos')
    cliente = models.CharField(max_length=255)
    finalidad = models.TextField()
    fecha_firma = models.DateField()
    aceptado = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='spdp/consentimientos/', blank=True, null=True)

    def get_document_name(self):
        return f"Consentimiento_{self.cliente}_{self.fecha_firma.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Consentimiento SPDP"
        verbose_name_plural = "Consentimientos SPDP"

class SPDP_RAT(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_rat')
    tipo_dato = models.CharField(max_length=255)
    finalidad = models.TextField()
    base_legal = models.CharField(max_length=255)
    medidas_seguridad = models.TextField()
    fecha_inicio = models.DateField(default=timezone.now)
    archivo = models.FileField(upload_to='spdp/rat/', blank=True, null=True)

    def get_document_name(self):
        return f"RAT_{self.tipo_dato}_{self.fecha_inicio.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "RAT SPDP"
        verbose_name_plural = "RAT SPDP"

class SPDP_DPIA(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_dpia')
    descripcion = models.TextField()
    riesgo_identificado = models.TextField()
    medidas_mitigacion = models.TextField()
    fecha_elaboracion = models.DateField(default=timezone.now)
    archivo = models.FileField(upload_to='spdp/dpia/', blank=True, null=True)

    def get_document_name(self):
        return f"DPIA_{self.fecha_elaboracion.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "DPIA SPDP"
        verbose_name_plural = "DPIA SPDP"

class SPDP_ARCO(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_arco')
    cliente = models.CharField(max_length=255)
    tipo_solicitud = models.CharField(max_length=50, choices=[
        ('ACCESO','Acceso'),
        ('RECTIFICACION','Rectificación'),
        ('CANCELACION','Cancelación'),
        ('OPOSICION','Oposición')
    ])
    descripcion = models.TextField()
    fecha_solicitud = models.DateField(default=timezone.now)
    fecha_respuesta = models.DateField(null=True, blank=True)
    respondido = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='spdp/arco/', blank=True, null=True)

    def get_document_name(self):
        return f"ARCO_{self.cliente}_{self.tipo_solicitud}_{self.fecha_solicitud.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Solicitud ARCO SPDP"
        verbose_name_plural = "Solicitudes ARCO SPDP"

class SPDP_Incidente(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_incidentes')
    cliente = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField()
    fecha_detectado = models.DateField(default=timezone.now)
    nivel_gravedad = models.CharField(max_length=10, choices=[
        ('BAJO','Bajo'),
        ('MEDIO','Medio'),
        ('ALTO','Alto')
    ])
    notificado = models.BooleanField(default=False)
    archivo = models.FileField(upload_to='spdp/incidentes/', blank=True, null=True)

    def get_document_name(self):
        return f"Incidente_{self.fecha_detectado.strftime('%Y%m%d')}_{self.nivel_gravedad}"

    class Meta:
        verbose_name = "Incidente SPDP"
        verbose_name_plural = "Incidentes SPDP"

class SPDP_PoliticaInterna(models.Model):

    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_politicas')
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha_aprobacion = models.DateField(default=timezone.now)
    vigente = models.BooleanField(default=True)
    archivo = models.FileField(upload_to='spdp/politicas/', blank=True, null=True)

    def get_document_name(self):
        return f"Politica_{self.nombre}_{self.fecha_aprobacion.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Política Interna SPDP"
        verbose_name_plural = "Políticas Internas SPDP"

from django.db import models
from datetime import timedelta
from django.utils import timezone


class SPDP_ActaDelegado(models.Model):

    # =====================================================
    # I. DOCUMENTO DEL DELEGADO DE PROTECCIÓN DE DATOS (DPD)
    # =====================================================

    regulacion = models.ForeignKey(
        Regulacion,
        on_delete=models.CASCADE,
        related_name='spdp_delegado'
    )

    nombre_delegado = models.CharField(max_length=255,null=True, blank=True, verbose_name="Delegado (DPD)")
    identificacion_delegado = models.CharField(max_length=50,null=True, blank=True)
    correo_delegado = models.EmailField(blank=True, null=True)
    telefono_delegado = models.CharField(max_length=30, blank=True, null=True)

    fecha_nombramiento = models.DateField(null=True, blank=True)
    acto_designacion = models.CharField(
        max_length=255,
        help_text="Número o referencia del acto administrativo",
        null=True, blank=True
    )

    tipo_vinculacion = models.CharField(
        max_length=50,
        choices=[
            ("dependencia", "Relación de dependencia"),
            ("servicios", "Prestación de servicios"),
            ("externo", "Delegado externo")
        ],
        blank=True,
        null=True
    )

    funciones_delegado = models.TextField(
        help_text="Funciones del DPD conforme a la LOPDP",
        blank=True,
        null=True
    )

    declaracion_independencia = models.BooleanField(default=True)
    declaracion_confidencialidad = models.BooleanField(default=True)
    hash_delegado = models.CharField(max_length=255, blank=True, null=True)

    # =====================================================
    # II. REGISTRO DE ACTIVIDADES DE TRATAMIENTO (RAT)
    # =====================================================

    rat_titular_datos = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='rat_tratamientos',
    help_text="Usuario titular de los datos personales",
    verbose_name="Titulares (DPD)"

    )



    rat_nombre_tratamiento = models.CharField(
        max_length=255,
        help_text="Nombre o identificación del tratamiento",
        blank=True,
        null=True
    )

    rat_finalidad = models.TextField(
        help_text="Finalidad específica del tratamiento",
        blank=True,
        null=True
    )

    RAT_BASE_LEGAL_CHOICES = [
    ("art7_consentimiento", "Art. 7 LOPDP – Consentimiento del titular"),
    ("art7_obligacion_legal", "Art. 7 LOPDP – Cumplimiento de obligación legal"),
    ("art7_contrato", "Art. 7 LOPDP – Ejecución de un contrato"),
    ("art7_precontractual", "Art. 7 LOPDP – Medidas precontractuales"),
    ("art7_interes_publico", "Art. 7 LOPDP – Interés público o ejercicio de potestades públicas"),
    ("art7_interes_legitimo", "Art. 7 LOPDP – Interés legítimo del responsable o tercero"),
    ("art7_intereses_vitales", "Art. 7 LOPDP – Protección de intereses vitales"),
    ("art12_nna", "Art. 12 LOPDP – Datos de niños, niñas y adolescentes"),
    ]

    RAT_CATEGORIA_DATOS_CHOICES = [
    ("personales", "Datos personales"),
    ("sensibles", "Datos sensibles"),
    ("financieros", "Datos financieros"),
    ("salud", "Datos de salud"),
    ("laborales", "Datos laborales"),
    ]

    RAT_CATEGORIA_TITULARES_CHOICES = [
    ("clientes", "Clientes"),
    ("empleados", "Empleados"),
    ("proveedores", "Proveedores"),
    ("usuarios_web", "Usuarios web"),
    ]

    RAT_CATEGORIA_DESTINATARIOS_CHOICES = [
    ("internos", "Departamentos internos"),
    ("externos", "Proveedores de servicios"),
    ("entidades_gubernamentales", "Entidades gubernamentales"),
    ("terceros_autorizados", "Terceros autorizados"),
    ]



    rat_base_legal =  models.CharField(
    max_length=255,
    null=True,
    choices=RAT_BASE_LEGAL_CHOICES,
    help_text=(
        "Base(s) legal(es) del tratamiento conforme a la LOPDP. "

    )
    )


    rat_categoria_datos =  models.CharField(
    max_length=255,
    blank=True,
    null=True,
    choices=RAT_CATEGORIA_DATOS_CHOICES,
    help_text="Categorías de datos personales tratados. Seleccione uno o varios."
    )

    rat_categoria_titulares = models.CharField(
    max_length=255,
    blank=True,
    null=True,
    choices=RAT_CATEGORIA_TITULARES_CHOICES,
    help_text="Categorías de titulares de datos. Seleccione uno o varios."
    )

    rat_categoria_destinatarios =  models.CharField(
    max_length=255,
    blank=True,
    null=True,
    choices=RAT_CATEGORIA_DESTINATARIOS_CHOICES,
    help_text="Destinatarios o terceros receptores de datos. Seleccione uno o varios.",

    )

    rat_transferencias_internacionales = models.BooleanField(default=False)

    rat_pais_transferencia = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="País u organismo internacional receptor"
    )

    rat_plazo_conservacion = models.CharField(
        max_length=255,
        help_text="Plazo o criterio de conservación de datos",
        blank=True,
        null=True
    )

    rat_medidas_tecnicas = models.TextField(
        help_text="Medidas técnicas de seguridad aplicadas",
        blank=True,
        null=True
    )

    rat_medidas_organizativas = models.TextField(
        help_text="Medidas organizativas de seguridad aplicadas",
        blank=True,
        null=True
    )

    rat_responsable_tratamiento = models.CharField(
        max_length=255,
        help_text="Responsable del tratamiento",
        blank=True,
        null=True
    )



    rat_categoria_titulares = models.ManyToManyField(
    Group,
    blank=True,
    help_text="Grupos de usuarios que actúan como titulares de los datos",

    )

    # =====================================================
    # III. REGISTRO DE INCIDENTES DE SEGURIDAD Y MITIGACIÓN
    # =====================================================

    incidente_identificacion = models.CharField(
        max_length=255,
        help_text="Código o identificación del incidente",
        blank=True,
        null=True
    )

    incidente_fecha_deteccion = models.DateField(
        help_text="Fecha de detección del incidente",
        blank=True,
        null=True
    )

    incidente_descripcion = models.TextField(
        help_text="Descripción detallada del incidente",
        blank=True,
        null=True
    )

    incidente_tipo = models.CharField(
        max_length=100,
        help_text="Tipo de incidente (confidencialidad, integridad, disponibilidad)",
        blank=True,
        null=True
    )

    incidente_datos_afectados = models.TextField(
        help_text="Datos personales afectados",
        blank=True,
        null=True
    )

    incidente_titulares_afectados = models.TextField(
        help_text="Categoría de titulares afectados",
        blank=True,
        null=True
    )

    incidente_riesgo = models.CharField(
        max_length=100,
        help_text="Nivel de riesgo (bajo, medio, alto)",
        blank=True,
        null=True
    )

    incidente_notificado_spdp = models.BooleanField(
        default=False,
        help_text="¿El incidente fue notificado a la SPDP?"
    )

    incidente_fecha_notificacion = models.DateField(
        blank=True,
        null=True
    )

    incidente_medidas_mitigacion = models.TextField(
        help_text="Medidas de mitigación adoptadas",
        blank=True,
        null=True
    )

    incidente_medidas_correctivas = models.TextField(
        help_text="Medidas correctivas implementadas",
        blank=True,
        null=True
    )

    incidente_estado = models.CharField(
        max_length=50,
        choices=[
            ("abierto", "Abierto"),
            ("en_proceso", "En proceso"),
            ("cerrado", "Cerrado")
        ],
        blank=True,
        null=True
    )

    archivo_incidente = models.FileField(
        upload_to='spdp/incidentes/',
        blank=True,
        null=True
    )

    # =====================================================
    # CONTROL GENERAL
    # =====================================================

    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True,null=True, blank=True)
    fecha_expiracion = models.DateTimeField(
    null=True,
    blank=True,
    editable=False,
    help_text="Fecha automática de expiración (fecha de creación + 310 días)")

    legalizado_spd = models.BooleanField(default=False, verbose_name="Legalizado (SPDP)")


    hash_delegado = models.CharField(max_length=64, unique=True, null=True, blank=True)  # DPD
    hash_rat = models.CharField(max_length=64, unique=True, null=True, blank=True)       # RAT
    hash_incidente = models.CharField(max_length=64, unique=True, null=True, blank=True) # Incidente

    # =====================================================
    # 🔐 MÉTODOS DE GENERACIÓN DE HASH
    # =====================================================
    def _generate_hash(self, doc_type: str) -> str:
        """
        Genera un hash SHA-256 único para cada documento.
        Incluye id del registro, tipo de documento, UUID y timestamp.
        """
        raw = f"{self.id}|{doc_type}|{uuid.uuid4()}|{timezone.now().isoformat()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def generate_hash_delegado(self):
        self.hash_delegado = self._generate_hash("DPD")
        self.save(update_fields=["hash_delegado"])
        return self.hash_delegado

    def generate_hash_rat(self):
        self.hash_rat = self._generate_hash("RAT")
        self.save(update_fields=["hash_rat"])
        return self.hash_rat

    def generate_hash_incidente(self):
        self.hash_incidente = self._generate_hash("INCIDENTE")
        self.save(update_fields=["hash_incidente"])
        return self.hash_incidente

    # =====================================================
    # MÉTODOS DE UTILIDAD
    # =====================================================
    def get_qr_url_delegado(self):
        import qrcode, io, base64
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f"DPD-{self.id}-{self.hash_delegado}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    def get_qr_url_rat(self):
        import qrcode, io, base64
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f"RAT-{self.id}-{self.hash_rat}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"

    def get_qr_url_incidente(self):
        import qrcode, io, base64
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(f"INCIDENTE-{self.id}-{self.hash_incidente}")
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode()}"


    def get_document_name(self):
        return f"SPDP_{self.nombre_delegado}_{self.fecha_nombramiento.strftime('%Y%m%d')}"

    @property
    def dias_para_expirar(self):
        if self.fecha_expiracion and self.fecha_actualizacion:
            delta = self.fecha_expiracion - self.fecha_actualizacion
            return delta.days
        return None



    def save(self, *args, **kwargs):
        if self.fecha_creacion and not self.fecha_expiracion:
            self.fecha_expiracion = self.fecha_creacion + timedelta(days=310)
        super().save(*args, **kwargs)





    class Meta:
        verbose_name = "Registro: Superintendencia de Protección de Datos Personales (SPDP)"
        verbose_name_plural = "Registros: Superintendencia de Protección de Datos Personales (SPDP)"


# ===========================
# SRI - Servicio de Rentas Internas
# ===========================
class SRI_RUC(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='sri_ruc')
    ruc = models.CharField(max_length=13)
    fecha_emision = models.DateField()
    archivo = models.FileField(upload_to='sri/ruc/', blank=True, null=True)

    def get_document_name(self):
        return f"RUC_{self.ruc}_{self.fecha_emision.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "RUC SRI"
        verbose_name_plural = "RUC SRI"



class SRI_Retenciones(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='sri_retenciones')
    proveedor = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_emision = models.DateField()
    archivo = models.FileField(upload_to='sri/retenciones/', blank=True, null=True)

    def get_document_name(self):
        return f"Retencion_{self.proveedor}_{self.fecha_emision.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Retención SRI"
        verbose_name_plural = "Retenciones SRI"


from django.db import models

from django.db import models
from django.contrib.postgres.fields import JSONField  # Si usas PostgreSQL

from django.db import models


TIPO_IDENTIFICACION_CHOICES = [
    ("C", "Cédula"),
    ("R", "RUC"),
    ("P", "Pasaporte"),
    ("I", "Identificación exterior"),
]

SI_NO_CHOICES = [
    ("SI", "Sí"),
    ("NO", "No"),
]

TIPO_SUJETO_CHOICES = [
    ("01", "Persona Natural"),
    ("02", "Persona Jurídica"),
]

OTROS_MOTIVOS_CHOICES = [
    ("01", "Influencia significativa"),
    ("02", "Control indirecto"),
    ("03", "Relación contractual"),
    ("04", "Acuerdo de accionistas"),
    ("05", "Control familiar"),
    ("06", "Control indirecto de sociedad"),
    ("07", "Fideicomiso"),
    ("08", "Protector"),
    ("09", "Administrador o directivo"),
]

PROVINCIA_CHOICES = [
    ("001", "Azuay"),
    ("002", "Bolívar"),
    ("003", "Cañar"),
    ("004", "Carchi"),
    ("005", "Cotopaxi"),
    ("006", "Chimborazo"),
    ("007", "El Oro"),
    ("008", "Esmeraldas"),
    ("009", "Guayas"),
    ("010", "Imbabura"),
    ("011", "Loja"),
    ("012", "Los Ríos"),
    ("013", "Manabí"),
    ("014", "Morona Santiago"),
    ("015", "Napo"),
    ("016", "Pastaza"),
    ("017", "Pichincha"),
    ("018", "Tungurahua"),
    ("019", "Zamora Chinchipe"),
    ("020", "Galápagos"),
    ("021", "Sucumbíos"),
    ("022", "Orellana"),
    ("023", "Santo Domingo de los Tsáchilas"),
    ("024", "Santa Elena"),
]


class SRI_AnexosTributarios(models.Model):
    """
    MODELO ÚNICO DE ANEXOS TRIBUTARIOS SRI – ECUADOR
    Incluye: ATS, RDEP, Dividendos, Partes Relacionadas, Conciliación Tributaria
    y REBEFICS (Beneficiarios Finales y Composición Societaria).
    Cada campo cuenta con verbose_name y help_text para claridad.
    """

    # ==================================================
    # I. IDENTIFICACIÓN DEL CONTRIBUYENTE
    # ==================================================

    ruc = models.CharField(
        max_length=13,
        verbose_name="RUC",
        help_text="Registro Único de Contribuyentes de la sociedad, debe contener 13 dígitos sin guiones."
    )
    razon_social = models.CharField(
        max_length=255,
        verbose_name="Razón social",
        help_text="Nombre legal completo registrado ante el SRI."
    )
    ejercicio_fiscal = models.PositiveIntegerField(
        verbose_name="Ejercicio fiscal",
        help_text="Año fiscal al que corresponde la información reportada (formato YYYY)."
    )
    mes = models.PositiveIntegerField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        verbose_name="Mes",
        help_text="Mes al que corresponde el anexo (01=Enero, 12=Diciembre)."
    )
    obligado_contabilidad = models.BooleanField(
        default=True,
        verbose_name="Obligado a llevar contabilidad",
        help_text="Indica si el contribuyente está obligado a llevar contabilidad conforme normativa vigente."
    )

    # ==================================================
    # II. ATS – COMPRAS
    # ==================================================
    compras_tipo_comprobante = models.CharField(
        max_length=2, null=True, blank=True,
        help_text="Código del tipo de comprobante según catálogo del SRI (ej: 01=Factura, 04=Nota de Crédito)."
    )
    compras_tipo_id_proveedor = models.CharField(
        max_length=2, null=True, blank=True,
        help_text="Tipo de identificación del proveedor (04=RUC, 05=Cédula, 06=Pasaporte, etc.)."
    )
    compras_id_proveedor = models.CharField(
        max_length=13, null=True, blank=True,
        help_text="Número de identificación del proveedor sin guiones."
    )
    compras_razon_social_proveedor = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Razón social o nombres completos del proveedor."
    )
    compras_fecha_emision = models.DateField(
        null=True, blank=True,
        help_text="Fecha de emisión del comprobante de compra."
    )
    compras_establecimiento = models.CharField(
        max_length=3, null=True, blank=True,
        help_text="Código de establecimiento del comprobante (3 dígitos)."
    )
    compras_punto_emision = models.CharField(
        max_length=3, null=True, blank=True,
        help_text="Código de punto de emisión del comprobante (3 dígitos)."
    )
    compras_secuencial = models.CharField(
        max_length=9, null=True, blank=True,
        help_text="Número secuencial del comprobante (9 dígitos)."
    )
    compras_autorizacion = models.CharField(
        max_length=49, null=True, blank=True,
        help_text="Número de autorización electrónica del comprobante."
    )
    compras_base_no_objeto_iva = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Base imponible no objeto de IVA."
    )
    compras_base_iva_0 = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Base imponible gravada con tarifa 0% de IVA."
    )
    compras_base_iva = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Base imponible gravada con tarifa diferente de 0%."
    )
    compras_monto_iva = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Valor del IVA pagado en la compra."
    )
    compras_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Valor total del comprobante de compra (incluye impuestos)."
    )

    # ==================================================
    # III. ATS – RETENCIONES
    # ==================================================
    retencion_ir_codigo = models.CharField(
        max_length=3, null=True, blank=True,
        help_text="Código de retención en la fuente de Impuesto a la Renta según tabla del SRI."
    )
    retencion_ir_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Porcentaje aplicado de retención en la fuente de Impuesto a la Renta."
    )
    retencion_ir_valor = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Valor retenido por concepto de Impuesto a la Renta."
    )
    retencion_iva_codigo = models.CharField(
        max_length=3, null=True, blank=True,
        help_text="Código de retención de IVA según catálogo del SRI."
    )
    retencion_iva_porcentaje = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Porcentaje de retención de IVA aplicado."
    )
    retencion_iva_valor = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Valor retenido por concepto de IVA."
    )

    # ==================================================
    # IV. ATS – VENTAS (CORREGIDO)
    # ==================================================
    ventas_tipo_id_cliente = models.CharField(
        max_length=2, null=True, blank=True,
        help_text="Tipo de identificación del cliente (04=RUC, 05=Cédula, etc.)."
    )
    ventas_id_cliente = models.CharField(
        max_length=13, null=True, blank=True,
        help_text="Número de identificación del cliente."
    )
    ventas_razon_social_cliente = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Razón social o nombres completos del cliente."
    )
    ventas_base_iva_0 = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Base imponible de ventas gravadas con tarifa 0% de IVA."
    )
    ventas_base_iva = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Base imponible de ventas gravadas con tarifa diferente de 0%."
    )
    ventas_porcentaje_iva = models.DecimalField(
        max_digits=5, decimal_places=2, default=12,
        help_text="Porcentaje de IVA aplicado sobre la base imponible gravada (ej: 12%)."
    )
    ventas_monto_iva = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Valor total de IVA generado en las ventas. Debe ser igual a ventas_base_iva * porcentaje_iva."
    )
    ventas_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,null=True,blank=True,
        help_text="Valor total facturado al cliente, incluyendo impuestos. Debe ser ventas_base_iva_0 + ventas_base_iva + ventas_monto_iva."
    )


    FORMA_COBRO_CHOICES = [
    ('01', 'Sin utilización del sistema financiero'),
    ('15', 'Compensación'),
    ('16', 'Tarjeta de débito'),
    ('17', 'Dinero electrónico'),
    ('18', 'Tarjeta prepago'),
    ('19', 'Tarjeta de crédito'),
    ('20', 'Transferencia bancaria'),
    ('21', 'Cheque'),
    ('24', 'Otros con utilización del sistema financiero'),
    ]

    ventas_forma_cobro = models.CharField(
        max_length=2,
        choices=FORMA_COBRO_CHOICES,
        null=True,
        blank=True,
        help_text=(
        "Forma de cobro utilizada en la venta según catálogo ATS del SRI. "
        "Obligatorio desde junio 2016 cuando el comprobante es electrónico. "
        "Códigos válidos: "
        "01=Sin sistema financiero, "
        "15=Compensación, "
        "16=Tarjeta débito, "
        "17=Dinero electrónico, "
        "18=Tarjeta prepago, "
        "19=Tarjeta crédito, "
        "20=Transferencia bancaria, "
        "21=Cheque, "
        "24=Otros con sistema financiero."
        )
    )


    ventas_compensacion_ley_solidaridad = models.DecimalField(
        max_digits=18, decimal_places=2, default=0,
        help_text="Valor de compensaciones de ventas por Ley de Solidaridad aplicado al establecimiento."
    )



    # ==================================================
    # V. RDEP – RELACIÓN DE DEPENDENCIA
    # ==================================================
    tiene_empleados = models.BooleanField(
        default=False,
        help_text="Indica si la empresa tuvo empleados en relación de dependencia durante el ejercicio fiscal."
    )
    empleado_tipo_id = models.CharField(
        max_length=2, null=True, blank=True,
        help_text="Tipo de identificación del empleado."
    )
    empleado_identificacion = models.CharField(
        max_length=13, null=True, blank=True,
        help_text="Número de identificación del empleado."
    )
    empleado_nombres = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Nombres completos del empleado."
    )
    empleado_cargo = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Cargo o puesto desempeñado por el empleado."
    )
    empleado_sueldo_anual = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Total de ingresos gravados percibidos por el empleado en el año."
    )
    empleado_aporte_iess = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Valor total aportado al IESS por el empleado."
    )
    empleado_ir_retenido = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Impuesto a la Renta retenido al empleado durante el ejercicio fiscal."
    )

    # ==================================================
    # VI. DIVIDENDOS
    # ==================================================
    distribuyo_dividendos = models.BooleanField(
        default=False,
        help_text="Indica si la sociedad distribuyó dividendos a sus socios."
    )
    socio_tipo_id = models.CharField(
        max_length=2, null=True, blank=True,
        help_text="Tipo de identificación del socio/accionista."
    )
    socio_identificacion = models.CharField(
        max_length=13, null=True, blank=True,
        help_text="Número de identificación del socio/accionista."
    )
    socio_nombre = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Nombre completo del socio/accionista."
    )
    socio_porcentaje_participacion = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text="Porcentaje de participación del socio/accionista."
    )
    dividendo_pagado = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto total de dividendos pagados al socio."
    )
    impuesto_dividendo = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Impuesto retenido sobre los dividendos distribuidos."
    )

    # ==================================================
    # VII. PARTES RELACIONADAS
    # ==================================================
    tiene_partes_relacionadas = models.BooleanField(
        default=False,
        help_text="Indica si la sociedad realizó operaciones con partes relacionadas."
    )
    parte_relacionada_identificacion = models.CharField(
        max_length=13, null=True, blank=True,
        help_text="Número de identificación de la parte relacionada."
    )
    parte_relacionada_nombre = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Nombre de la parte relacionada."
    )
    monto_operacion_parte_relacionada = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto total de operaciones realizadas con la parte relacionada."
    )
    tipo_operacion = models.CharField(
        max_length=100, null=True, blank=True,
        help_text="Tipo de operación realizada con la parte relacionada."
    )

    # ==================================================
    # VIII. CONCILIACIÓN TRIBUTARIA
    # ==================================================
    utilidad_contable = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Resultado contable antes de ajustes fiscales."
    )
    gastos_no_deducibles = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Total de gastos contables no deducibles fiscalmente."
    )
    ingresos_exentos = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Ingresos que están exentos del Impuesto a la Renta."
    )
    base_imponible = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Base imponible determinada para el cálculo del Impuesto a la Renta."
    )
    impuesto_renta_causado = models.DecimalField(
        max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto del Impuesto a la Renta causado según la base imponible."
    )

    # ==================================================
    # IX. FIRMAS Y RESPONSABILIDAD
    # ==================================================
    representante_legal = models.CharField(
        max_length=255,
        help_text="Nombre completo del representante legal de la sociedad."
    )
    contador = models.CharField(
        max_length=255,
        help_text="Nombre completo del contador responsable."
    )
    fecha_certificacion = models.DateField(
        help_text="Fecha en la que se certifica la información reportada."
    )

    tipo_sociedad = models.CharField(
        max_length=2,
        null=True, blank=True,
        verbose_name="Tipo de Sociedad",
        help_text="Código de tipo de sociedad según Tabla 1 del SRI (2 caracteres)."
    )

    porcentaje_accionario_no_bolsa = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True, blank=True,
        verbose_name="Porcentaje Accionario No Bolsa",
        help_text="Porcentaje accionario que NO negocia en bolsa (hasta 3 enteros y 6 decimales)."
    )

    codigo_operativo = models.CharField(
        max_length=3,
        null=True, blank=True,
        verbose_name="Código Operativo",
        help_text="Código operativo de 3 caracteres según instructivo REBEFICS."
    )

    porcentaje_accionario_bolsa = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True, blank=True,
        verbose_name="Porcentaje Accionario Bolsa",
        help_text="Porcentaje accionario que negocia en bolsa (hasta 3 enteros y 6 decimales)."
    )

    anticipada = models.CharField(
        max_length=4,
        null=True, blank=True,
        verbose_name="Anticipada",
        help_text="Año de declaración anticipada en formato YYYY."
    )

    tipo_declaracion = models.CharField(
        max_length=2,
        null=True, blank=True,
        verbose_name="Tipo de Declaración",
        help_text="Código según Tabla 8 del SRI (2 caracteres)."
    )

    # ==================================================
    # BENEFICIARIO FINAL
    # ==================================================

    bf_tipo_identificacion = models.CharField(
        "Tipo de identificación del beneficiario final",
        max_length=1,
        choices=TIPO_IDENTIFICACION_CHOICES,
        blank=True,
        null=True,
        help_text="Tipo de documento de identificación del beneficiario final (cédula, RUC, pasaporte o identificación exterior).",
    )

    bf_identificacion = models.CharField(
        "Número de identificación del beneficiario final",
        max_length=13,
        blank=True,
        null=True,
        help_text="Número de identificación del beneficiario final conforme al tipo seleccionado."
    )

    bf_primer_nombre = models.CharField(
        "Primer nombre",
        max_length=100,
        blank=True,
        null=True,
        help_text="Primer nombre del beneficiario final."
    )

    bf_segundo_nombre = models.CharField(
        "Segundo nombre",
        max_length=100,
        blank=True,
        null=True,
        help_text="Segundo nombre del beneficiario final, si aplica."
    )

    bf_primer_apellido = models.CharField(
        "Primer apellido",
        max_length=100,
        blank=True,
        null=True,
        help_text="Primer apellido del beneficiario final."
    )

    bf_segundo_apellido = models.CharField(
        "Segundo apellido",
        max_length=100,
        blank=True,
        null=True,
        help_text="Segundo apellido del beneficiario final, si aplica."
    )

    bf_fecha_nacimiento = models.DateField(
        "Fecha de nacimiento",
        blank=True,
        null=True,
        help_text="Fecha de nacimiento del beneficiario final."
    )

    bf_residencia_fiscal = models.CharField(
        "País de residencia fiscal",
        max_length=3,
        blank=True,
        null=True,
        help_text="Código numérico del país de residencia fiscal según estándar ISO (por ejemplo: 593 para Ecuador)."
    )

    bf_nacionalidad_uno = models.CharField(
        "Primera nacionalidad",
        max_length=3,
        blank=True,
        null=True,
        help_text="Código numérico del país correspondiente a la nacionalidad principal del beneficiario final."
    )

    bf_nacionalidad_dos = models.CharField(
        "Segunda nacionalidad",
        max_length=3,
        blank=True,
        null=True,
        help_text="Código numérico del país correspondiente a una segunda nacionalidad, si aplica."
    )

    # ==================================================
    # DOMICILIO
    # ==================================================

    bf_provincia = models.CharField(
        "Provincia de residencia",
        max_length=5,
        choices=PROVINCIA_CHOICES,
        blank=True,
        null=True,
        help_text="Provincia del domicilio del beneficiario final dentro del Ecuador."
    )

    bf_ciudad = models.CharField(
            "Ciudad",
            max_length=5,
            blank=True,
            null=True,
            help_text="Código de ciudad según la división política administrativa del Ecuador."
    )

    bf_canton = models.CharField(
        "Cantón",
        max_length=5,
        blank=True,
        null=True,
        help_text="Código del cantón según la división política administrativa del Ecuador."
    )

    bf_parroquia = models.CharField(
        "Parroquia",
        max_length=7,
        blank=True,
        null=True,
        help_text="Código de parroquia conforme al catálogo territorial del INEC."
    )

    bf_calle = models.CharField(
        "Calle principal",
        max_length=100,
        blank=True,
        null=True,
        help_text="Nombre de la calle principal del domicilio del beneficiario final."
    )

    bf_numero = models.CharField(
        "Número de domicilio",
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de casa, edificio o lote del domicilio."
    )

    bf_interseccion = models.CharField(
        "Intersección",
        max_length=100,
        blank=True,
        null=True,
        help_text="Nombre de la calle transversal o intersección."
    )

    bf_codigo_postal = models.CharField(
        "Código postal",
        max_length=10,
        blank=True,
        null=True,
        help_text="Código postal correspondiente al domicilio."
    )

    bf_referencia = models.CharField(
        "Referencia de ubicación",
        max_length=255,
        blank=True,
        null=True,
        help_text="Referencia adicional para ubicar el domicilio (ejemplo: edificio, oficina, referencia cercana)."
    )

    # ==================================================
    # CONTROL DEL BENEFICIARIO FINAL
    # ==================================================

    bf_porcentaje_participacion = models.DecimalField(
        "Porcentaje de participación",
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Porcentaje de participación directa o indirecta del beneficiario final en la sociedad."
    )

    bf_por_propiedad = models.CharField(
        "Control por propiedad",
        max_length=2,
        choices=SI_NO_CHOICES,
        blank=True,
        null=True,
        help_text="Indica si el beneficiario final ejerce control a través de participación accionaria."
    )

    bf_por_administracion = models.CharField(
        "Control por administración",
        max_length=2,
        choices=SI_NO_CHOICES,
        blank=True,
        null=True,
        help_text="Indica si el beneficiario final ejerce control mediante funciones de administración o dirección."
    )

    bf_por_otros_motivos = models.CharField(
        "Otros motivos de control",
        max_length=2,
        choices=OTROS_MOTIVOS_CHOICES,
        blank=True,
        null=True,
        help_text="Código que identifica otros motivos por los cuales se considera beneficiario final."
    )

    # ==================================================
    # DIVIDENDOS
    # ==================================================

    distribuyo_dividendos = models.CharField(
        "Distribución de dividendos",
        max_length=2,
        choices=SI_NO_CHOICES,
        blank=True,
        null=True,
        help_text="Indica si durante el ejercicio fiscal se distribuyeron dividendos al beneficiario final."
    )

    dividendo_pagado = models.DecimalField(
        "Monto de dividendos pagados",
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Monto total de dividendos pagados al beneficiario final durante el ejercicio fiscal."
    )

    impuesto_dividendo = models.DecimalField(
        "Impuesto retenido por dividendos",
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Valor del impuesto retenido sobre los dividendos distribuidos."
    )

    # ==================================================
    # COMPOSICIÓN SOCIETARIA
    # ==================================================

    socio_tipo_identificacion = models.CharField(
        "Tipo de identificación del socio",
        max_length=1,
        choices=TIPO_IDENTIFICACION_CHOICES,
        blank=True,
        null=True,
        help_text="Tipo de identificación del socio o accionista de la compañía."
    )

    socio_identificacion = models.CharField(
        "Identificación del socio",
        max_length=13,
        blank=True,
        null=True,
        help_text="Número de identificación del socio o accionista."
    )

    socio_nombre = models.CharField(
        "Nombre o razón social del socio",
        max_length=255,
        blank=True,
        null=True,
        help_text="Nombre completo o razón social del socio o accionista."
    )

    socio_tipo_sujeto = models.CharField(
        "Tipo de sujeto",
        max_length=2,
        choices=TIPO_SUJETO_CHOICES,
        blank=True,
        null=True,
        help_text="Tipo de sujeto del socio: persona natural o persona jurídica."
    )

    socio_porcentaje = models.DecimalField(
        "Porcentaje de participación del socio",
        max_digits=9,
        decimal_places=6,
        blank=True,
        null=True,
        help_text="Porcentaje de participación accionaria del socio o accionista dentro de la compañía."
    )

    # ==================================================
    # XI. METADATA
    # ==================================================
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de creación del registro."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Fecha y hora de la última actualización del registro."
    )



    def calcular_totales_ventas(self):
        base_0 = Decimal(self.ventas_base_iva_0 or 0)
        base_12 = Decimal(self.ventas_base_iva or 0)
        porcentaje = Decimal(self.ventas_porcentaje_iva or 0)

        self.ventas_monto_iva = (base_12 * porcentaje / Decimal("100")).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)
        self.ventas_total = (base_0 + base_12).quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)


    class Meta:
        verbose_name = "Anexo: Servicios De Rentas Internas (SRI)"
        verbose_name_plural = "Anexos: Servicios De Rentas Internas (SRI)"
        ordering = ["-ejercicio_fiscal", "-mes"]
        indexes = [
            models.Index(fields=["ruc", "ejercicio_fiscal", "mes"]),
        ]

    def __str__(self):
        return f"{self.ruc} – Anexos SRI {self.ejercicio_fiscal}-{self.mes:02d}"



# ===========================
# Ministerio de Trabajo
# ===========================
class MT_Contratos(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='mt_contratos')
    empleado = models.CharField(max_length=255)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    tipo_contrato = models.CharField(max_length=100)
    archivo = models.FileField(upload_to='mt/contratos/', blank=True, null=True)

    def get_document_name(self):
        return f"Contrato_{self.empleado}_{self.fecha_inicio.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Contrato MT"
        verbose_name_plural = "Contratos MT"

class MT_Nominas(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='mt_nominas')
    empleado = models.CharField(max_length=255)
    periodo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateField()
    archivo = models.FileField(upload_to='mt/nominas/', blank=True, null=True)

    def get_document_name(self):
        return f"Nomina_{self.empleado}_{self.periodo}"

    class Meta:
        verbose_name = "Nómina MT"
        verbose_name_plural = "Nóminas MT"

class MT_Planillas(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='mt_planillas')
    tipo_planilla = models.CharField(max_length=255)
    periodo = models.CharField(max_length=20)
    fecha_presentacion = models.DateField()
    archivo = models.FileField(upload_to='mt/planillas/', blank=True, null=True)

    def get_document_name(self):
        return f"Planilla_{self.tipo_planilla}_{self.periodo}"

    class Meta:
        verbose_name = "Planilla MT"
        verbose_name_plural = "Planillas MT"

# ===========================
# IESS - Instituto Ecuatoriano de Seguridad Social
# ===========================
class IESS_Afiliaciones(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='iess_afiliaciones')
    empleado = models.CharField(max_length=255)
    fecha_afiliacion = models.DateField()
    archivo = models.FileField(upload_to='iess/afiliaciones/', blank=True, null=True)

    def get_document_name(self):
        return f"Afiliacion_{self.empleado}_{self.fecha_afiliacion.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Afiliación IESS"
        verbose_name_plural = "Afiliaciones IESS"

class IESS_Aportes(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='iess_aportes')
    empleado = models.CharField(max_length=255)
    periodo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_pago = models.DateField()
    archivo = models.FileField(upload_to='iess/aportes/', blank=True, null=True)

    def get_document_name(self):
        return f"Aporte_{self.empleado}_{self.periodo}"

    class Meta:
        verbose_name = "Aporte IESS"
        verbose_name_plural = "Aportes IESS"

class IESS_HistorialAportes(models.Model):
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='iess_historial')
    empleado = models.CharField(max_length=255)
    periodo = models.CharField(max_length=20)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    archivo = models.FileField(upload_to='iess/historial/', blank=True, null=True)

    def get_document_name(self):
        return f"HistorialAporte_{self.empleado}_{self.periodo}"

    class Meta:
        verbose_name = "Historial de Aportes IESS"
        verbose_name_plural = "Historiales de Aportes IESS"



from django.db import models
from decimal import Decimal


from django.db import models
from decimal import Decimal


class SRI_DeclaracionImpuestos(models.Model):

    # =====================
    # RÉGIMEN TRIBUTARIO
    # =====================
    REGIMEN_CHOICES = (
        ('RIMPE_EMPRENDEDOR', 'RIMPE Emprendedor'),
        ('RIMPE_POPULAR', 'RIMPE Negocio Popular'),
        ('REGIMEN_GENERAL', 'Régimen General'),
    )

    # =====================
    # DATOS GENERALES
    # =====================
    ruc = models.CharField(
        max_length=13,
        verbose_name="RUC",
        help_text="Registro Único de Contribuyentes del sujeto pasivo.",
        null=True, blank=True
    )

    razon_social = models.CharField(
        max_length=255,
        verbose_name="Razón social",
        help_text="Nombre o razón social del contribuyente.",
        null=True, blank=True
    )

    regimen = models.CharField(
        max_length=20,
        choices=REGIMEN_CHOICES,
        verbose_name="Régimen tributario",
        help_text="Régimen tributario registrado ante el SRI.",
        null=True, blank=True
    )

    ejercicio_fiscal = models.PositiveIntegerField(
        verbose_name="Ejercicio fiscal",
        help_text="Año fiscal al que corresponde la información.",
        null=True, blank=True
    )
    mes = models.PositiveIntegerField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        verbose_name="Mes",
        help_text="Mes correspondiente a los anexos (01=Enero, 12=Diciembre).",
        null=True, blank=True
    )

    fecha_declaracion = models.DateField(
        verbose_name="Fecha de declaración",
        help_text="Fecha de presentación de la declaración.",
        null=True, blank=True
    )

    # =====================
    # IVA
    # =====================
    iva_ventas = models.DecimalField(
        max_digits=14, decimal_places=2,
        verbose_name="IVA en ventas",
        help_text="IVA causado por ventas gravadas.",
        null=True, blank=True
    )

    iva_compras = models.DecimalField(
        max_digits=14, decimal_places=2,
        verbose_name="IVA en compras",
        help_text="IVA pagado en compras con derecho a crédito tributario.",
        null=True, blank=True
    )

    iva_a_pagar = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False,
        verbose_name="IVA a pagar",
        help_text="IVA a pagar calculado automáticamente.",
        null=True, blank=True
    )

    # =====================
    # IMPUESTO A LA RENTA
    # =====================
    ingresos_gravados = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name="Ingresos gravados",
        help_text="Ingresos sujetos a Impuesto a la Renta.",
        null=True, blank=True
    )

    costos_gastos_deducibles = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name="Costos y gastos deducibles",
        help_text="Costos y gastos deducibles según normativa.",
        null=True, blank=True
    )

    base_imponible_renta = models.DecimalField(
        max_digits=16, decimal_places=2, editable=False,
        verbose_name="Base imponible del Impuesto a la Renta",
        help_text="Base imponible calculada automáticamente.",
        null=True, blank=True
    )

    impuesto_renta_causado = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name="Impuesto a la Renta causado",
        help_text="Impuesto determinado antes de créditos.",
        null=True, blank=True
    )

    anticipos_renta = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name="Anticipos y créditos tributarios",
        help_text="Anticipos y créditos aplicables.",
        null=True, blank=True
    )

    renta_a_pagar = models.DecimalField(
        max_digits=16, decimal_places=2, editable=False,
        verbose_name="IR a pagar",
        help_text="Valor final del Impuesto a la Renta.",
        null=True, blank=True
    )

    # =====================
    # RETENCIONES
    # =====================
    retencion_iva = models.DecimalField(
        max_digits=14, decimal_places=2,
        verbose_name="Retención de IVA",
        help_text="IVA retenido a terceros.",
        null=True, blank=True
    )

    retencion_renta = models.DecimalField(
        max_digits=14, decimal_places=2,
        verbose_name="RT a pagar",
        help_text="Retenciones de Impuesto a la Renta practicadas.",
        null=True, blank=True
    )

    # =====================
    # ICE
    # =====================
    ice_causado = models.DecimalField(
        max_digits=14, decimal_places=2,
        verbose_name="Impuesto a los Consumos Especiales (ICE)",
        help_text="ICE causado según actividad económica.",
        null=True, blank=True
    )

    # =====================
    # ISD
    # =====================
    pagos_exterior = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name="Pagos al exterior",
        help_text="Pagos sujetos a ISD.",
        null=True, blank=True
    )

    isd_causado = models.DecimalField(
        max_digits=14, decimal_places=2, editable=False,
        verbose_name="ISD a pagar",
        help_text="ISD calculado automáticamente (5%).",
        null=True, blank=True
    )

    # =====================
    # PATENTE MUNICIPAL
    # =====================
    base_patente = models.DecimalField(
        max_digits=16, decimal_places=2,
        verbose_name="Base imponible de patente municipal",
        help_text="Base imponible para patente municipal.",
        null=True, blank=True
    )

    patente_municipal = models.DecimalField(
        max_digits=14, decimal_places=2,
        verbose_name="PM a pagar",
        help_text="Valor anual de la patente municipal.",
        null=True, blank=True
    )

    # =====================
    # AUDITORÍA
    # =====================
    cp = models.DecimalField(
        max_digits=25, decimal_places=2,
        verbose_name="N. Comprobante (CP)",
        help_text="Número de comprobante de pago asociad.",
        null=True, blank=True
    )
    archivo_auditoria = models.FileField(
        upload_to='sri/declaraciones/auditoria/',
        verbose_name="Archivo de auditoría",
        null=True, blank=True
    )
    declarado = models.BooleanField(default=False, verbose_name="Declarado",null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    actualizado_en = models.DateTimeField(auto_now=True, null=True, blank=True)


    class Meta:
        verbose_name = "Declaracion: Servicio de Rentas Internas (SRI)"
        verbose_name_plural = "Declaraciones: Servicio de Rentas Internas (SRI)"
        ordering = ["-creado_en"]

    # =====================
    # CÁLCULOS AUTOMÁTICOS
    # =====================
    def save(self, *args, **kwargs):

        iva_ventas = self.iva_ventas or Decimal('0.00')
        iva_compras = self.iva_compras or Decimal('0.00')
        ingresos = self.ingresos_gravados or Decimal('0.00')
        costos = self.costos_gastos_deducibles or Decimal('0.00')
        impuesto_renta = self.impuesto_renta_causado or Decimal('0.00')
        anticipos = self.anticipos_renta or Decimal('0.00')
        pagos_exterior = self.pagos_exterior or Decimal('0.00')

        # IVA
        if self.regimen != 'RIMPE_POPULAR':
            self.iva_a_pagar = max(iva_ventas - iva_compras, Decimal('0.00'))
        else:
            self.iva_a_pagar = Decimal('0.00')

        # Impuesto a la Renta
        if self.regimen == 'REGIMEN_GENERAL':
            self.base_imponible_renta = max(ingresos - costos, Decimal('0.00'))
            self.renta_a_pagar = max(impuesto_renta - anticipos, Decimal('0.00'))
        else:
            self.base_imponible_renta = Decimal('0.00')
            self.renta_a_pagar = Decimal('0.00')

        # ISD (5%)
        self.isd_causado = (pagos_exterior * Decimal('0.05')).quantize(Decimal('0.01'))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.razon_social or 'Sin nombre'} - {self.ejercicio_fiscal or 'ejercicio'}-{self.mes or 'mes' if self.mes else '00'}"





from django.db import models
import uuid
import hashlib
from django.db import models
from django.utils.timezone import now


class ContratoLaboral(models.Model):
    """
    MODELO INTEGRAL DE CONTRATO LABORAL – ECUADOR
    Conforme al Código del Trabajo, Ministerio de Trabajo e IESS.
    Permite generar contrato PDF, registro SUT y respaldo legal.
    """

    # ==================================================
    # I. IDENTIFICACIÓN DEL EMPLEADOR
    # ==================================================
    empleador_razon_social = models.CharField(
        max_length=255,
        verbose_name="Razón social del empleador",
        help_text="Nombre legal completo de la empresa o persona empleadora."
    )

    empleador_ruc = models.CharField(
        max_length=13,
        verbose_name="RUC del empleador",
        help_text="Registro Único de Contribuyentes del empleador."
    )

    empleador_representante_legal = models.CharField(
        max_length=255,
        verbose_name="Representante legal",
        help_text="Nombre completo del representante legal del empleador."
    )

    empleador_domicilio = models.TextField(
        verbose_name="Domicilio del empleador",
        help_text="Dirección completa del empleador."
    )

    # ==================================================
    # II. IDENTIFICACIÓN DEL TRABAJADOR
    # ==================================================
    trabajador_nombres = models.CharField(
        max_length=255,
        verbose_name="Trabajador",
        help_text="Nombres y apellidos completos del trabajador."
    )

    trabajador_identificacion = models.CharField(
        max_length=13,
        verbose_name="Número de identificación",
        help_text="Número de cédula o pasaporte del trabajador."
    )

    trabajador_nacionalidad = models.CharField(
        max_length=100,
        verbose_name="Nacionalidad",
        help_text="Nacionalidad del trabajador."
    )

    trabajador_estado_civil = models.CharField(
        max_length=50,
        verbose_name="Estado civil",
        help_text="Estado civil del trabajador."
    )

    trabajador_domicilio = models.TextField(
        verbose_name="Domicilio del trabajador",
        help_text="Dirección domiciliaria del trabajador."
    )

    # ==================================================
    # III. DATOS DEL CONTRATO
    # ==================================================
    TIPO_CONTRATO = [
        ("INDEFINIDO", "Contrato por tiempo indefinido"),
        ("PLAZO_FIJO", "Contrato a plazo fijo"),
        ("OCASIONAL", "Contrato ocasional"),
        ("OBRA", "Contrato por obra o servicio"),
        ("JORNADA_PARCIAL", "Contrato de jornada parcial"),
    ]

    tipo_contrato = models.CharField(
        max_length=20,
        choices=TIPO_CONTRATO,
        verbose_name="Tipo de contrato",
        help_text="Tipo de contrato conforme al Código del Trabajo."
    )

    fecha_inicio = models.DateField(
        verbose_name="Fecha de inicio",
        help_text="Fecha de inicio de la relación laboral."
    )

    fecha_fin = models.DateField(
        null=True, blank=True,
        verbose_name="Fecha de finalización",
        help_text="Fecha de terminación del contrato, si aplica."
    )

    duracion_contrato = models.CharField(
        max_length=100,
        null=True, blank=True,
        verbose_name="Duración del contrato",
        help_text="Plazo del contrato en meses o días, si aplica."
    )

    # ==================================================
    # IV. CARGO Y FUNCIONES
    # ==================================================
    cargo = models.CharField(
        max_length=255,
        verbose_name="Cargo",
        help_text="Cargo o puesto de trabajo del trabajador."
    )

    area_trabajo = models.CharField(
        max_length=255,
        verbose_name="Área o departamento",
        help_text="Área o departamento donde desempeña sus funciones."
    )

    funciones = models.TextField(
        verbose_name="Funciones del cargo",
        help_text="Descripción detallada de las funciones del trabajador."
    )

    lugar_trabajo = models.CharField(
        max_length=255,
        verbose_name="Lugar de trabajo",
        help_text="Lugar donde se ejecutarán las labores."
    )

    # ==================================================
    # V. JORNADA LABORAL
    # ==================================================
    JORNADA = [
        ("COMPLETA", "Jornada completa"),
        ("PARCIAL", "Jornada parcial"),
        ("NOCTURNA", "Jornada nocturna"),
        ("MIXTA", "Jornada mixta"),
    ]

    tipo_jornada = models.CharField(
        max_length=20,
        choices=JORNADA,
        verbose_name="Tipo de jornada",
        help_text="Tipo de jornada laboral conforme a la ley."
    )

    horas_semanales = models.PositiveIntegerField(
        verbose_name="Horas semanales",
        help_text="Número de horas laboradas a la semana.",
        null=True, blank=True
    )

    horario = models.CharField(
        max_length=255,
        verbose_name="Horario de trabajo",
        help_text="Horario habitual de trabajo (ej. 08h00 a 17h00).",
        null=True, blank=True
    )

    # ==================================================
    # VI. REMUNERACIÓN
    # ==================================================
    salario_mensual = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Salario mensual",
        help_text="Remuneración mensual en dólares, nunca inferior al SBU."
    )

    forma_pago = models.CharField(
        max_length=100,
        verbose_name="Forma de pago",
        help_text="Forma de pago del salario (transferencia, cheque, efectivo)."
    )

    beneficios_adicionales = models.TextField(
        null=True, blank=True,
        verbose_name="Beneficios adicionales",
        help_text="Bonos, comisiones u otros beneficios contractuales."
    )

    # ==================================================
    # VII. APORTES Y OBLIGACIONES LEGALES
    # ==================================================
    afiliacion_iess = models.BooleanField(
        default=True,
        verbose_name="Afiliación al IESS",
        help_text="Indica si el trabajador será afiliado al IESS."
    )

    decimo_tercer_sueldo = models.BooleanField(
        default=True,
        verbose_name="Décimo tercer sueldo",
        help_text="Indica si el trabajador recibe décimo tercer sueldo."
    )

    decimo_cuarto_sueldo = models.BooleanField(
        default=True,
        verbose_name="Décimo cuarto sueldo",
        help_text="Indica si el trabajador recibe décimo cuarto sueldo."
    )

    vacaciones_anuales = models.PositiveIntegerField(
        default=15,
        verbose_name="Vacaciones anuales",
        help_text="Número de días de vacaciones anuales conforme a la ley."
    )

    # ==================================================
    # VIII. CONFIDENCIALIDAD Y PROHIBICIONES
    # ==================================================
    clausula_confidencialidad = models.BooleanField(
        default=True,
        verbose_name="Cláusula de confidencialidad",
        help_text="Indica si el contrato incluye cláusula de confidencialidad."
    )

    clausula_no_competencia = models.BooleanField(
        default=False,
        verbose_name="Cláusula de no competencia",
        help_text="Indica si existe cláusula de no competencia."
    )

    # ==================================================
    # IX. TERMINACIÓN DEL CONTRATO
    # ==================================================
    causales_terminacion = models.TextField(
        verbose_name="Causales de terminación",
        help_text="Causales de terminación conforme al Código del Trabajo."
    )

    # ==================================================
    # X. FIRMAS Y FORMALIDADES
    # ==================================================
    lugar_firma = models.CharField(
        max_length=255,
        verbose_name="Lugar de suscripción",
        help_text="Ciudad donde se suscribe el contrato."
    )

    fecha_firma = models.DateField(
        verbose_name="Fecha de suscripción",
        help_text="Fecha de firma del contrato laboral."
    )

    empleador_firma = models.CharField(
        max_length=255,
        verbose_name="Firma del empleador",
        help_text="Nombre del representante que firma el contrato."
    )

    trabajador_firma = models.CharField(
        max_length=255,
        verbose_name="Firma del trabajador",
        help_text="Nombre del trabajador firmante."
    )

    # ==================================================
    # XI. METADATA
    # ==================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # ==================================================
    # XII. HASH DE CERTIFICACIÓN
    # ==================================================
    hash_contrato = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        verbose_name="Hash único del contrato",
        help_text="Hash SHA-256 único que certifica la integridad del contrato.",
        null=True, blank=True
    )
    legalizado = models.BooleanField(
        default=False,
        verbose_name="Contrato legalizado",
        help_text="Indica si el contrato ha sido legalizado ante el Ministerio de Trabajo."
    )
    ID_SUT_registro = models.CharField(
        max_length=50,
        null=True, blank=True,
        verbose_name="ID de registro SUT",
        help_text="Identificador del registro del contrato en el Sistema Único de Trabajadores (SUT)."
    )






    class Meta:
        verbose_name = "Contrato Laboral"
        verbose_name_plural = "Contratos Laborales"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.ID_SUT_registro}"

    def save(self, *args, **kwargs):
        if not self.hash_contrato:
            raw = f"{self.empleador_ruc}|{self.trabajador_identificacion}|{self.fecha_inicio}|{uuid.uuid4()}|{now().isoformat()}"
            self.hash_contrato = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)






from django.db import models
from decimal import Decimal


from django.db import models
from decimal import Decimal
import uuid, hashlib
from django.utils.timezone import now


from decimal import Decimal
from django.utils.timezone import now
import uuid
import hashlib
from django.db import models
from djmoney.models.fields import MoneyField

class Nomina(models.Model):
    """
    Modelo único de nómina compatible con:
    - IESS
    - Ministerio de Trabajo (Ecuador)
    """

    # =======================
    # DATOS DEL EMPLEADOR
    # =======================
    ruc_empleador = models.CharField(max_length=13, null=True, blank=True,
        verbose_name="RUC del empleador",
        help_text="Número de RUC registrado en el SRI y el IESS."
    )

    razon_social = models.CharField(max_length=255, null=True, blank=True,
        verbose_name="Razón social",
        help_text="Nombre legal de la empresa empleadora."
    )

    # =======================
    # DATOS DEL EMPLEADO
    # =======================

    # =======================
    # CONTRATO
    # =======================


    contrato = models.ForeignKey('ContratoLaboral', on_delete=models.CASCADE, related_name='nominas',
        unique=True,
        null=True, blank=True,
        verbose_name="Contrato SUT",
        help_text="Contrato del trabajador asociado a esta nómina."
    )

    fecha_ingreso = models.DateField(null=True, blank=True,
        verbose_name="Fecha de ingreso",
        help_text="Fecha de inicio de la relación laboral."
    )

    fecha_salida = models.DateField(null=True, blank=True,
        verbose_name="Fecha de salida",
        help_text="Fecha de terminación del contrato, si aplica."
    )

    # =======================
    # PERÍODO DE NÓMINA
    # =======================
    mes = models.PositiveIntegerField(null=True, blank=True,
        verbose_name="Mes",
        help_text="Mes al que corresponde la nómina (1–12)."
    )

    anio = models.PositiveIntegerField(null=True, blank=True,
        verbose_name="Año",
        help_text="Año al que corresponde la nómina."
    )

    # =======================
    # REMUNERACIÓN
    # =======================
    sueldo_base = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Sueldo base",
        help_text="Sueldo mensual acordado en el contrato."
    )


    horas_extra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name="Horas extra",
        help_text="Valor monetario de horas suplementarias y extraordinarias."
    )

    recibe_bonificacion = models.BooleanField(default=False,
        verbose_name="Recibe bonificación",
        help_text="Indica si el trabajador recibe bonificaciones. Si es False, el valor se considera 0.00."
    )

    otros_ingresos = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Bonificaciones",
        help_text="Bonificaciones u otros ingresos gravados según IESS. Se coloca 0 si no aplica."
    )

    # =======================
    # DÉCIMOS Y UTILIDADES
    # =======================
    recibe_decimo_tercero = models.BooleanField(default=True,
        verbose_name="Recibe décimo tercero",
        help_text="Indica si aplica el décimo tercero sueldo. Aplica en Diciembre 1/2 sueldo anual. Declarar al IESS."
    )
    decimo_tercero = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="13º",
        help_text="Valor proporcional del décimo tercero. 0 si no aplica."
    )

    recibe_decimo_cuarto = models.BooleanField(default=True,
        verbose_name="Decimo cuarto",
        help_text="Indica si aplica el décimo cuarto sueldo. Aplica 15 agosto es un sueldo basico unificado."
    )
    decimo_cuarto = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="14º",
        help_text="Valor proporcional del décimo cuarto. 0 si no aplica."
    )

    recibe_utilidades = models.BooleanField(default=False,
        verbose_name="Recibe utilidades",
        help_text="Indica si recibe participación en utilidades. Declarar al IESS si corresponde."
    )
    utilidades = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Utilidades",
        help_text="Participación en utilidades del trabajador. 0 si no aplica."
    )

    # =======================
    # VACACIONES
    # =======================
    recibe_vacaciones = models.BooleanField(default=False,
        verbose_name="Recibe vacaciones",
        help_text="Indica si el trabajador recibe pago de vacaciones proporcional."
    )

    vacaciones = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Vacaciones",
        help_text="Valor proporcional de vacaciones (15 días de sueldo base). 0 si no aplica."
    )

    # =======================
    # DESCUENTOS
    # =======================
    recibe_descuento = models.BooleanField(default=False,
        verbose_name="Aplica descuentos",
        help_text="Indica si aplica descuentos legales o deducciones al trabajador."
    )

    DESCUENTOS_LEGALES = [
        ("PRESTAMOS_EMPLEADOR", "Préstamos otorgados por el empleador"),
        ("PRESTAMOS_IESS", "Préstamos del IESS (cesantía, hipotecarios, educativos)"),
        ("ANTICIPOS", "Anticipos de sueldo"),
        ("APORTES_IESS", "Aportes obligatorios al IESS"),
        ("IMPUESTO_RENTA", "Retención de Impuesto a la Renta"),
        ("PENSION_ALIMENTICIA", "Pensiones alimenticias"),
        ("EMBARGO_JUDICIAL", "Embargos judiciales sobre salario"),
        ("SANCIONES_INTERNAS", "Sanciones por incumplimiento de políticas internas, según reglamento de la empresa"),
    ]

    razon_descuento = models.CharField(max_length=50, choices=DESCUENTOS_LEGALES, null=True, blank=True,
        verbose_name="Razón de descuento",
        help_text="Motivo del descuento aplicado al trabajador."
    )

    descuentos = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Descuentos",
        help_text="Suma de descuentos legales y deducciones aplicadas al trabajador."
    )

    # =======================
    # APORTES IESS
    # =======================
    aporte_iess_trabajador = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="A-IESS-T",
        help_text="9.45 % del sueldo base, descontado al trabajador según IESS."
    )

    aporte_iess_empleador = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="A-IESS-E",
        help_text="11.15 % del sueldo base, asumido por el empleador."
    )

    # =======================
    # TOTALES
    # =======================
    total_ingresos = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Total ingresos",
        help_text="Suma total de ingresos del trabajador en el mes, considerando bonificaciones, décimos, utilidades y vacaciones."
    )

    sueldo_a_pagar = MoneyField(max_digits=10, decimal_places=2, null=True, blank=True,
        default_currency='USD',
        verbose_name="Sueldo",
        help_text="Valor neto que recibe el trabajador luego de descuentos y aporte IESS."
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True,
        verbose_name="Fecha de creación",
        help_text="Fecha en la que se generó el registro de nómina."
    )

    hash_contrato = models.CharField(max_length=64, unique=True, editable=False, null=True, blank=True,
        verbose_name="Hash único del contrato",
        help_text="Hash SHA-256 único que certifica la integridad del contrato."
    )

    # ==================================================
    # LÓGICA DE CÁLCULO
    # ==================================================
    def save(self, *args, **kwargs):
        if not self.hash_contrato:
            raw = f"{self.contrato}|{self.fecha_ingreso}|{uuid.uuid4()}|{now().isoformat()}"
            self.hash_contrato = hashlib.sha256(raw.encode("utf-8")).hexdigest()

        sueldo = self.sueldo_base or Decimal("0.00")
        horas = self.horas_extra or Decimal("0.00")
        otros = self.otros_ingresos if self.recibe_bonificacion else Decimal("0.00")

        # Décimos y utilidades
        self.decimo_tercero = (sueldo / Decimal("12")) if self.recibe_decimo_tercero else Decimal("0.00")
        self.decimo_cuarto = (sueldo / Decimal("12")) if self.recibe_decimo_cuarto else Decimal("0.00")
        self.utilidades = self.utilidades if self.recibe_utilidades else Decimal("0.00")

        # Vacaciones (proporcional a 15 días)
        self.vacaciones = (sueldo / Decimal("2")) / Decimal("12") if self.recibe_vacaciones else Decimal("0.00")

        # Aportes IESS
        self.aporte_iess_trabajador = sueldo * Decimal("0.0945")
        self.aporte_iess_empleador = sueldo * Decimal("0.1115")

        # Total ingresos
        self.total_ingresos = (
            sueldo + horas + otros +
            self.decimo_tercero +
            self.decimo_cuarto +
            self.utilidades +
            self.vacaciones
        )

        # Neto a pagar
        descuentos = self.descuentos or Decimal("0.00")
        self.sueldo_a_pagar = self.total_ingresos - self.aporte_iess_trabajador - descuentos

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Nómina de trabajador"
        verbose_name_plural = "Nómina de trabajadores: Instituto Ecuatoriano de Seguridad Social (IESS)"

    def __str__(self):
        return f"{self.mes}/{self.anio}"
