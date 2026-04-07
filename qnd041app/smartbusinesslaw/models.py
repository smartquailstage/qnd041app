from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
import uuid
import hashlib
from django.utils import timezone
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP



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
        max_length=16,
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
        null=True, blank=True,
        help_text="Año al que corresponde el reporte financiero. Ejemplo: 2025"
    )
    economic_activity = models.CharField(
        "Actividad económica",
        max_length=10,
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

    # =========================
    # BALANCE GENERAL
    # =========================

    c_1_activo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1 - ACTIVO"
    )

    c_101_activo_corriente = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101 - ACTIVO CORRIENTE"
    )

    c_10101_efectivo_y_equivalentes_de_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10101 - EFECTIVO Y EQUIVALENTES DE EFECTIVO"
    )

    c_1010101_caja = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010101 - CAJA"
    )

    c_1010102_instituciones_financieras_publicas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010102 - INSTITUCIONES FINANCIERAS PÚBLICAS"
    )

    c_1010103_instituciones_financieras_privadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010103 - INSTITUCIONES FINANCIERAS PRIVADAS"
    )

    c_10102_activos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102 - ACTIVOS FINANCIEROS"
    )

    c_1010201_activos_financieros_a_valor_razonable_con_cambios_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010201 - ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_101020101_renta_variable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020101 - RENTA VARIABLE"
    )

    c_10102010101_acciones_y_participaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010101 - ACCIONES Y PARTICIPACIONES"
    )

    c_10102010102_cuotas_de_fondos_colectivos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010102 - CUOTAS DE FONDOS COLECTIVOS"
    )

    c_10102010103_valores_de_titularizacion_de_participacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010103 - VALORES DE  TITULARIZACIÓN DE PARTICIPACIÓN"
    )

    c_10102010104_unidades_de_participacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010104 - UNIDADES DE PARTICIPACIÓN"
    )

    c_10102010105_inversiones_en_el_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010105 - INVERSIONES EN EL EXTERIOR"
    )

    c_10102010106_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010106 - OTROS"
    )

    c_101020102_renta_fija = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020102 - RENTA FIJA"
    )

    c_10102010201_avales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010201 - AVALES"
    )

    c_10102010202_bonos_del_estado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010202 - BONOS DEL ESTADO"
    )

    c_10102010203_bonos_de_prenda = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010203 - BONOS DE PRENDA"
    )

    c_10102010204_cedulas_hipotecarias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010204 - CÉDULAS HIPOTECARIAS"
    )

    c_10102010205_certificados_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010205 - CERTIFICADOS FINANCIEROS"
    )

    c_10102010206_certificados_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010206 - CERTIFICADOS DE INVERSIÓN"
    )

    c_10102010207_certificados_de_tesoreria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010207 - CERTIFICADOS DE TESORERÍA"
    )

    c_10102010208_certificados_de_deposito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010208 - CERTIFICADOS DE DEPÓSITO"
    )

    c_10102010209_cupones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010209 - CUPONES"
    )

    c_10102010210_depositos_a_plazo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010210 - DEPÓSITOS A PLAZO"
    )

    c_10102010211_letras_de_cambio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010211 - LETRAS DE CAMBIO"
    )

    c_10102010212_notas_de_credito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010212 - NOTAS DE CRÉDITO"
    )

    c_10102010213_obligaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010213 - OBLIGACIONES"
    )

    c_10102010214_facturas_comerciales_negociables = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010214 - FACTURAS COMERCIALES NEGOCIABLES"
    )

    c_10102010215_overnights = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010215 - OVERNIGHTS"
    )

    c_10102010216_obligaciones_convertibles_en_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010216 - OBLIGACIONES CONVERTIBLES EN ACCIONES"
    )

    c_10102010217_papel_comercial = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010217 - PAPEL COMERCIAL"
    )

    c_10102010218_pagares = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010218 - PAGARÉS"
    )

    c_10102010219_polizas_de_acumulacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010219 - PÓLIZAS DE ACUMULACIÓN"
    )

    c_10102010220_titulos_del_banco_central = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010220 - TÍTULOS DEL BANCO CENTRAL"
    )

    c_10102010221_valores_de_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010221 - VALORES DE TITULARIZACIÓN"
    )

    c_10102010222_inversiones_en_el_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010222 - INVERSIONES EN EL EXTERIOR"
    )

    c_10102010223_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010223 - OTROS"
    )

    c_101020103_derivados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020103 - DERIVADOS"
    )

    c_10102010301_forward = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010301 - FORWARD"
    )

    c_10102010302_futuros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010302 - FUTUROS"
    )

    c_10102010303_opciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010303 - OPCIONES"
    )

    c_10102010304_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102010304 - OTROS"
    )

    c_1010202_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010202 - ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_101020201_renta_variable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020201 - RENTA VARIABLE"
    )

    c_10102020101_acciones_y_participaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020101 - ACCIONES Y PARTICIPACIONES"
    )

    c_10102020102_cuotas_de_fondos_colectivos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020102 - CUOTAS DE FONDOS COLECTIVOS"
    )

    c_10102020103_unidades_de_participacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020103 - UNIDADES DE PARTICIPACIÓN"
    )

    c_10102020104_valores_de_titularizacion_de_participacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020104 - VALORES DE  TITULARIZACIÓN DE PARTICIPACIÓN"
    )

    c_10102020105_inversiones_en_el_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020105 - INVERSIONES EN EL EXTERIOR"
    )

    c_10102020106_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020106 - OTROS"
    )

    c_101020202_renta_fija = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020202 - RENTA FIJA"
    )

    c_10102020201_avales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020201 - AVALES"
    )

    c_10102020202_bonos_del_estado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020202 - BONOS DEL ESTADO"
    )

    c_10102020203_bonos_de_prenda = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020203 - BONOS DE PRENDA"
    )

    c_10102020204_cedulas_hipotecarias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020204 - CÉDULAS HIPOTECARIAS"
    )

    c_10102020205_certificados_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020205 - CERTIFICADOS FINANCIEROS"
    )

    c_10102020206_certificados_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020206 - CERTIFICADOS DE INVERSIÓN"
    )

    c_10102020207_certificados_de_tesoreria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020207 - CERTIFICADOS DE TESORERÍA"
    )

    c_10102020208_certificados_de_deposito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020208 - CERTIFICADOS DE DEPÓSITO"
    )

    c_10102020209_cupones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020209 - CUPONES"
    )

    c_10102020210_depositos_a_plazo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020210 - DEPÓSITOS A PLAZO"
    )

    c_10102020211_letras_de_cambio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020211 - LETRAS DE CAMBIO"
    )

    c_10102020212_notas_de_credito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020212 - NOTAS DE CRÉDITO"
    )

    c_10102020213_obligaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020213 - OBLIGACIONES"
    )

    c_10102020214_facturas_comerciales_negociables = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020214 - FACTURAS COMERCIALES NEGOCIABLES"
    )

    c_10102020215_overnights = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020215 - OVERNIGHTS"
    )

    c_10102020216_obligaciones_convertibles_en_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020216 - OBLIGACIONES CONVERTIBLES EN ACCIONES"
    )

    c_10102020217_papel_comercial = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020217 - PAPEL COMERCIAL"
    )

    c_10102020218_pagares = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020218 - PAGARÉS"
    )

    c_10102020219_polizas_de_acumulacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020219 - PÓLIZAS DE ACUMULACIÓN"
    )

    c_10102020220_titulos_del_banco_central = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020220 - TÍTULOS DEL BANCO CENTRAL"
    )

    c_10102020221_valores_de_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020221 - VALORES DE TITULARIZACIÓN"
    )

    c_10102020222_inversiones_en_el_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020222 - INVERSIONES EN EL EXTERIOR"
    )

    c_10102020223_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102020223 - OTROS"
    )

    c_1010203_activos_financieros_al_costo_amortizado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010203 - ACTIVOS FINANCIEROS AL COSTO AMORTIZADO"
    )

    c_101020302_renta_fija = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020302 - RENTA FIJA"
    )

    c_10102030201_avales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030201 - AVALES"
    )

    c_10102030202_bonos_del_estado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030202 - BONOS DEL ESTADO"
    )

    c_10102030203_bonos_de_prenda = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030203 - BONOS DE PRENDA"
    )

    c_10102030204_cedulas_hipotecarias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030204 - CÉDULAS HIPOTECARIAS"
    )

    c_10102030205_certificados_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030205 - CERTIFICADOS FINANCIEROS"
    )

    c_10102030206_certificados_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030206 - CERTIFICADOS DE INVERSIÓN"
    )

    c_10102030207_certificados_de_tesoreria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030207 - CERTIFICADOS DE TESORERÍA"
    )

    c_10102030208_certificados_de_deposito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030208 - CERTIFICADOS DE DEPÓSITO"
    )

    c_10102030209_cupones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030209 - CUPONES"
    )

    c_10102030210_depositos_a_plazo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030210 - DEPÓSITOS A PLAZO"
    )

    c_10102030211_letras_de_cambio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030211 - LETRAS DE CAMBIO"
    )

    c_10102030212_notas_de_credito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030212 - NOTAS DE CRÉDITO"
    )

    c_10102030213_obligaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030213 - OBLIGACIONES"
    )

    c_10102030214_facturas_comerciales_negociables = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030214 - FACTURAS COMERCIALES NEGOCIABLES"
    )

    c_10102030215_overnights = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030215 - OVERNIGHTS"
    )

    c_10102030216_obligaciones_convertibles_en_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030216 - OBLIGACIONES CONVERTIBLES EN ACCIONES"
    )

    c_10102030217_papel_comercial = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030217 - PAPEL COMERCIAL"
    )

    c_10102030218_pagares = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030218 - PAGARÉS"
    )

    c_10102030219_polizas_de_acumulacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030219 - PÓLIZAS DE ACUMULACIÓN"
    )

    c_10102030220_titulos_del_banco_central = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030220 - TÍTULOS DEL BANCO CENTRAL"
    )

    c_10102030221_valores_de_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030221 - VALORES DE TITULARIZACIÓN"
    )

    c_10102030222_inversiones_en_el_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030222 - INVERSIONES EN EL EXTERIOR"
    )

    c_10102030223_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102030223 - OTROS"
    )

    c_1010204_provision_por_deterioro_de_activos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010204 - PROVISIÓN POR DETERIORO DE ACTIVOS FINANCIEROS"
    )

    c_101020401_activos_financieros_a_valor_razonable_con_cambios_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020401 - ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_101020402_activos_financieros_al_costo_amortizado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020402 - ACTIVOS FINANCIEROS AL COSTO AMORTIZADO"
    )

    c_101020403_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020403 - ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_1010205_deudores_comerciales_y_otras_cuentas_por_cobrar_no_relacionados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010205 - DEUDORES COMERCIALES Y OTRAS CUENTAS POR COBRAR NO RELACIONADOS"
    )

    c_101020501_de_actividades_ordinarias_que_generen_intereses = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020501 - DE ACTIVIDADES ORDINARIAS QUE GENEREN INTERESES"
    )

    c_10102050101_cuentas_y_documentos_a_cobrar_a_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050101 - CUENTAS Y DOCUMENTOS A COBRAR  A CLIENTES"
    )

    c_10102050102_cuentas_y_documentos_a_cobrar_a_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050102 - CUENTAS Y DOCUMENTOS A COBRAR  A TERCEROS"
    )

    c_101020502_de_actividades_ordinarias_que_no_generen_intereses = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020502 - DE ACTIVIDADES ORDINARIAS QUE NO GENEREN INTERESES"
    )

    c_10102050201_cuentas_y_documentos_a_cobrar_a_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050201 - CUENTAS Y DOCUMENTOS A COBRAR  A CLIENTES"
    )

    c_10102050202_cuentas_y_documentos_a_cobrar_a_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050202 - CUENTAS Y DOCUMENTOS A COBRAR  A TERCEROS"
    )

    c_10102050203_cuentas_por_cobrar_al_originador = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050203 - CUENTAS POR COBRAR AL ORIGINADOR"
    )

    c_10102050204_comisiones_por_operaciones_bursatiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050204 - COMISIONES POR OPERACIONES  BURSÁTILES"
    )

    c_10102050207_contrato_de_underwriting = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050207 - CONTRATO DE UNDERWRITING"
    )

    c_10102050208_por_administracion_y_manejo_de_portafolios_de_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050208 - POR  ADMINISTRACIÓN Y MANEJO DE PORTAFOLIOS DE TERCEROS"
    )

    c_10102050209_por_administracion_y_manejo_de_fondos_administrados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050209 - POR ADMINISTRACIÓN Y MANEJO DE FONDOS ADMINISTRADOS"
    )

    c_10102050210_por_administracion_y_manejo_de_negocios_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050210 - POR ADMINISTRACIÓN Y MANEJO DE NEGOCIOS FIDUCIARIOS"
    )

    c_10102050211_por_custodia_y_conservacion_de_valores_materializados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050211 - POR CUSTODIA Y CONSERVACIÓN DE VALORES MATERIALIZADOS"
    )

    c_10102050212_por_custodia_y_conservacion_de_valores_desmaterializados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050212 - POR CUSTODIA Y CONSERVACIÓN DE VALORES DESMATERIALIZADOS"
    )

    c_10102050213_por_manejo_de_libro_de_acciones_y_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050213 - POR MANEJO DE LIBRO DE ACCIONES Y ACCIONISTAS"
    )

    c_10102050214_por_asesoria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050214 - POR ASESORÍA"
    )

    c_10102050215_dividendos_por_cobrar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050215 - DIVIDENDOS POR COBRAR"
    )

    c_10102050216_intereses_por_cobrar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050216 - INTERESES POR COBRAR"
    )

    c_10102050217_deudores_por_intermediacion_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050217 - DEUDORES POR INTERMEDIACIÓN DE VALORES"
    )

    c_10102050218_anticipo_a_comitentes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050218 - ANTICIPO A COMITENTES"
    )

    c_10102050219_anticipo_a_constructor_por_avance_de_obra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050219 - ANTICIPO A CONSTRUCTOR POR AVANCE DE OBRA"
    )

    c_10102050220_derechos_por_compromiso_de_recompra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050220 - DERECHOS POR COMPROMISO DE RECOMPRA"
    )

    c_10102050221_otras_cuentas_por_cobrar_no_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10102050221 - OTRAS CUENTAS POR COBRAR NO RELACIONADAS"
    )

    c_1010206_documentos_y_cuentas_por_cobrar_relacionados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010206 - DOCUMENTOS Y CUENTAS POR COBRAR RELACIONADOS"
    )

    c_101020601_por_cobrar_a_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020601 - POR COBRAR A ACCIONISTAS"
    )

    c_101020602_por_cobrar_a_companias_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020602 - POR COBRAR A COMPAÑÍAS RELACIONADAS"
    )

    c_101020603_por_cobrar_a_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020603 - POR COBRAR A CLIENTES"
    )

    c_101020604_otras_cuentas_por_cobrar_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 101020604 - OTRAS CUENTAS POR COBRAR RELACIONADAS"
    )

    c_1010207_provision_por_cuentas_incobrables_y_deterioro = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010207 - PROVISIÓN POR CUENTAS INCOBRABLES Y DETERIORO"
    )

    c_10103_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10103 - INVENTARIOS"
    )

    c_1010301_inventarios_de_materia_prima = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010301 - INVENTARIOS DE MATERIA PRIMA"
    )

    c_1010302_inventarios_de_productos_en_proceso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010302 - INVENTARIOS DE PRODUCTOS EN PROCESO"
    )

    c_1010303_inventarios_de_suministros_o_materiales_a_ser_consumidos_en_el_proceso_de_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010303 - INVENTARIOS DE SUMINISTROS O MATERIALES A SER CONSUMIDOS EN EL PROCESO DE PRODUCCION"
    )

    c_1010304_inventarios_de_suministros_o_materiales_a_ser_consumidos_en_la_prestacion_del_servicio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010304 - INVENTARIOS DE SUMINISTROS O MATERIALES A SER CONSUMIDOS EN LA PRESTACION DEL SERVICIO"
    )

    c_1010305_inventarios_de_prod_term_y_mercad_en_almacen_producido_por_la_compania = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010305 - INVENTARIOS DE PROD. TERM. Y MERCAD. EN ALMACÉN - PRODUCIDO POR LA COMPAÑÍA"
    )

    c_1010306_inventarios_de_prod_term_y_mercad_en_almacen_comprado_a_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010306 - INVENTARIOS DE PROD. TERM. Y MERCAD. EN ALMACÉN - COMPRADO A  TERCEROS"
    )

    c_1010307_mercaderias_en_transito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010307 - MERCADERÍAS EN TRÁNSITO"
    )

    c_1010308_obras_en_construccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010308 - OBRAS EN CONSTRUCCION"
    )

    c_1010309_obras_terminadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010309 - OBRAS TERMINADAS"
    )

    c_1010310_materiales_o_bienes_para_la_construccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010310 - MATERIALES O BIENES PARA LA CONSTRUCCION"
    )

    c_1010311_inventarios_repuestos_herramientas_y_accesorios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010311 - INVENTARIOS REPUESTOS, HERRAMIENTAS Y ACCESORIOS"
    )

    c_1010312_otros_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010312 - OTROS INVENTARIOS"
    )

    c_1010313_provision_por_valor_neto_de_realizacion_y_otras_perdidas_en_inventario = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010313 - (-) PROVISIÓN POR VALOR NETO DE REALIZACIÓN Y OTRAS PERDIDAS EN INVENTARIO"
    )

    c_10104_servicios_y_otros_pagos_anticipados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10104 - SERVICIOS Y OTROS PAGOS ANTICIPADOS"
    )

    c_1010401_seguros_pagados_por_anticipado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010401 - SEGUROS PAGADOS POR ANTICIPADO"
    )

    c_1010402_arriendos_pagados_por_anticipado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010402 - ARRIENDOS PAGADOS POR ANTICIPADO"
    )

    c_1010403_anticipos_a_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010403 - ANTICIPOS A PROVEEDORES"
    )

    c_1010404_otros_anticipos_entregados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010404 - OTROS ANTICIPOS ENTREGADOS"
    )

    c_10105_activos_por_impuestos_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10105 - ACTIVOS POR IMPUESTOS CORRIENTES"
    )

    c_1010501_credito_tributario_a_favor_de_la_empresa_iva = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010501 - CRÉDITO TRIBUTARIO A FAVOR DE LA EMPRESA (IVA)"
    )

    c_1010502_credito_tributario_a_favor_de_la_empresa_i_r = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010502 - CRÉDITO TRIBUTARIO A FAVOR DE LA EMPRESA ( I. R.)"
    )

    c_1010503_anticipo_de_impuesto_a_la_renta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1010503 - ANTICIPO DE IMPUESTO A LA RENTA"
    )

    c_10106_activos_corrientes_mantenidos_para_la_venta_y_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10106 - ACTIVOS CORRIENTES MANTENIDOS PARA LA VENTA Y OPERACIONES DISCONTINUADAS"
    )

    c_10107_construcciones_en_proceso_nic_11_y_secc23_pymes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10107 - CONSTRUCCIONES EN PROCESO (NIC 11 Y SECC.23 PYMES)"
    )

    c_10108_otros_activos_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10108 - OTROS ACTIVOS CORRIENTES"
    )

    c_102_activos_no_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102 - ACTIVOS NO CORRIENTES"
    )

    c_10201_propiedad_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10201 - PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_1020101_terrenos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020101 - TERRENOS"
    )

    c_1020102_edificios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020102 - EDIFICIOS"
    )

    c_1020103_construcciones_en_curso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020103 - CONSTRUCCIONES EN CURSO"
    )

    c_1020104_instalaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020104 - INSTALACIONES"
    )

    c_1020105_muebles_y_enseres = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020105 - MUEBLES Y ENSERES"
    )

    c_1020106_maquinaria_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020106 - MAQUINARIA Y EQUIPO"
    )

    c_1020107_naves_aereonaves_barcazas_y_similares = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020107 - NAVES, AEREONAVES, BARCAZAS Y SIMILARES"
    )

    c_1020108_equipo_de_computacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020108 - EQUIPO DE COMPUTACIÓN"
    )

    c_1020109_vehiculos_equipos_de_trasporte_y_equipo_caminero_movil = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020109 - VEHÍCULOS, EQUIPOS DE TRASPORTE Y EQUIPO CAMINERO MÓVIL"
    )

    c_1020110_otros_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020110 - OTROS PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_1020111_repuestos_y_herramientas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020111 - REPUESTOS Y HERRAMIENTAS"
    )

    c_1020112_depreciacion_acumulada_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020112 - (-) DEPRECIACIÓN ACUMULADA PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_1020113_deterioro_acumulado_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020113 - (-) DETERIORO  ACUMULADO DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_1020114_activos_de_exploracion_y_explotacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020114 - ACTIVOS DE EXPLORACION Y EXPLOTACION"
    )

    c_102011401_activos_de_exploracion_y_explotacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102011401 - ACTIVOS DE EXPLORACION Y EXPLOTACION"
    )

    c_102011402_amortizacion_acumulada_de_activos_de_exploracion_y_explotacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102011402 - (-) AMORTIZACION ACUMULADA DE ACTIVOS DE EXPLORACIÓN Y EXPLOTACIÓN"
    )

    c_102011403_deterioro_acumulado_de_activos_de_exploracion_y_explotacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102011403 - (-) DETERIORO  ACUMULADO DE ACTIVOS DE EXPLORACIÓN Y EXPLOTACIÓN"
    )

    c_10202_propiedades_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10202 - PROPIEDADES DE INVERSIÓN"
    )

    c_1020201_terrenos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020201 - TERRENOS"
    )

    c_102020101_terrenos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102020101 - TERRENOS"
    )

    c_102020102_derechos_de_uso_sobre_terrenos_subarrendados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102020102 - DERECHOS DE USO SOBRE TERRENOS SUBARRENDADOS"
    )

    c_1020202_edificios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020202 - EDIFICIOS"
    )

    c_102020201_edificios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102020201 - EDIFICIOS"
    )

    c_102020202_derechos_de_uso_sobre_edificios_subarrendados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 102020202 - DERECHOS DE USO SOBRE EDIFICIOS SUBARRENDADOS"
    )

    c_1020203_depreciacion_acumulada_de_propiedades_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020203 - (-) DEPRECIACION ACUMULADA DE PROPIEDADES DE INVERSIÓN"
    )

    c_1020204_deterioro_acumulado_de_propiedades_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020204 - (-) DETERIORO ACUMULADO DE PROPIEDADES DE INVERSIÓN"
    )

    c_10203_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10203 - ACTIVOS BIOLOGICOS"
    )

    c_1020301_animales_vivos_en_crecimiento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020301 - ANIMALES VIVOS EN CRECIMIENTO"
    )

    c_1020302_animales_vivos_en_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020302 - ANIMALES VIVOS EN PRODUCCION"
    )

    c_1020303_plantas_en_crecimiento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020303 - PLANTAS EN CRECIMIENTO"
    )

    c_1020304_plantas_en_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020304 - PLANTAS EN PRODUCCION"
    )

    c_1020305_depreciacion_acumulada_de_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020305 - (-) DEPRECIACION ACUMULADA DE ACTIVOS BIOLÓGICOS"
    )

    c_1020306_deterioro_acumulado_de_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020306 - (-) DETERIORO ACUMULADO DE ACTIVOS BIOLOGÍCOS"
    )

    c_10204_activo_intangible = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10204 - ACTIVO INTANGIBLE"
    )

    c_1020401_plusvalias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020401 - PLUSVALÍAS"
    )

    c_1020402_marcas_patentes_derechos_de_llave_cuotas_patrimoniales_y_otros_similares = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020402 - MARCAS, PATENTES, DERECHOS DE LLAVE , CUOTAS PATRIMONIALES Y OTROS SIMILARES"
    )

    c_1020403_concesiones_y_licencias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020403 - CONCESIONES Y LICENCIAS"
    )

    c_1020404_activos_de_exploracion_y_explotacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020404 - ACTIVOS DE EXPLORACION Y EXPLOTACION"
    )

    c_1020405_amortizacion_acumulada_de_activos_intangible = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020405 - (-) AMORTIZACIÓN ACUMULADA DE ACTIVOS INTANGIBLE"
    )

    c_1020406_deterioro_acumulado_de_activo_intangible = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020406 - (-) DETERIORO ACUMULADO DE ACTIVO INTANGIBLE"
    )

    c_1020407_otros_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020407 - OTROS INTANGIBLES"
    )

    c_10205_activos_por_impuestos_diferidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10205 - ACTIVOS POR IMPUESTOS DIFERIDOS"
    )

    c_10206_activos_financieros_no_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10206 - ACTIVOS FINANCIEROS NO CORRIENTES"
    )

    c_1020601_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020601 - ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_1020602_provision_por_deterioro_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020602 - (-) PROVISION POR DETERIORO DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_1020603_activos_financieros_a_costo_amortizado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020603 - ACTIVOS FINANCIEROS A COSTO AMORTIZADO"
    )

    c_1020604_provision_por_deterioro_de_activos_financieros_a_costo_amortizado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020604 - (-) PROVISIÓN POR DETERIORO DE ACTIVOS FINANCIEROS A COSTO AMORTIZADO"
    )

    c_1020605_activos_financieros_a_valor_razonable_con_cambios_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020605 - ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_1020606_provision_por_deterioro_de_activos_financieros_a_valor_razonable_con_cambios_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020606 - (-)PROVISIÓN POR DETERIORO DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_10207_derecho_de_uso_por_activos_arrendados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10207 - DERECHO DE USO POR ACTIVOS ARRENDADOS"
    )

    c_1020701_depreciacion_acumulada_de_activos_provenientes_por_derechos_de_uso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020701 - (-) DEPRECIACIÓN ACUMULADA DE ACTIVOS PROVENIENTES POR DERECHOS DE USO"
    )

    c_1020702_deterioro_acumulado_de_activos_provenientes_por_derechos_de_uso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020702 - (-) DETERIORO ACUMULADO DE ACTIVOS PROVENIENTES POR DERECHOS DE USO"
    )

    c_1020703_derecho_de_uso_por_activos_arrendados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020703 - DERECHO DE USO POR ACTIVOS ARRENDADOS"
    )

    c_10208_otros_activos_no_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10208 - OTROS ACTIVOS NO CORRIENTES"
    )

    c_1020801_derechos_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020801 - DERECHOS FIDUCIARIOS"
    )

    c_1020802_depositos_en_garantia = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020802 - DEPÓSITOS EN GARANTÍA"
    )

    c_1020803_depositos_en_garantia_por_operaciones_bursatiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020803 - DEPÓSITOS EN GARANTÍA POR OPERACIONES BURSÁTILES"
    )

    c_1020805_acciones_del_deposito_centralizado_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020805 - ACCIONES DEL DEPÓSITO CENTRALIZADO DE VALORES"
    )

    c_1020806_inversiones_subsidiarias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020806 - INVERSIONES SUBSIDIARIAS"
    )

    c_1020807_inversiones_asociadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020807 - INVERSIONES ASOCIADAS"
    )

    c_1020808_inversiones_negocios_conjuntos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020808 - INVERSIONES NEGOCIOS CONJUNTOS"
    )

    c_1020809_otras_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020809 - OTRAS INVERSIONES"
    )

    c_1020810_provision_valuacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020810 - (-) PROVISIÓN VALUACIÓN DE INVERSIONES"
    )

    c_1020811_otros_activos_no_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020811 - OTROS ACTIVOS NO CORRIENTES"
    )

    c_10209_documentos_y_cuentas_por_cobrar_no_relacionados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10209 - DOCUMENTOS Y CUENTAS POR COBRAR NO RELACIONADOS"
    )

    c_1020901_cuentas_y_documentos_a_cobrar_a_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020901 - CUENTAS Y DOCUMENTOS A COBRAR  A CLIENTES"
    )

    c_1020902_cuentas_y_documentos_a_cobrar_a_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020902 - CUENTAS Y DOCUMENTOS A COBRAR  A TERCEROS"
    )

    c_1020903_otras_cuentas_por_cobrar_no_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1020903 - OTRAS CUENTAS POR COBRAR NO RELACIONADAS"
    )

    c_10210_documentos_y_cuentas_por_cobrar_relacionados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 10210 - DOCUMENTOS Y CUENTAS POR COBRAR RELACIONADOS"
    )

    c_1021001_por_cobrar_a_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1021001 - POR COBRAR A ACCIONISTAS"
    )

    c_1021002_por_cobrar_a_companias_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1021002 - POR COBRAR A COMPAÑÍAS RELACIONADAS"
    )

    c_1021003_por_cobrar_a_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1021003 - POR COBRAR A CLIENTES"
    )

    c_1021004_otras_cuentas_por_cobrar_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 1021004 - OTRAS CUENTAS POR COBRAR RELACIONADAS"
    )

    c_2_pasivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2 - PASIVO"
    )

    c_201_pasivo_corriente = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201 - PASIVO CORRIENTE"
    )

    c_20101_pasivos_financieros_a_valor_razonable_con_cambios_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20101 - PASIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN RESULTADOS"
    )

    c_20102_pasivos_por_contratos_de_arrendamiento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20102 - PASIVOS POR CONTRATOS DE ARRENDAMIENTO"
    )

    c_20103_cuentas_y_documentos_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20103 - CUENTAS Y DOCUMENTOS POR PAGAR"
    )

    c_2010301_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010301 - LOCALES"
    )

    c_201030101_prestamos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201030101 - PRÉSTAMOS"
    )

    c_201030102_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201030102 - PROVEEDORES"
    )

    c_201030103_otras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201030103 - OTRAS"
    )

    c_2010302_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010302 - DEL EXTERIOR"
    )

    c_201030201_prestamos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201030201 - PRÉSTAMOS"
    )

    c_201030202_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201030202 - PROVEEDORES"
    )

    c_201030203_otras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201030203 - OTRAS"
    )

    c_20104_obligaciones_con_instituciones_financieras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20104 - OBLIGACIONES CON INSTITUCIONES FINANCIERAS"
    )

    c_2010401_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010401 - LOCALES"
    )

    c_2010402_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010402 - DEL EXTERIOR"
    )

    c_20105_provisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20105 - PROVISIONES"
    )

    c_2010501_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010501 - LOCALES"
    )

    c_2010502_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010502 - DEL EXTERIOR"
    )

    c_20106_porcion_corriente_de_valores_emitidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20106 - PORCIÓN CORRIENTE DE VALORES EMITIDOS"
    )

    c_2010601_obligaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010601 - OBLIGACIONES"
    )

    c_2010602_papel_comercial = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010602 - PAPEL COMERCIAL"
    )

    c_2010603_valores_de_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010603 - VALORES DE TITULARIZACIÓN"
    )

    c_2010604_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010604 - OTROS"
    )

    c_2010605_intereses_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010605 - INTERESES POR PAGAR"
    )

    c_20107_otras_obligaciones_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20107 - OTRAS OBLIGACIONES CORRIENTES"
    )

    c_2010701_con_la_administracion_tributaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010701 - CON LA ADMINISTRACIÓN TRIBUTARIA"
    )

    c_2010702_impuesto_a_la_renta_por_pagar_del_ejercicio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010702 - IMPUESTO A LA RENTA POR PAGAR DEL EJERCICIO"
    )

    c_2010703_con_el_iess = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010703 - CON EL IESS"
    )

    c_2010704_por_beneficios_de_ley_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010704 - POR BENEFICIOS DE LEY A EMPLEADOS"
    )

    c_2010705_participacion_trabajadores_por_pagar_del_ejercicio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010705 - PARTICIPACIÓN TRABAJADORES POR PAGAR DEL EJERCICIO"
    )

    c_2010706_dividendos_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010706 - DIVIDENDOS POR PAGAR"
    )

    c_2010707_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010707 - OTROS"
    )

    c_20108_cuentas_por_pagar_a_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20108 - CUENTAS POR PAGAR A RELACIONADAS"
    )

    c_2010801_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010801 - LOCALES"
    )

    c_201080101_prestamos_de_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080101 - PRÉSTAMOS DE ACCIONISTAS"
    )

    c_201080102_prestamos_de_companias_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080102 - PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_201080103_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080103 - PROVEEDORES"
    )

    c_201080104_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080104 - OTROS"
    )

    c_2010802_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2010802 - DEL EXTERIOR"
    )

    c_201080201_prestamos_de_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080201 - PRÉSTAMOS DE ACCIONISTAS"
    )

    c_201080202_prestamos_de_companias_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080202 - PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_201080203_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080203 - PROVEEDORES"
    )

    c_201080204_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 201080204 - OTROS"
    )

    c_20109_otros_pasivos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20109 - OTROS PASIVOS FINANCIEROS"
    )

    c_20110_anticipos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20110 - ANTICIPOS"
    )

    c_2011001_anticipos_de_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011001 - ANTICIPOS DE CLIENTES"
    )

    c_2011002_otros_anticipos_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011002 - OTROS ANTICIPOS RECIBIDOS"
    )

    c_20111_pasivos_directamente_asociados_con_los_activos_no_corrientes_y_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20111 - PASIVOS DIRECTAMENTE ASOCIADOS CON LOS ACTIVOS NO CORRIENTES Y OPERACIONES DISCONTINUADAS"
    )

    c_20112_porcion_corriente_de_provisiones_por_beneficios_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20112 - PORCION CORRIENTE DE PROVISIONES POR BENEFICIOS A EMPLEADOS"
    )

    c_2011201_jubilacion_patronal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011201 - JUBILACION PATRONAL"
    )

    c_2011202_otros_beneficios_para_los_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011202 - OTROS BENEFICIOS PARA LOS EMPLEADOS"
    )

    c_20113_otros_pasivos_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20113 - OTROS PASIVOS CORRIENTES"
    )

    c_2011301_comisiones_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011301 - COMISIONES POR PAGAR"
    )

    c_2011302_por_operaciones_bursatiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011302 - POR OPERACIONES BURSÁTILES"
    )

    c_2011303_por_custodia = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011303 - POR CUSTODIA"
    )

    c_2011304_por_administracion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011304 - POR ADMINISTRACIÓN"
    )

    c_2011305_otras_comisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011305 - OTRAS COMISIONES"
    )

    c_2011306_sanciones_y_multas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011306 - SANCIONES Y MULTAS"
    )

    c_2011307_indemnizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011307 - INDEMNIZACIONES"
    )

    c_2011308_obligaciones_judiciales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011308 - OBLIGACIONES JUDICIALES"
    )

    c_2011309_acreedores_por_intermediacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011309 - ACREEDORES POR INTERMEDIACIÓN"
    )

    c_2011310_obligacion_por_compromiso_de_recompra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011310 - OBLIGACIÓN POR COMPROMISO DE RECOMPRA"
    )

    c_2011311_por_contratos_de_underwriting = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011311 - POR CONTRATOS DE UNDERWRITING"
    )

    c_2011312_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2011312 - OTROS"
    )

    c_20114_pasivos_financieros_al_costo_amortizado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20114 - PASIVOS FINANCIEROS AL COSTO AMORTIZADO"
    )

    c_202_pasivo_no_corriente = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202 - PASIVO NO CORRIENTE"
    )

    c_20201_pasivos_por_contratos_de_arrendamiento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20201 - PASIVOS POR CONTRATOS DE ARRENDAMIENTO"
    )

    c_20202_cuentas_y_documentos_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20202 - CUENTAS Y DOCUMENTOS POR PAGAR"
    )

    c_2020201_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020201 - LOCALES"
    )

    c_202020101_prestamos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202020101 - PRÉSTAMOS"
    )

    c_202020102_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202020102 - PROVEEDORES"
    )

    c_202020103_otras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202020103 - OTRAS"
    )

    c_2020202_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020202 - DEL EXTERIOR"
    )

    c_202020201_prestamos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202020201 - PRÉSTAMOS"
    )

    c_202020202_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202020202 - PROVEEDORES"
    )

    c_202020203_otras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202020203 - OTRAS"
    )

    c_20203_obligaciones_con_instituciones_financieras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20203 - OBLIGACIONES CON INSTITUCIONES FINANCIERAS"
    )

    c_2020301_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020301 - LOCALES"
    )

    c_2020302_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020302 - DEL EXTERIOR"
    )

    c_20204_cuentas_por_pagar_a_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20204 - CUENTAS POR PAGAR A RELACIONADAS"
    )

    c_2020401_locales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020401 - LOCALES"
    )

    c_202040101_prestamos_de_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040101 - PRÉSTAMOS DE ACCIONISTAS"
    )

    c_202040102_prestamos_de_companias_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040102 - PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_202040103_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040103 - PROVEEDORES"
    )

    c_202040104_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040104 - OTROS"
    )

    c_2020402_del_exterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020402 - DEL EXTERIOR"
    )

    c_202040201_prestamos_de_accionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040201 - PRÉSTAMOS DE ACCIONISTAS"
    )

    c_202040202_prestamos_de_companias_relacionadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040202 - PRÉSTAMOS DE COMPAÑÍAS RELACIONADAS"
    )

    c_202040203_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040203 - PROVEEDORES"
    )

    c_202040204_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 202040204 - OTROS"
    )

    c_20205_porcion_no_corriente_de_valores_emitidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20205 - PORCIÓN NO CORRIENTE DE VALORES EMITIDOS"
    )

    c_2020501_obligaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020501 - OBLIGACIONES"
    )

    c_2020502_papel_comercial = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020502 - PAPEL COMERCIAL"
    )

    c_2020503_valores_de_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020503 - VALORES DE TITULARIZACIÓN"
    )

    c_2020504_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020504 - OTROS"
    )

    c_2020505_intereses_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020505 - INTERESES POR PAGAR"
    )

    c_20206_anticipos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20206 - ANTICIPOS"
    )

    c_2020601_anticipos_de_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020601 - ANTICIPOS DE CLIENTES"
    )

    c_2020602_otros_anticipos_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020602 - OTROS ANTICIPOS RECIBIDOS"
    )

    c_20207_provisiones_por_beneficios_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20207 - PROVISIONES POR BENEFICIOS A EMPLEADOS"
    )

    c_2020701_jubilacion_patronal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020701 - JUBILACION PATRONAL"
    )

    c_2020702_otros_beneficios_no_corrientes_para_los_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020702 - OTROS BENEFICIOS NO CORRIENTES PARA LOS EMPLEADOS"
    )

    c_20208_otras_provisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20208 - OTRAS PROVISIONES"
    )

    c_20209_pasivo_diferido = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20209 - PASIVO DIFERIDO"
    )

    c_2020901_ingresos_diferidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020901 - INGRESOS DIFERIDOS"
    )

    c_2020902_pasivos_por_impuestos_diferidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 2020902 - PASIVOS POR IMPUESTOS DIFERIDOS"
    )

    c_20210_otros_pasivos_no_corrientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 20210 - OTROS PASIVOS NO CORRIENTES"
    )

    c_3_patrimonio_neto = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 3 - PATRIMONIO NETO"
    )

    c_30_patrimonio_neto_atribuible_a_los_propietarios_de_la_controladora = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30 - PATRIMONIO NETO ATRIBUIBLE A LOS PROPIETARIOS DE LA CONTROLADORA"
    )

    c_301_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 301 - CAPITAL"
    )

    c_30101_capital_suscrito_o_asignado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30101 - CAPITAL SUSCRITO O  ASIGNADO"
    )

    c_30102_capital_suscrito_no_pagado_acciones_en_tesoreria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30102 - (-) CAPITAL SUSCRITO NO PAGADO, ACCIONES EN TESORERÍA"
    )

    c_30103_fondo_patrimonial = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30103 - FONDO PATRIMONIAL"
    )

    c_30104_patrimonio_de_los_negocios_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30104 - PATRIMONIO DE LOS NEGOCIOS FIDUCIARIOS"
    )

    c_30105_patrimonio_de_los_fondos_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30105 - PATRIMONIO DE LOS FONDOS DE INVERSIÓN"
    )

    c_3010501_patrimonio_del_fondo_administrado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 3010501 - PATRIMONIO DEL FONDO ADMINISTRADO"
    )

    c_3010502_patrimonio_del_fondo_colectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 3010502 - PATRIMONIO DEL FONDO COLECTIVO"
    )

    c_302_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 302 - APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_303_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 303 - PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_304_reservas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 304 - RESERVAS"
    )

    c_30401_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30401 - RESERVA LEGAL"
    )

    c_30402_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30402 - RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_305_otros_resultados_integrales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 305 - OTROS RESULTADOS INTEGRALES"
    )

    c_30501_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30501 - SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO INTEGRAL"
    )

    c_30502_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30502 - SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_30503_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30503 - SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_30504_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30504 - OTROS SUPERAVIT POR REVALUACION"
    )

    c_306_resultados_acumulados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 306 - RESULTADOS ACUMULADOS"
    )

    c_30601_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30601 - GANANCIAS ACUMULADAS"
    )

    c_30602_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30602 - (-) PÉRDIDAS ACUMULADAS"
    )

    c_30603_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30603 - RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_30604_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30604 - RESERVA DE CAPITAL"
    )

    c_30605_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30605 - RESERVA POR DONACIONES"
    )

    c_30606_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30606 - RESERVA POR VALUACIÓN"
    )

    c_30607_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30607 - SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_307_resultados_del_ejercicio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 307 - RESULTADOS DEL EJERCICIO"
    )

    c_30701_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30701 - GANANCIA NETA DEL PERIODO"
    )

    c_30702_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 30702 - (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_31_participacion_controladora = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 31 - PARTICIPACIÓN CONTROLADORA"
    )

    # =========================
    # ESTADO INTEGRAL DE RESULTADOS
    # =========================

    c_401_ingresos_de_actividades_ordinarias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401 - INGRESOS DE ACTIVIDADES ORDINARIAS"
    )

    c_40101_venta_de_bienes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40101 - VENTA DE BIENES"
    )

    c_40102_prestacion_de_servicios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40102 - PRESTACION DE SERVICIOS"
    )

    c_4010201_ingresos_por_asesoria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010201 - INGRESOS POR ASESORÍA"
    )

    c_4010202_ingresos_por_estructuracion_de_oferta_publica_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010202 - INGRESOS POR ESTRUCTURACIÓN DE OFERTA PÚBLICA DE VALORES"
    )

    c_4010203_ingresos_por_estructuracion_de_negocios_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010203 - INGRESOS POR ESTRUCTURACIÓN DE NEGOCIOS FIDUCIARIOS"
    )

    c_4010204_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010204 - OTROS"
    )

    c_40103_contratos_de_construccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40103 - CONTRATOS DE CONSTRUCCION"
    )

    c_40104_subvenciones_del_gobierno = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40104 - SUBVENCIONES DEL GOBIERNO"
    )

    c_40105_regalias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40105 - REGALÍAS"
    )

    c_40106_intereses = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40106 - INTERESES"
    )

    c_4010601_intereses_generados_por_ventas_a_credito = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010601 - INTERESES GENERADOS POR VENTAS A CREDITO"
    )

    c_4010602_intereses_y_rendimientos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010602 - INTERESES Y RENDIMIENTOS FINANCIEROS"
    )

    c_4010603_otros_intereses_generados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010603 - OTROS INTERESES GENERADOS"
    )

    c_40107_dividendos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40107 - DIVIDENDOS"
    )

    c_40108_ganancia_por_medicion_a_valor_razonable_de_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40108 - GANANCIA POR MEDICION A VALOR RAZONABLE  DE ACTIVOS BIOLOGICOS"
    )

    c_40109_ingresos_por_comisiones_prestacion_de_servicios_custodia_registro_compensacion_y_liquidacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40109 - INGRESOS POR COMISIONES, PRESTACIÓN DE SERVICIOS, CUSTODIA, REGISTRO, COMPENSACIÓN Y LIQUIDACIÓN"
    )

    c_4010901_comisiones_ganadas_por_intermediacion_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010901 - COMISIONES GANADAS POR INTERMEDIACIÓN DE VALORES"
    )

    c_401090101_por_operaciones_bursatiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090101 - POR OPERACIONES BURSATILES"
    )

    c_401090103_por_contratos_de_underwriting = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090103 - POR CONTRATOS DE UNDERWRITING"
    )

    c_401090104_por_comision_en_operaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090104 - POR COMISIÓN EN OPERACIONES"
    )

    c_401090105_por_inscripciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090105 - POR INSCRIPCIONES"
    )

    c_401090106_por_mantenimiento_de_inscripcion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090106 - POR MANTENIMIENTO DE INSCRIPCIÓN"
    )

    c_4010902_por_prestacion_de_servicios_de_administracion_y_manejo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010902 - POR PRESTACIÓN DE SERVICIOS DE ADMINISTRACIÓN Y MANEJO"
    )

    c_401090201_portafolio_de_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090201 - PORTAFOLIO DE TERCEROS"
    )

    c_401090202_fondos_administrados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090202 - FONDOS ADMINISTRADOS"
    )

    c_401090203_fondos_colectivos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090203 - FONDOS COLECTIVOS"
    )

    c_401090204_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090204 - TITULARIZACIÓN"
    )

    c_401090205_fideicomisos_mercantiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090205 - FIDEICOMISOS MERCANTILES"
    )

    c_401090206_encargos_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090206 - ENCARGOS FIDUCIARIOS"
    )

    c_401090207_por_calificacion_de_riesgo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090207 - POR CALIFICACION DE RIESGO"
    )

    c_401090208_por_representacion_de_obligacionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090208 - POR REPRESENTACION DE OBLIGACIONISTAS"
    )

    c_4010903_custodia_registro_compensacion_y_liquidacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4010903 - CUSTODIA, REGISTRO, COMPENSACIÓN Y LIQUIDACIÓN"
    )

    c_401090301_custodia_valores_materializados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090301 - CUSTODIA VALORES MATERIALIZADOS"
    )

    c_401090302_custodia_valores_desmaterializados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090302 - CUSTODIA VALORES DESMATERIALIZADOS"
    )

    c_401090303_compensacion_y_liquidacion_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090303 - COMPENSACIÓN Y LIQUIDACIÓN DE VALORES"
    )

    c_401090304_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 401090304 - OTROS"
    )

    c_40110_ingresos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40110 - INGRESOS  FINANCIEROS"
    )

    c_4011001_dividendos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4011001 - DIVIDENDOS"
    )

    c_4011002_intereses_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4011002 - INTERESES FINANCIEROS"
    )

    c_4011003_ganancia_en_inversiones_en_asociadas_subsidiarias_y_otras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4011003 - GANANCIA EN INVERSIONES EN ASOCIADAS / SUBSIDIARIAS Y OTRAS"
    )

    c_4011004_valuacion_de_instrumentos_financieros_a_valor_razonable_con_cambio_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4011004 - VALUACION DE INSTRUMENTOS FINANCIEROS A VALOR RAZONABLE CON CAMBIO EN RESULTADOS"
    )

    c_4011005_ganancia_en_venta_de_titulos_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4011005 - GANANCIA EN VENTA DE TITULOS VALORES"
    )

    c_4011006_otros_ingresos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 4011006 - OTROS INGRESOS  FINANCIEROS"
    )

    c_40112_descuento_en_ventas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40112 - (-) DESCUENTO EN VENTAS"
    )

    c_40113_devoluciones_en_ventas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40113 - (-) DEVOLUCIONES EN VENTAS"
    )

    c_40114_bonificacion_en_producto = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40114 - (-) BONIFICACIÓN EN PRODUCTO"
    )

    c_40115_otras_rebajas_comerciales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40115 - (-) OTRAS REBAJAS COMERCIALES"
    )

    c_40116_utilidad_en_cambio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40116 - UTILIDAD EN CAMBIO"
    )

    c_402_ganancia_bruta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 402 - GANANCIA BRUTA"
    )

    c_403_otros_ingresos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 403 - OTROS INGRESOS"
    )

    c_40301_ganancia_en_venta_de_propiedad_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40301 - GANANCIA EN VENTA DE PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_40302_ganancia_en_venta_de_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40302 - GANANCIA EN VENTA DE ACTIVOS BIOLÓGICOS"
    )

    c_40303_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 40303 - OTROS"
    )

    c_501_costo_de_ventas_y_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 501 - COSTO DE VENTAS Y PRODUCCIÓN"
    )

    c_50101_materiales_utilizados_o_productos_vendidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50101 - MATERIALES UTILIZADOS O PRODUCTOS VENDIDOS"
    )

    c_5010101_inventario_inicial_de_bienes_no_producidos_por_la_compania = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010101 - (+) INVENTARIO INICIAL DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010102_compras_netas_locales_de_bienes_no_producidos_por_la_compania = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010102 - (+) COMPRAS NETAS LOCALES DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010103_importaciones_de_bienes_no_producidos_por_la_compania = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010103 - (+) IMPORTACIONES DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010104_inventario_final_de_bienes_no_producidos_por_la_compania = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010104 - (-) INVENTARIO FINAL DE BIENES NO PRODUCIDOS POR LA COMPAÑIA"
    )

    c_5010105_inventario_inicial_de_materia_prima = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010105 - (+) INVENTARIO INICIAL DE MATERIA PRIMA"
    )

    c_5010106_compras_netas_locales_de_materia_prima = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010106 - (+) COMPRAS NETAS LOCALES DE MATERIA PRIMA"
    )

    c_5010107_importaciones_de_materia_prima = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010107 - (+) IMPORTACIONES DE MATERIA PRIMA"
    )

    c_5010108_inventario_final_de_materia_prima = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010108 - (-) INVENTARIO FINAL DE MATERIA PRIMA"
    )

    c_5010109_inventario_inicial_de_productos_en_proceso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010109 - (+) INVENTARIO INICIAL DE PRODUCTOS EN PROCESO"
    )

    c_5010110_inventario_final_de_productos_en_proceso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010110 - (-) INVENTARIO FINAL DE PRODUCTOS EN PROCESO"
    )

    c_5010111_inventario_inicial_productos_terminados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010111 - (+) INVENTARIO INICIAL PRODUCTOS TERMINADOS"
    )

    c_5010112_inventario_final_de_productos_terminados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010112 - (-) INVENTARIO FINAL DE PRODUCTOS TERMINADOS"
    )

    c_50102_mano_de_obra_directa = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50102 - (+) MANO DE OBRA DIRECTA"
    )

    c_5010201_sueldos_y_beneficios_sociales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010201 - SUELDOS Y BENEFICIOS SOCIALES"
    )

    c_5010202_gastos_planes_de_beneficios_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010202 - GASTOS PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_50103_mano_de_obra_indirecta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50103 - (+) MANO DE OBRA INDIRECTA"
    )

    c_5010301_sueldos_y_beneficios_sociales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010301 - SUELDOS Y BENEFICIOS SOCIALES"
    )

    c_5010302_gasto_planes_de_beneficios_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010302 - GASTO PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_50104_otros_costos_indirectos_de_fabricacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50104 - (+) OTROS COSTOS INDIRECTOS DE FABRICACION"
    )

    c_5010401_depreciacion_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010401 - DEPRECIACIÓN PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_5010402_deterioro_o_perdidas_de_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010402 - DETERIORO O PERDIDAS DE ACTIVOS BIOLOGICOS"
    )

    c_5010403_deterioro_de_propiedad_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010403 - DETERIORO DE PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_5010404_efecto_valor_neto_de_realizacion_de_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010404 - EFECTO VALOR NETO DE REALIZACION DE INVENTARIOS"
    )

    c_5010405_gasto_por_garantias_en_venta_de_productos_o_servicios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010405 - GASTO POR GARANTIAS EN VENTA DE PRODUCTOS O SERVICIOS"
    )

    c_5010406_mantenimiento_y_reparaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010406 - MANTENIMIENTO Y REPARACIONES"
    )

    c_5010407_suministros_materiales_y_repuestos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010407 - SUMINISTROS MATERIALES Y REPUESTOS"
    )

    c_5010408_otros_costos_de_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010408 - OTROS COSTOS DE PRODUCCIÓN"
    )

    c_50105_costos_de_contratos_de_construcciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50105 - COSTOS DE CONTRATOS DE CONSTRUCCIONES"
    )

    c_5010501_costos_de_acuerdo_a_porcentajes_o_grados_de_terminacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5010501 - COSTOS DE ACUERDO A PORCENTAJES O GRADOS DE TERMINACIÓN"
    )

    c_502_gastos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502 - GASTOS"
    )

    c_50201_gastos_de_venta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50201 - GASTOS DE VENTA"
    )

    c_5020101_sueldos_salarios_y_demas_remuneraciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020101 - SUELDOS, SALARIOS Y DEMÁS REMUNERACIONES"
    )

    c_5020102_aportes_a_la_seguridad_social_incluido_fondo_de_reserva = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020102 - APORTES A LA SEGURIDAD SOCIAL (INCLUIDO FONDO DE RESERVA)"
    )

    c_5020103_beneficios_sociales_e_indemnizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020103 - BENEFICIOS SOCIALES E INDEMNIZACIONES"
    )

    c_5020104_gasto_planes_de_beneficios_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020104 - GASTO PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_5020105_honorarios_comisiones_y_dietas_a_personas_naturales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020105 - HONORARIOS, COMISIONES Y DIETAS A PERSONAS NATURALES"
    )

    c_5020106_remuneraciones_a_otros_trabajadores_autonomos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020106 - REMUNERACIONES A OTROS TRABAJADORES AUTÓNOMOS"
    )

    c_5020107_honorarios_a_extranjeros_por_servicios_ocasionales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020107 - HONORARIOS A EXTRANJEROS POR SERVICIOS OCASIONALES"
    )

    c_5020108_mantenimiento_y_reparaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020108 - MANTENIMIENTO Y REPARACIONES"
    )

    c_5020109_arrendamiento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020109 - ARRENDAMIENTO"
    )

    c_5020110_comisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020110 - COMISIONES"
    )

    c_5020111_promocion_y_publicidad = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020111 - PROMOCIÓN Y PUBLICIDAD"
    )

    c_5020112_combustibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020112 - COMBUSTIBLES"
    )

    c_5020113_lubricantes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020113 - LUBRICANTES"
    )

    c_5020114_seguros_y_reaseguros_primas_y_cesiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020114 - SEGUROS Y REASEGUROS (PRIMAS Y CESIONES)"
    )

    c_5020115_transporte = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020115 - TRANSPORTE"
    )

    c_5020116_gastos_de_gestion_agasajos_a_accionistas_trabajadores_y_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020116 - GASTOS DE GESTIÓN (AGASAJOS A ACCIONISTAS, TRABAJADORES Y CLIENTES)"
    )

    c_5020117_gastos_de_viaje = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020117 - GASTOS DE VIAJE"
    )

    c_5020118_agua_energia_luz_y_telecomunicaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020118 - AGUA, ENERGÍA, LUZ, Y TELECOMUNICACIONES"
    )

    c_5020119_notarios_y_registradores_de_la_propiedad_o_mercantiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020119 - NOTARIOS Y REGISTRADORES DE LA PROPIEDAD O MERCANTILES"
    )

    c_5020120_depreciaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020120 - DEPRECIACIONES:"
    )

    c_502012001_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012001 - PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502012002_propiedades_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012002 - PROPIEDADES DE INVERSIÓN"
    )

    c_502012003_activos_por_derecho_de_uso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012003 - ACTIVOS POR DERECHO DE USO"
    )

    c_5020121_amortizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020121 - AMORTIZACIONES"
    )

    c_502012101_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012101 - INTANGIBLES"
    )

    c_502012102_otros_activos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012102 - OTROS ACTIVOS"
    )

    c_5020122_gasto_deterioro = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020122 - GASTO DETERIORO"
    )

    c_502012201_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012201 - PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502012202_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012202 - INVENTARIOS"
    )

    c_502012203_instrumentos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012203 - INSTRUMENTOS FINANCIEROS"
    )

    c_502012204_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012204 - INTANGIBLES"
    )

    c_502012205_cuentas_por_cobrar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012205 - CUENTAS POR COBRAR"
    )

    c_502012206_otros_activos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012206 - OTROS ACTIVOS"
    )

    c_502012207_derechos_de_uso_por_activos_arrendados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012207 - DERECHOS DE USO POR ACTIVOS ARRENDADOS"
    )

    c_5020123_gastos_por_cantidades_anormales_de_utilizacion_en_el_proceso_de_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020123 - GASTOS POR CANTIDADES ANORMALES DE UTILIZACION EN EL PROCESO DE PRODUCCIÓN:"
    )

    c_502012301_mano_de_obra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012301 - MANO DE OBRA"
    )

    c_502012302_materiales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012302 - MATERIALES"
    )

    c_502012303_costos_de_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502012303 - COSTOS DE PRODUCCION"
    )

    c_5020124_gasto_por_reestructuracion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020124 - GASTO POR REESTRUCTURACION"
    )

    c_5020125_valor_neto_de_realizacion_de_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020125 - VALOR NETO DE REALIZACION DE INVENTARIOS"
    )

    c_5020126_gasto_impuesto_a_la_renta_activos_y_pasivos_diferidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020126 - GASTO IMPUESTO A LA RENTA (ACTIVOS Y PASIVOS DIFERIDOS)"
    )

    c_5020127_suministros_y_materiales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020127 - SUMINISTROS Y MATERIALES"
    )

    c_5020128_otros_gastos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020128 - OTROS GASTOS"
    )

    c_50202_gastos_administrativos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50202 - GASTOS ADMINISTRATIVOS"
    )

    c_5020201_sueldos_salarios_y_demas_remuneraciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020201 - SUELDOS, SALARIOS Y DEMÁS REMUNERACIONES"
    )

    c_5020202_aportes_a_la_seguridad_social_incluido_fondo_de_reserva = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020202 - APORTES A LA SEGURIDAD SOCIAL (INCLUIDO FONDO DE RESERVA)"
    )

    c_5020203_beneficios_sociales_e_indemnizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020203 - BENEFICIOS SOCIALES E INDEMNIZACIONES"
    )

    c_5020204_gasto_planes_de_beneficios_a_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020204 - GASTO PLANES DE BENEFICIOS A EMPLEADOS"
    )

    c_5020205_honorarios_comisiones_y_dietas_a_personas_naturales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020205 - HONORARIOS, COMISIONES Y DIETAS A PERSONAS NATURALES"
    )

    c_5020206_remuneraciones_a_otros_trabajadores_autonomos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020206 - REMUNERACIONES A OTROS TRABAJADORES AUTÓNOMOS"
    )

    c_5020207_honorarios_a_extranjeros_por_servicios_ocasionales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020207 - HONORARIOS A EXTRANJEROS POR SERVICIOS OCASIONALES"
    )

    c_5020208_mantenimiento_y_reparaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020208 - MANTENIMIENTO Y REPARACIONES"
    )

    c_5020209_arrendamiento = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020209 - ARRENDAMIENTO"
    )

    c_5020210_comisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020210 - COMISIONES"
    )

    c_5020211_promocion_y_publicidad = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020211 - PROMOCIÓN Y PUBLICIDAD"
    )

    c_5020212_combustibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020212 - COMBUSTIBLES"
    )

    c_5020213_lubricantes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020213 - LUBRICANTES"
    )

    c_5020214_seguros_y_reaseguros_primas_y_cesiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020214 - SEGUROS Y REASEGUROS (PRIMAS Y CESIONES)"
    )

    c_5020215_transporte = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020215 - TRANSPORTE"
    )

    c_5020216_gastos_de_gestion_agasajos_a_accionistas_trabajadores_y_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020216 - GASTOS DE GESTIÓN (AGASAJOS A ACCIONISTAS, TRABAJADORES Y CLIENTES)"
    )

    c_5020217_gastos_de_viaje = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020217 - GASTOS DE VIAJE"
    )

    c_5020218_agua_energia_luz_y_telecomunicaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020218 - AGUA, ENERGÍA, LUZ, Y TELECOMUNICACIONES"
    )

    c_5020219_notarios_y_registradores_de_la_propiedad_o_mercantiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020219 - NOTARIOS Y REGISTRADORES DE LA PROPIEDAD O MERCANTILES"
    )

    c_5020220_impuestos_contribuciones_y_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020220 - IMPUESTOS, CONTRIBUCIONES Y OTROS"
    )

    c_5020221_depreciaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020221 - DEPRECIACIONES"
    )

    c_502022101_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022101 - PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502022102_propiedades_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022102 - PROPIEDADES DE INVERSIÓN"
    )

    c_502022103_activos_por_derecho_de_uso = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022103 - ACTIVOS POR DERECHO DE USO"
    )

    c_5020222_amortizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020222 - AMORTIZACIONES"
    )

    c_502022201_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022201 - INTANGIBLES"
    )

    c_502022202_otros_activos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022202 - OTROS ACTIVOS"
    )

    c_5020223_gasto_deterioro = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020223 - GASTO DETERIORO:"
    )

    c_502022301_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022301 - PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_502022302_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022302 - INVENTARIOS"
    )

    c_502022303_instrumentos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022303 - INSTRUMENTOS FINANCIEROS"
    )

    c_502022304_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022304 - INTANGIBLES"
    )

    c_502022305_cuentas_por_cobrar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022305 - CUENTAS POR COBRAR"
    )

    c_502022306_otros_activos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022306 - OTROS ACTIVOS"
    )

    c_502022307_derechos_de_uso_por_activos_arrendados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022307 - DERECHOS DE USO POR ACTIVOS ARRENDADOS"
    )

    c_5020224_gastos_por_cantidades_anormales_de_utilizacion_en_el_proceso_de_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020224 - GASTOS POR CANTIDADES ANORMALES DE UTILIZACION EN EL PROCESO DE PRODUCCIÓN"
    )

    c_502022401_mano_de_obra = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022401 - MANO DE OBRA"
    )

    c_502022402_materiales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022402 - MATERIALES"
    )

    c_502022403_costos_de_produccion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502022403 - COSTOS DE PRODUCCION"
    )

    c_5020225_gasto_por_reestructuracion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020225 - GASTO POR REESTRUCTURACION"
    )

    c_5020226_valor_neto_de_realizacion_de_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020226 - VALOR NETO DE REALIZACION DE INVENTARIOS"
    )

    c_5020227_gasto_impuesto_a_la_renta_activos_y_pasivos_diferidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020227 - GASTO IMPUESTO A LA RENTA (ACTIVOS Y PASIVOS DIFERIDOS)"
    )

    c_5020228_suministros_y_materiales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020228 - SUMINISTROS Y MATERIALES"
    )

    c_5020229_otros_gastos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020229 - OTROS GASTOS"
    )

    c_50203_gastos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50203 - GASTOS FINANCIEROS"
    )

    c_5020301_intereses = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020301 - INTERESES"
    )

    c_502030101_intereses_por_prestamos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030101 - INTERESES POR PRESTAMOS"
    )

    c_502030102_intereses_por_arrendamientos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030102 - INTERESES POR ARRENDAMIENTOS"
    )

    c_502030103_intereses_por_valores_emitidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030103 - INTERESES POR VALORES EMITIDOS"
    )

    c_502030104_otros_intereses = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030104 - OTROS INTERESES"
    )

    c_5020302_comisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020302 - COMISIONES"
    )

    c_502030201_comisiones_pagadas_por_intermediacion_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030201 - COMISIONES PAGADAS POR INTERMEDIACIÓN DE VALORES:"
    )

    c_50203020101_por_operaciones_bursatiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50203020101 - POR OPERACIONES BURSATILES"
    )

    c_50203020103_por_contratos_de_underwriting = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50203020103 - POR CONTRATOS DE UNDERWRITING"
    )

    c_50203020104_por_comision_en_operaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50203020104 - POR COMISIÓN EN OPERACIONES"
    )

    c_50203020105_por_inscripciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50203020105 - POR INSCRIPCIONES"
    )

    c_50203020106_por_mantenimiento_de_inscripcion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50203020106 - POR MANTENIMIENTO DE INSCRIPCIÓN"
    )

    c_5020303_por_prestacion_de_servicios_de_administracion_y_manejo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020303 - POR PRESTACIÓN DE SERVICIOS DE ADMINISTRACIÓN Y MANEJO"
    )

    c_502030301_portafolio_de_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030301 - PORTAFOLIO DE TERCEROS"
    )

    c_502030302_fondos_administrados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030302 - FONDOS ADMINISTRADOS"
    )

    c_502030303_fondos_colectivos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030303 - FONDOS COLECTIVOS"
    )

    c_502030304_titularizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030304 - TITULARIZACIÓN"
    )

    c_502030305_fideicomisos_mercantiles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030305 - FIDEICOMISOS MERCANTILES"
    )

    c_502030306_encargos_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030306 - ENCARGOS FIDUCIARIOS"
    )

    c_502030307_por_calificacion_de_riesgo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030307 - POR CALIFICACION DE RIESGO"
    )

    c_502030308_por_representacion_de_obligacionistas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030308 - POR REPRESENTACION DE OBLIGACIONISTAS"
    )

    c_5020304_custodia_registro_compensacion_y_liquidacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020304 - CUSTODIA, REGISTRO, COMPENSACIÓN Y LIQUIDACIÓN"
    )

    c_502030401_custodia_valores_materializados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030401 - CUSTODIA VALORES MATERIALIZADOS"
    )

    c_502030402_custodia_valores_desmaterializados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030402 - CUSTODIA VALORES DESMATERIALIZADOS"
    )

    c_502030403_compensacion_y_liquidacion_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030403 - COMPENSACIÓN Y LIQUIDACIÓN DE VALORES"
    )

    c_502030404_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030404 - OTROS"
    )

    c_5020305_gastos_por_servicios_de_asesoria_y_estructuracion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020305 - GASTOS POR SERVICIOS DE ASESORIA Y ESTRUCTURACION"
    )

    c_502030501_por_asesoria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030501 - POR ASESORÍA"
    )

    c_502030502_por_estructuracion_de_oferta_publica_de_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030502 - POR ESTRUCTURACIÓN DE OFERTA PÚBLICA DE VALORES"
    )

    c_502030503_por_estructuracion_de_negocios_fiduciarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030503 - POR ESTRUCTURACIÓN DE NEGOCIOS FIDUCIARIOS"
    )

    c_502030504_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 502030504 - OTROS"
    )

    c_5020306_gastos_de_financiamiento_de_activos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020306 - GASTOS DE FINANCIAMIENTO DE ACTIVOS"
    )

    c_5020307_diferencia_en_cambio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020307 - DIFERENCIA EN CAMBIO"
    )

    c_5020308_valuacion_de_instrumentos_financieros_a_valor_razonable_con_cambio_en_resultados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020308 - VALUACION DE INSTRUMENTOS FINANCIEROS A VALOR RAZONABLE CON CAMBIO EN RESULTADOS"
    )

    c_5020309_perdida_en_venta_de_titulos_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020309 - PERDIDA EN VENTA DE TITULOS VALORES"
    )

    c_5020310_perdida_en_venta_de_propiedad_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020310 - PERDIDA EN VENTA DE PROPIEDAD, PLANTA Y EQUIPO"
    )

    c_5020311_perdida_en_venta_de_activos_biologicos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020311 - PERDIDA EN VENTA DE ACTIVOS BIOLOGICOS"
    )

    c_5020312_otros_gastos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020312 - OTROS GASTOS FINANCIEROS"
    )

    c_50204_otros_gastos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 50204 - OTROS GASTOS"
    )

    c_5020401_perdida_en_inversiones_en_asociadas_subsidiarias_y_otras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020401 - PERDIDA EN INVERSIONES EN ASOCIADAS / SUBSIDIARIAS Y OTRAS"
    )

    c_5020402_otros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 5020402 - OTROS"
    )

    c_600_ganancia_perdida_antes_de_15_a_trabajadores_e_impuesto_a_la_renta_de_operaciones_continuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 600 - GANANCIA (PÉRDIDA) ANTES DE 15% A TRABAJADORES E IMPUESTO A LA RENTA DE OPERACIONES CONTINUADAS"
    )

    c_601_15_participacion_trabajadores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 601 - 15% PARTICIPACIÓN TRABAJADORES"
    )

    c_602_ganancia_perdida_antes_de_impuestos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 602 - GANANCIA (PÉRDIDA) ANTES DE IMPUESTOS"
    )

    c_603_impuesto_a_la_renta_causado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 603 - IMPUESTO A LA RENTA CAUSADO"
    )

    c_604_ganancia_perdida_de_operaciones_continuadas_antes_del_impuesto_diferido = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 604 - GANANCIA (PÉRDIDA) DE OPERACIONES CONTINUADAS ANTES DEL IMPUESTO DIFERIDO"
    )

    c_605_gasto_por_impuesto_diferido = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 605 - (-) GASTO POR IMPUESTO DIFERIDO"
    )

    c_606_ingreso_por_impuesto_diferido = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 606 - (+) INGRESO POR IMPUESTO DIFERIDO"
    )

    c_607_ganancia_perdida_de_operaciones_continuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 607 - GANANCIA (PERDIDA) DE OPERACIONES CONTINUADAS"
    )

    c_700_ingresos_por_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 700 - INGRESOS POR OPERACIONES DISCONTINUADAS"
    )

    c_701_gastos_por_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 701 - GASTOS POR OPERACIONES DISCONTINUADAS"
    )

    c_702_ganancia_perdida_antes_de_15_a_trabajadores_e_impuesto_a_la_renta_de_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 702 - GANANCIA (PÉRDIDA) ANTES DE 15% A TRABAJADORES E IMPUESTO A LA RENTA DE OPERACIONES DISCONTINUADAS"
    )

    c_703_15_participacion_trabajadores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 703 - 15% PARTICIPACIÓN TRABAJADORES"
    )

    c_704_ganancia_perdida_antes_de_impuestos_de_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 704 - GANANCIA (PÉRDIDA) ANTES DE IMPUESTOS DE OPERACIONES DISCONTINUADAS"
    )

    c_705_impuesto_a_la_renta_causado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 705 - IMPUESTO A LA RENTA CAUSADO"
    )

    c_706_ganancia_perdida_de_operaciones_discontinuadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 706 - GANANCIA (PÉRDIDA) DE OPERACIONES DISCONTINUADAS"
    )

    c_707_ganancia_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 707 - GANANCIA (PÉRDIDA) NETA DEL PERIODO"
    )

    c_800_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 800 - OTRO RESULTADO INTEGRAL"
    )

    c_80001_componentes_del_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80001 - COMPONENTES DEL OTRO RESULTADO INTEGRAL"
    )

    c_80002_diferencia_de_cambio_por_conversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80002 - DIFERENCIA DE CAMBIO POR CONVERSIÓN"
    )

    c_80003_valuacion_de_activos_financieros_a_valor_razonable_con_cambio_en_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80003 - VALUACIÓN DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIO EN OTRO RESULTADO INTEGRAL"
    )

    c_80004_ganancias_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80004 - GANANCIAS POR REVALUACIÓN DE PROPIEDADES, PLANTA  Y EQUIPO"
    )

    c_80005_ganancias_perdidas_actuariales_por_planes_de_beneficios_definidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80005 - GANANCIAS (PÉRDIDAS) ACTUARIALES POR PLANES DE BENEFICIOS DEFINIDOS"
    )

    c_80006_reversion_del_deterioro_perdida_por_deterioro_de_un_activo_revaluado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80006 - REVERSION DEL DETERIORO (PÉRDIDA POR DETERIORO) DE UN ACTIVO REVALUADO"
    )

    c_80007_participacion_de_otro_resultado_integral_de_asociadas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80007 - PARTICIPACION DE OTRO RESULTADO INTEGRAL DE ASOCIADAS"
    )

    c_80008_impuesto_sobre_las_ganancias_relativo_a_otro_resultado_integral = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80008 - IMPUESTO SOBRE LAS GANANCIAS RELATIVO A OTRO RESULTADO INTEGRAL"
    )

    c_80009_otros_detallar_en_notas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80009 - OTROS (DETALLAR EN NOTAS)"
    )

    c_801_resultado_integral_total_del_ano = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 801 - RESULTADO INTEGRAL TOTAL DEL AÑO"
    )

    c_80101_propietarios_de_la_controladora = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80101 - PROPIETARIOS DE LA CONTROLADORA"
    )

    c_80102_participacion_no_controladora_informativo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 80102 - PARTICIPACION NO CONTROLADORA (INFORMATIVO)"
    )
    # =========================
    # CAMBIOS EN EL PATRIMONIO
    # =========================
    equity_opening_balance = models.DecimalField(
        "Saldo inicial del patrimonio", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Saldo total del patrimonio al inicio del ejercicio fiscal."
    )
    equity_increases = models.DecimalField(
        "Incrementos del patrimonio", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Aumentos en el patrimonio durante el periodo, incluyendo aportes de socios y utilidades netas."
    )
    equity_decreases = models.DecimalField(
        "Disminuciones del patrimonio", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Reducciones en el patrimonio durante el periodo, como distribución de dividendos o pérdidas netas."
    )
    equity_closing_balance = models.DecimalField(
        "Saldo final del patrimonio", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Saldo total del patrimonio al cierre del ejercicio fiscal."
    )

    # =========================
    # FLUJO DE EFECTIVO
    # =========================

    c_95_incremento_neto_disminucion_en_el_efectivo_y_equivalentes_al_efectivo_antes_del_efecto_de_los_cambios_en_la_tasa_de_cambio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95 - INCREMENTO NETO (DISMINUCIÓN) EN EL EFECTIVO Y EQUIVALENTES AL EFECTIVO, ANTES DEL EFECTO DE LOS CAMBIOS EN LA TASA DE CAMBIO"
    )

    c_9501_flujos_de_efectivo_procedentes_de_utilizados_en_actividades_de_operacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9501 - FLUJOS DE EFECTIVO PROCEDENTES DE (UTILIZADOS EN) ACTIVIDADES DE OPERACIÓN"
    )

    c_950101_clases_de_cobros_por_actividades_de_operacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950101 - Clases de cobros por actividades de operación"
    )

    c_95010101_cobros_procedentes_de_las_ventas_de_bienes_y_prestacion_de_servicios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010101 - Cobros procedentes de las ventas de bienes y prestación de servicios"
    )

    c_95010102_cobros_procedentes_de_regalias_cuotas_comisiones_y_otros_ingresos_de_actividades_ordinarias = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010102 - Cobros procedentes de regalías, cuotas, comisiones y otros ingresos de actividades ordinarias"
    )

    c_95010103_cobros_procedentes_de_contratos_mantenidos_con_propositos_de_intermediacion_o_para_negociar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010103 - Cobros procedentes de contratos mantenidos con propósitos de intermediación o para negociar"
    )

    c_95010104_cobros_procedentes_de_primas_y_prestaciones_anualidades_y_otros_beneficios_de_polizas_suscritas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010104 - Cobros procedentes de primas y prestaciones, anualidades y otros beneficios de pólizas suscritas"
    )

    c_95010105_otros_cobros_por_actividades_de_operacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010105 - Otros cobros por actividades de operación"
    )

    c_950102_clases_de_pagos_por_actividades_de_operacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950102 - Clases de pagos por actividades de operación"
    )

    c_95010201_pagos_a_proveedores_por_el_suministro_de_bienes_y_servicios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010201 - Pagos a proveedores por el suministro de bienes y servicios"
    )

    c_95010202_pagos_procedentes_de_contratos_mantenidos_para_intermediacion_o_para_negociar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010202 - Pagos procedentes de contratos mantenidos para intermediación o para negociar"
    )

    c_95010203_pagos_a_y_por_cuenta_de_los_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010203 - Pagos a y por cuenta de los empleados"
    )

    c_95010204_pagos_por_primas_y_prestaciones_anualidades_y_otras_obligaciones_derivadas_de_las_polizas_suscritas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010204 - Pagos por primas y prestaciones, anualidades y otras obligaciones derivadas de las pólizas suscritas"
    )

    c_95010205_otros_pagos_por_actividades_de_operacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 95010205 - Otros pagos por actividades de operación"
    )

    c_950103_dividendos_pagados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950103 - Dividendos pagados"
    )

    c_950104_dividendos_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950104 - Dividendos recibidos"
    )

    c_950105_intereses_pagados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950105 - Intereses pagados"
    )

    c_950106_intereses_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950106 - Intereses recibidos"
    )

    c_950107_impuestos_a_las_ganancias_pagados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950107 - Impuestos a las ganancias pagados"
    )

    c_950108_otras_entradas_salidas_de_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950108 - Otras entradas (salidas) de efectivo"
    )

    c_9502_flujos_de_efectivo_procedentes_de_utilizados_en_actividades_de_inversion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9502 - FLUJOS DE EFECTIVO PROCEDENTES DE (UTILIZADOS EN) ACTIVIDADES DE INVERSIÓN"
    )

    c_950201_efectivo_procedentes_de_la_venta_de_acciones_en_subsidiarias_u_otros_negocios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950201 - Efectivo procedentes de la venta de acciones en subsidiarias u otros negocios"
    )

    c_950202_efectivo_utilizado_para_adquirir_acciones_en_subsidiarias_u_otros_negocios_para_tener_el_control = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950202 - Efectivo utilizado para adquirir acciones en subsidiarias u otros negocios para tener el control"
    )

    c_950203_efectivo_utilizado_en_la_compra_de_participaciones_no_controladoras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950203 - Efectivo utilizado en la compra de participaciones no controladoras"
    )

    c_950204_otros_cobros_por_la_venta_de_acciones_o_instrumentos_de_deuda_de_otras_entidades = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950204 - Otros cobros por la venta de acciones o instrumentos de deuda de otras entidades"
    )

    c_950205_otros_pagos_para_adquirir_acciones_o_instrumentos_de_deuda_de_otras_entidades = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950205 - Otros pagos para adquirir acciones o instrumentos de deuda de otras entidades"
    )

    c_950206_otros_cobros_por_la_venta_de_participaciones_en_negocios_conjuntos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950206 - Otros cobros por la venta de participaciones en negocios conjuntos"
    )

    c_950207_otros_pagos_para_adquirir_participaciones_en_negocios_conjuntos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950207 - Otros pagos para adquirir participaciones en negocios conjuntos"
    )

    c_950208_importes_procedentes_por_la_venta_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950208 - Importes procedentes por la venta de propiedades, planta y equipo"
    )

    c_950209_adquisiciones_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950209 - Adquisiciones de propiedades, planta y equipo"
    )

    c_950210_importes_procedentes_de_ventas_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950210 - Importes procedentes de ventas de activos intangibles"
    )

    c_950211_compras_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950211 - Compras de activos intangibles"
    )

    c_950212_importes_procedentes_de_otros_activos_a_largo_plazo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950212 - Importes procedentes de otros activos a largo plazo"
    )

    c_950213_compras_de_otros_activos_a_largo_plazo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950213 - Compras de otros activos a largo plazo"
    )

    c_950214_importes_procedentes_de_subvenciones_del_gobierno = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950214 - Importes procedentes de subvenciones del gobierno"
    )

    c_950215_anticipos_de_efectivo_efectuados_a_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950215 - Anticipos de efectivo efectuados a terceros"
    )

    c_950216_cobros_procedentes_del_reembolso_de_anticipos_y_prestamos_concedidos_a_terceros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950216 - Cobros procedentes del reembolso de anticipos y préstamos concedidos a terceros"
    )

    c_950217_pagos_derivados_de_contratos_de_futuro_a_termino_de_opciones_y_de_permuta_financiera = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950217 - Pagos derivados de contratos de futuro, a término, de opciones y de permuta financiera"
    )

    c_950218_cobros_procedentes_de_contratos_de_futuro_a_termino_de_opciones_y_de_permuta_financiera = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950218 - Cobros procedentes de contratos de futuro, a término, de opciones y de permuta financiera"
    )

    c_950219_dividendos_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950219 - Dividendos recibidos"
    )

    c_950220_intereses_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950220 - Intereses recibidos"
    )

    c_950221_otras_entradas_salidas_de_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950221 - Otras entradas (salidas) de efectivo"
    )

    c_9503_flujos_de_efectivo_procedentes_de_utilizados_en_actividades_de_financiacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9503 - FLUJOS DE EFECTIVO PROCEDENTES DE (UTILIZADOS EN) ACTIVIDADES DE FINANCIACIÓN"
    )

    c_950301_aporte_en_efectivo_por_aumento_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950301 - Aporte en efectivo por aumento de capital"
    )

    c_950302_financiamiento_por_emision_de_titulos_valores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950302 - Financiamiento por emisión de títulos valores"
    )

    c_950303_pagos_por_adquirir_o_rescatar_las_acciones_de_la_entidad = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950303 - Pagos por adquirir o rescatar las acciones de la entidad"
    )

    c_950304_financiacion_por_prestamos_a_largo_plazo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950304 - Financiación por préstamos a largo plazo"
    )

    c_950305_pagos_de_prestamos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950305 - Pagos de préstamos"
    )

    c_950306_pagos_de_pasivos_por_arrendamientos_financieros = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950306 - Pagos de pasivos por arrendamientos financieros"
    )

    c_950307_importes_procedentes_de_subvenciones_del_gobierno = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950307 - Importes procedentes de subvenciones del gobierno"
    )

    c_950308_dividendos_pagados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950308 - Dividendos pagados"
    )

    c_950309_intereses_recibidos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950309 - Intereses recibidos"
    )

    c_950310_otras_entradas_salidas_de_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950310 - Otras entradas (salidas) de efectivo"
    )

    c_9504_efectos_de_la_variacion_en_la_tasa_de_cambio_sobre_el_efectivo_y_equivalentes_al_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9504 - EFECTOS DE LA VARIACION EN LA TASA DE CAMBIO SOBRE EL EFECTIVO Y EQUIVALENTES AL EFECTIVO"
    )

    c_950401_efectos_de_la_variacion_en_la_tasa_de_cambio_sobre_el_efectivo_y_equivalentes_al_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 950401 - Efectos de la variación en la tasa de cambio sobre el efectivo y equivalentes al efectivo"
    )

    c_9505_incremento_disminucion_neto_de_efectivo_y_equivalentes_al_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9505 - INCREMENTO (DISMINUCIÓN) NETO DE EFECTIVO Y EQUIVALENTES AL EFECTIVO"
    )

    c_9506_efectivo_y_equivalentes_al_efectivo_al_principio_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9506 - EFECTIVO Y EQUIVALENTES AL EFECTIVO AL PRINCIPIO DEL PERIODO"
    )

    c_9507_efectivo_y_equivalentes_al_efectivo_al_final_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9507 - EFECTIVO Y EQUIVALENTES AL EFECTIVO AL FINAL DEL PERIODO"
    )

    c_96_ganancia_perdida_antes_de_15_a_trabajadores_e_impuesto_a_la_renta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 96 - GANANCIA (PÉRDIDA) ANTES DE 15% A TRABAJADORES E IMPUESTO A LA RENTA"
    )

    c_97_ajuste_por_partidas_distintas_al_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 97 - AJUSTE POR PARTIDAS DISTINTAS AL EFECTIVO"
    )

    c_9701_ajustes_por_gasto_de_depreciacion_y_amortizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9701 - Ajustes por gasto de depreciación y amortización"
    )

    c_9702_ajustes_por_gastos_por_deterioro_reversiones_por_deterioro_reconocidas_en_los_resultados_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9702 - Ajustes por gastos por deterioro (reversiones por deterioro) reconocidas en los resultados del periodo"
    )

    c_9703_perdida_ganancia_de_moneda_extranjera_no_realizada = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9703 - Pérdida (ganancia) de moneda extranjera no realizada"
    )

    c_9704_perdidas_en_cambio_de_moneda_extranjera = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9704 - Pérdidas en cambio de moneda extranjera"
    )

    c_9705_ajustes_por_gastos_en_provisiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9705 - Ajustes por gastos en provisiones"
    )

    c_9706_ajuste_por_participaciones_no_controladoras = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9706 - Ajuste por participaciones no controladoras"
    )

    c_9707_ajuste_por_pagos_basados_en_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9707 - Ajuste por pagos basados en acciones"
    )

    c_9708_ajustes_por_ganancias_perdidas_en_valor_razonable = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9708 - Ajustes por ganancias (pérdidas) en valor razonable"
    )

    c_9709_ajustes_por_gasto_por_impuesto_a_la_renta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9709 - Ajustes por gasto por impuesto a la renta"
    )

    c_9710_ajustes_por_gasto_por_participacion_trabajadores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9710 - Ajustes por gasto por participación trabajadores"
    )

    c_9711_otros_ajustes_por_partidas_distintas_al_efectivo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9711 - Otros ajustes por partidas distintas al efectivo"
    )

    c_98_cambios_en_activos_y_pasivos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 98 - CAMBIOS EN ACTIVOS Y PASIVOS"
    )

    c_9801_incremento_disminucion_en_cuentas_por_cobrar_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9801 - (Incremento) disminución en cuentas por cobrar clientes"
    )

    c_9802_incremento_disminucion_en_otras_cuentas_por_cobrar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9802 - (Incremento) disminución en otras cuentas por cobrar"
    )

    c_9803_incremento_disminucion_en_anticipos_de_proveedores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9803 - (Incremento) disminución en anticipos de proveedores"
    )

    c_9804_incremento_disminucion_en_inventarios = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9804 - (Incremento) disminución en inventarios"
    )

    c_9805_incremento_disminucion_en_otros_activos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9805 - (Incremento) disminución en otros activos"
    )

    c_9806_incremento_disminucion_en_cuentas_por_pagar_comerciales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9806 - Incremento  (disminución) en cuentas por pagar comerciales"
    )

    c_9807_incremento_disminucion_en_otras_cuentas_por_pagar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9807 - Incremento  (disminución) en otras cuentas por pagar"
    )

    c_9808_incremento_disminucion_en_beneficios_empleados = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9808 - Incremento  (disminución) en beneficios empleados"
    )

    c_9809_incremento_disminucion_en_anticipos_de_clientes = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9809 - Incremento  (disminución) en anticipos de clientes"
    )

    c_9810_incremento_disminucion_en_otros_pasivos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9810 - Incremento  (disminución) en otros pasivos"
    )

    c_9820_flujos_de_efectivo_netos_procedentes_de_utilizados_en_actividades_de_operacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9820 - Flujos de efectivo netos procedentes de (utilizados en) actividades de operación"
    )


#PATRIMONIO


    c_99_301_saldo_al_final_del_periodo_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 301 | SALDO AL FINAL DEL PERIODO / CAPITAL"
    )

    c_99_302_saldo_al_final_del_periodo_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 302 | SALDO AL FINAL DEL PERIODO / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_99_303_saldo_al_final_del_periodo_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 303 | SALDO AL FINAL DEL PERIODO / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_99_30401_saldo_al_final_del_periodo_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30401 | SALDO AL FINAL DEL PERIODO / RESERVA LEGAL"
    )

    c_99_30402_saldo_al_final_del_periodo_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30402 | SALDO AL FINAL DEL PERIODO / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_99_30501_saldo_al_final_del_periodo_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30501 | SALDO AL FINAL DEL PERIODO / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_99_30502_saldo_al_final_del_periodo_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30502 | SALDO AL FINAL DEL PERIODO / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_99_30503_saldo_al_final_del_periodo_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30503 | SALDO AL FINAL DEL PERIODO / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_99_30504_saldo_al_final_del_periodo_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30504 | SALDO AL FINAL DEL PERIODO / OTROS SUPERAVIT POR REVALUACION"
    )

    c_99_30601_saldo_al_final_del_periodo_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30601 | SALDO AL FINAL DEL PERIODO / GANANCIAS ACUMULADAS"
    )

    c_99_30602_saldo_al_final_del_periodo_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30602 | SALDO AL FINAL DEL PERIODO / (-) PÉRDIDAS ACUMULADAS"
    )

    c_99_30603_saldo_al_final_del_periodo_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30603 | SALDO AL FINAL DEL PERIODO / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_99_30604_saldo_al_final_del_periodo_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30604 | SALDO AL FINAL DEL PERÍODO / RESERVA DE CAPITAL"
    )

    c_99_30605_saldo_al_final_del_periodo_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30605 | SALDO AL FINAL DEL PERÍODO / RESERVA POR DONACIONES"
    )

    c_99_30606_saldo_al_final_del_periodo_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30606 | SALDO AL FINAL DEL PERÍODO / RESERVA POR VALUACIÓN"
    )

    c_99_30607_saldo_al_final_del_periodo_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30607 | SALDO AL FINAL DEL PERIODO / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_99_30701_saldo_al_final_del_periodo_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30701 | SALDO AL FINAL DEL PERIODO / GANANCIA NETA DEL PERIODO"
    )

    c_99_30702_saldo_al_final_del_periodo_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30702 | SALDO AL FINAL DEL PERIODO / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_9901_301_saldo_reexpresado_del_periodo_inmediato_anterior_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 301 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / CAPITAL"
    )

    c_9901_302_saldo_reexpresado_del_periodo_inmediato_anterior_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 302 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_9901_303_saldo_reexpresado_del_periodo_inmediato_anterior_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 303 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_9901_30401_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30401 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / / RESERVA LEGAL"
    )

    c_9901_30402_saldo_reexpresado_del_periodo_inmediato_anterior_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30402 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_9901_30501_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30501 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_9901_30502_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30502 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_9901_30503_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30503 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_9901_30504_saldo_reexpresado_del_periodo_inmediato_anterior_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30504 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_9901_30601_saldo_reexpresado_del_periodo_inmediato_anterior_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30601 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / GANANCIAS ACUMULADAS"
    )

    c_9901_30602_saldo_reexpresado_del_periodo_inmediato_anterior_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30602 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / (-) PÉRDIDAS ACUMULADAS"
    )

    c_9901_30603_saldo_reexpresado_del_periodo_inmediato_anterior_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30603 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_9901_30604_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30604 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / RESERVA DE CAPITAL"
    )

    c_9901_30605_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30605 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR / RESERVA POR DONACIONES"
    )

    c_9901_30606_saldo_reexpresado_del_periodo_inmediato_anterior_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30606 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / RESERVA POR VALUACIÓN"
    )

    c_9901_30607_saldo_reexpresado_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30607 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_9901_30701_saldo_reexpresado_del_periodo_inmediato_anterior_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30701 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / GANANCIA NETA DEL PERIODO"
    )

    c_9901_30702_saldo_reexpresado_del_periodo_inmediato_anterior_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30702 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990101_301_saldo_del_periodo_inmediato_anterior_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 301 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / CAPITAL"
    )

    c_990101_302_saldo_del_periodo_inmediato_anterior_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 302 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990101_303_saldo_del_periodo_inmediato_anterior_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 303 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990101_30401_saldo_del_periodo_inmediato_anterior_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30401 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / RESERVA LEGAL"
    )

    c_990101_30402_saldo_del_periodo_inmediato_anterior_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30402 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990101_30501_saldo_del_periodo_inmediato_anterior_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30501 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990101_30502_saldo_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30502 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990101_30503_saldo_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30503 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990101_30504_saldo_del_periodo_inmediato_anterior_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30504 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990101_30601_saldo_del_periodo_inmediato_anterior_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30601 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / GANANCIAS ACUMULADAS"
    )

    c_990101_30602_saldo_del_periodo_inmediato_anterior_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30602 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990101_30603_saldo_del_periodo_inmediato_anterior_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30603 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990101_30604_saldo_del_periodo_inmediato_anterior_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30604 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / RESERVA DE CAPITAL"
    )

    c_990101_30605_saldo_del_periodo_inmediato_anterior_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30605 | SALDO DEL PERÍODO INMEDIATO ANTERIOR / RESERVA POR DONACIONES"
    )

    c_990101_30606_saldo_del_periodo_inmediato_anterior_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30606 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / RESERVA POR VALUACIÓN"
    )

    c_990101_30607_saldo_del_periodo_inmediato_anterior_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30607 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990101_30701_saldo_del_periodo_inmediato_anterior_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30701 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / GANANCIA NETA DEL PERIODO"
    )

    c_990101_30702_saldo_del_periodo_inmediato_anterior_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30702 | SALDO DEL PERÍODO INMEDIATO ANTERIOR  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990102_301_cambios_en_politicas_contables_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 301 | CAMBIOS EN POLITICAS CONTABLES: / CAPITAL"
    )

    c_990102_302_cambios_en_politicas_contables_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 302 | CAMBIOS EN POLITICAS CONTABLES:  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990102_303_cambios_en_politicas_contables_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 303 | CAMBIOS EN POLITICAS CONTABLES:  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990102_30401_cambios_en_politicas_contables_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30401 | CAMBIOS EN POLITICAS CONTABLES: / RESERVA LEGAL"
    )

    c_990102_30402_cambios_en_politicas_contables_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30402 | CAMBIOS EN POLITICAS CONTABLES:  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990102_30501_cambios_en_politicas_contables_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30501 | CAMBIOS EN POLITICAS CONTABLES: / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990102_30502_cambios_en_politicas_contables_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30502 | CAMBIOS EN POLITICAS CONTABLES:  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990102_30503_cambios_en_politicas_contables_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30503 | CAMBIOS EN POLITICAS CONTABLES:  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990102_30504_cambios_en_politicas_contables_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30504 | CAMBIOS EN POLITICAS CONTABLES:  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990102_30601_cambios_en_politicas_contables_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30601 | CAMBIOS EN POLITICAS CONTABLES: / GANANCIAS ACUMULADAS"
    )

    c_990102_30602_cambios_en_politicas_contables_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30602 | CAMBIOS EN POLITICAS CONTABLES: / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990102_30603_cambios_en_politicas_contables_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30603 | CAMBIOS EN POLITICAS CONTABLES:  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990102_30604_cambios_en_politicas_contables_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30604 | CAMBIOS EN POLITICAS CONTABLES: / RESERVA DE CAPITAL"
    )

    c_990102_30605_cambios_en_politicas_contables_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30605 | CAMBIOS EN POLITICAS CONTABLES: / RESERVA POR DONACIONES"
    )

    c_990102_30606_cambios_en_politicas_contables_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30606 | CAMBIOS EN POLITICAS CONTABLES:  / RESERVA POR VALUACIÓN"
    )

    c_990102_30607_cambios_en_politicas_contables_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30607 | CAMBIOS EN POLITICAS CONTABLES:  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990102_30701_cambios_en_politicas_contables_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30701 | CAMBIOS EN POLITICAS CONTABLES:  / GANANCIA NETA DEL PERIODO"
    )

    c_990102_30702_cambios_en_politicas_contables_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30702 | CAMBIOS EN POLITICAS CONTABLES:  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990103_301_correccion_de_errores_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 301 | CORRECCIÓN DE ERRORES / CAPITAL"
    )

    c_990103_302_correccion_de_errores_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 302 | CORRECCIÓN DE ERRORES  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990103_303_correccion_de_errores_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 303 | CORRECCIÓN DE ERRORES  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990103_30401_correccion_de_errores_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30401 | CORRECCIÓN DE ERRORES / RESERVA LEGAL"
    )

    c_990103_30402_correccion_de_errores_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30402 | CORRECCIÓN DE ERRORES  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990103_30501_correccion_de_errores_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30501 | CORRECCIÓN DE ERRORES / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990103_30502_correccion_de_errores_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30502 | CORRECCIÓN DE ERRORES  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990103_30503_correccion_de_errores_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30503 | CORRECCIÓN DE ERRORES  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990103_30504_correccion_de_errores_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30504 | CORRECCIÓN DE ERRORES  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990103_30601_correccion_de_errores_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30601 | CORRECCIÓN DE ERRORES / GANANCIAS ACUMULADAS"
    )

    c_990103_30602_correccion_de_errores_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30602 | CORRECCIÓN DE ERRORES / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990103_30603_correccion_de_errores_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30603 | CORRECCIÓN DE ERRORES  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990103_30604_correccion_de_errores_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30604 | CORRECCIÓN DE ERRORES / RESERVA DE CAPITAL"
    )

    c_990103_30605_correccion_de_errores_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30605 | CORRECCIÓN DE ERRORES / RESERVA POR DONACIONES"
    )

    c_990103_30606_correccion_de_errores_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30606 | CORRECCIÓN DE ERRORES  / RESERVA POR VALUACIÓN"
    )

    c_990103_30607_correccion_de_errores_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30607 | CORRECCIÓN DE ERRORES  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990103_30701_correccion_de_errores_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30701 | CORRECCIÓN DE ERRORES  / GANANCIA NETA DEL PERIODO"
    )

    c_990103_30702_correccion_de_errores_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30702 | CORRECCIÓN DE ERRORES  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_9902_301_cambios_del_ano_en_el_patrimonio_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 301 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / CAPITAL"
    )

    c_9902_302_cambios_del_ano_en_el_patrimonio_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 302 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_9902_303_cambios_del_ano_en_el_patrimonio_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 303 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_9902_30401_cambios_del_ano_en_el_patrimonio_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30401 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / RESERVA LEGAL"
    )

    c_9902_30402_cambios_del_ano_en_el_patrimonio_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30402 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_9902_30501_cambios_del_ano_en_el_patrimonio_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30501 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_9902_30502_cambios_del_ano_en_el_patrimonio_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30502 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_9902_30503_cambios_del_ano_en_el_patrimonio_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30503 | CAMBIOS DEL AÑO EN EL PATRIMONIO:   / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_9902_30504_cambios_del_ano_en_el_patrimonio_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30504 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_9902_30601_cambios_del_ano_en_el_patrimonio_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30601 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / GANANCIAS ACUMULADAS"
    )

    c_9902_30602_cambios_del_ano_en_el_patrimonio_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30602 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / (-) PÉRDIDAS ACUMULADAS"
    )

    c_9902_30603_cambios_del_ano_en_el_patrimonio_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30603 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_9902_30604_cambios_del_ano_en_el_patrimonio_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30604 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / RESERVA DE CAPITAL"
    )

    c_9902_30605_cambios_del_ano_en_el_patrimonio_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30605 | CAMBIOS DEL AÑO EN EL PATRIMONIO: / RESERVA POR DONACIONES"
    )

    c_9902_30606_cambios_del_ano_en_el_patrimonio_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30606 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / RESERVA POR VALUACIÓN"
    )

    c_9902_30607_cambios_del_ano_en_el_patrimonio_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30607 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_9902_30701_cambios_del_ano_en_el_patrimonio_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30701 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / GANANCIA NETA DEL PERIODO"
    )

    c_9902_30702_cambios_del_ano_en_el_patrimonio_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30702 | CAMBIOS DEL AÑO EN EL PATRIMONIO:  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990201_301_aumento_disminucion_de_capital_social_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 301 | Aumento (disminución) de capital social / CAPITAL"
    )

    c_990201_302_aumento_disminucion_de_capital_social_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 302 | Aumento (disminución) de capital social / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990201_303_aumento_disminucion_de_capital_social_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 303 | Aumento (disminución) de capital social / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990201_30401_aumento_disminucion_de_capital_social_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30401 | Aumento (disminución) de capital social / RESERVA LEGAL"
    )

    c_990201_30402_aumento_disminucion_de_capital_social_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30402 | Aumento (disminución) de capital social  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990201_30501_aumento_disminucion_de_capital_social_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30501 | Aumento (disminución) de capital social / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990201_30502_aumento_disminucion_de_capital_social_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30502 | Aumento (disminución) de capital social  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990201_30503_aumento_disminucion_de_capital_social_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30503 | Aumento (disminución) de capital social  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990201_30504_aumento_disminucion_de_capital_social_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30504 | Aumento (disminución) de capital social  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990201_30601_aumento_disminucion_de_capital_social_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30601 | Aumento (disminución) de capital social / GANANCIAS ACUMULADAS"
    )

    c_990201_30602_aumento_disminucion_de_capital_social_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30602 | Aumento (disminución) de capital social / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990201_30603_aumento_disminucion_de_capital_social_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30603 | Aumento (disminución) de capital social  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990201_30604_aumento_disminucion_de_capital_social_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30604 | Aumento (disminución) de capital social / RESERVA DE CAPITAL"
    )

    c_990201_30605_aumento_disminucion_de_capital_social_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30605 | Aumento (disminución) de capital social / RESERVA POR DONACIONES"
    )

    c_990201_30606_aumento_disminucion_de_capital_social_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30606 | Aumento (disminución) de capital social  / RESERVA POR VALUACIÓN"
    )

    c_990201_30607_aumento_disminucion_de_capital_social_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30607 | Aumento (disminución) de capital social  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990201_30701_aumento_disminucion_de_capital_social_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30701 | Aumento (disminución) de capital social  / GANANCIA NETA DEL PERIODO"
    )

    c_990201_30702_aumento_disminucion_de_capital_social_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30702 | Aumento (disminución) de capital social  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990202_301_aportes_para_futuras_capitalizaciones_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 301 | Aportes para futuras capitalizaciones / CAPITAL"
    )

    c_990202_302_aportes_para_futuras_capitalizaciones_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 302 | Aportes para futuras capitalizaciones  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990202_303_aportes_para_futuras_capitalizaciones_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 303 | Aportes para futuras capitalizaciones  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990202_30401_aportes_para_futuras_capitalizaciones_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30401 | Aportes para futuras capitalizaciones / RESERVA LEGAL"
    )

    c_990202_30402_aportes_para_futuras_capitalizaciones_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30402 | Aportes para futuras capitalizaciones  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990202_30501_aportes_para_futuras_capitalizaciones_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30501 | Aportes para futuras capitalizaciones / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990202_30502_aportes_para_futuras_capitalizaciones_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30502 | Aportes para futuras capitalizaciones  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990202_30503_aportes_para_futuras_capitalizaciones_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30503 | Aportes para futuras capitalizaciones  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990202_30504_aportes_para_futuras_capitalizaciones_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30504 | Aportes para futuras capitalizaciones  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990202_30601_aportes_para_futuras_capitalizaciones_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30601 | Aportes para futuras capitalizaciones / GANANCIAS ACUMULADAS"
    )

    c_990202_30602_aportes_para_futuras_capitalizaciones_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30602 | Aportes para futuras capitalizaciones / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990202_30603_aportes_para_futuras_capitalizaciones_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30603 | Aportes para futuras capitalizaciones  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990202_30604_aportes_para_futuras_capitalizaciones_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30604 | Aportes para futuras capitalizaciones / RESERVA DE CAPITAL"
    )

    c_990202_30605_aportes_para_futuras_capitalizaciones_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30605 | Aportes para futuras capitalizaciones / RESERVA POR DONACIONES"
    )

    c_990202_30606_aportes_para_futuras_capitalizaciones_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30606 | Aportes para futuras capitalizaciones  / RESERVA POR VALUACIÓN"
    )

    c_990202_30607_aportes_para_futuras_capitalizaciones_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30607 | Aportes para futuras capitalizaciones  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990202_30701_aportes_para_futuras_capitalizaciones_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30701 | Aportes para futuras capitalizaciones  / GANANCIA NETA DEL PERIODO"
    )

    c_990202_30702_aportes_para_futuras_capitalizaciones_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30702 | Aportes para futuras capitalizaciones  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990203_301_prima_por_emision_primaria_de_acciones_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 301 | Prima por emisión primaria de acciones / CAPITAL"
    )

    c_990203_302_prima_por_emision_primaria_de_acciones_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 302 | Prima por emisión primaria de acciones  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990203_303_prima_por_emision_primaria_de_acciones_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 303 | Prima por emisión primaria de acciones  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990203_30401_prima_por_emision_primaria_de_acciones_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30401 | Prima por emisión primaria de acciones / RESERVA LEGAL"
    )

    c_990203_30402_prima_por_emision_primaria_de_acciones_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30402 | Prima por emisión primaria de acciones  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990203_30501_prima_por_emision_primaria_de_acciones_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30501 | Prima por emisión primaria de acciones / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990203_30502_prima_por_emision_primaria_de_acciones_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30502 | Prima por emisión primaria de acciones  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990203_30503_prima_por_emision_primaria_de_acciones_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30503 | Prima por emisión primaria de acciones  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990203_30504_prima_por_emision_primaria_de_acciones_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30504 | Prima por emisión primaria de acciones  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990203_30601_prima_por_emision_primaria_de_acciones_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30601 | Prima por emisión primaria de acciones / GANANCIAS ACUMULADAS"
    )

    c_990203_30602_prima_por_emision_primaria_de_acciones_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30602 | Prima por emisión primaria de acciones / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990203_30603_prima_por_emision_primaria_de_acciones_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30603 | Prima por emisión primaria de acciones  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990203_30604_prima_por_emision_primaria_de_acciones_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30604 | Prima por emisión primaria de acciones / RESERVA DE CAPITAL"
    )

    c_990203_30605_prima_por_emision_primaria_de_acciones_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30605 | Prima por emisión primaria de acciones / RESERVA POR DONACIONES"
    )

    c_990203_30606_prima_por_emision_primaria_de_acciones_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30606 | Prima por emisión primaria de acciones  / RESERVA POR VALUACIÓN"
    )

    c_990203_30607_prima_por_emision_primaria_de_acciones_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30607 | Prima por emisión primaria de acciones  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990203_30701_prima_por_emision_primaria_de_acciones_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30701 | Prima por emisión primaria de acciones  / GANANCIA NETA DEL PERIODO"
    )

    c_990203_30702_prima_por_emision_primaria_de_acciones_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30702 | Prima por emisión primaria de acciones  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990204_301_dividendos_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 301 | Dividendos / CAPITAL"
    )

    c_990204_302_dividendos_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 302 | Dividendos  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990204_303_dividendos_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 303 | Dividendos  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990204_30401_dividendos_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30401 | Dividendos / RESERVA LEGAL"
    )

    c_990204_30402_dividendos_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30402 | Dividendos  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990204_30501_dividendos_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30501 | Dividendos / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990204_30502_dividendos_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30502 | Dividendos  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990204_30503_dividendos_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30503 | Dividendos  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990204_30504_dividendos_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30504 | Dividendos  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990204_30601_dividendos_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30601 | Dividendos / GANANCIAS ACUMULADAS"
    )

    c_990204_30602_dividendos_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30602 | Dividendos / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990204_30603_dividendos_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30603 | Dividendos  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990204_30604_dividendos_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30604 | Dividendos / RESERVA DE CAPITAL"
    )

    c_990204_30605_dividendos_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30605 | Dividendos / RESERVA POR DONACIONES"
    )

    c_990204_30606_dividendos_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30606 | Dividendos  / RESERVA POR VALUACIÓN"
    )

    c_990204_30607_dividendos_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30607 | Dividendos  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990204_30701_dividendos_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30701 | Dividendos  / GANANCIA NETA DEL PERIODO"
    )

    c_990204_30702_dividendos_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30702 | Dividendos  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990205_301_transferencia_de_resultados_a_otras_cuentas_patrimoniales_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 301 | Transferencia de Resultados a otras cuentas patrimoniales / CAPITAL"
    )

    c_990205_302_transferencia_de_resultados_a_otras_cuentas_patrimoniales_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 302 | Transferencia de Resultados a otras cuentas patrimoniales  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990205_303_transferencia_de_resultados_a_otras_cuentas_patrimoniales_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 303 | Transferencia de Resultados a otras cuentas patrimoniales  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990205_30401_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30401 | Transferencia de Resultados a otras cuentas patrimoniales / RESERVA LEGAL"
    )

    c_990205_30402_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30402 | Transferencia de Resultados a otras cuentas patrimoniales  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990205_30501_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30501 | Transferencia de Resultados a otras cuentas patrimoniales / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990205_30502_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30502 | Transferencia de Resultados a otras cuentas patrimoniales  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990205_30503_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30503 | Transferencia de Resultados a otras cuentas patrimoniales  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990205_30504_transferencia_de_resultados_a_otras_cuentas_patrimoniales_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30504 | Transferencia de Resultados a otras cuentas patrimoniales  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990205_30601_transferencia_de_resultados_a_otras_cuentas_patrimoniales_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30601 | Transferencia de Resultados a otras cuentas patrimoniales / GANANCIAS ACUMULADAS"
    )

    c_990205_30602_transferencia_de_resultados_a_otras_cuentas_patrimoniales_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30602 | Transferencia de Resultados a otras cuentas patrimoniales / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990205_30603_transferencia_de_resultados_a_otras_cuentas_patrimoniales_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30603 | Transferencia de Resultados a otras cuentas patrimoniales  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990205_30604_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30604 | Transferencia de Resultados a otras cuentas patrimoniales / RESERVA DE CAPITAL"
    )

    c_990205_30605_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30605 | Transferencia de Resultados a otras cuentas patrimoniales / RESERVA POR DONACIONES"
    )

    c_990205_30606_transferencia_de_resultados_a_otras_cuentas_patrimoniales_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30606 | Transferencia de Resultados a otras cuentas patrimoniales  / RESERVA POR VALUACIÓN"
    )

    c_990205_30607_transferencia_de_resultados_a_otras_cuentas_patrimoniales_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30607 | Transferencia de Resultados a otras cuentas patrimoniales  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990205_30701_transferencia_de_resultados_a_otras_cuentas_patrimoniales_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30701 | Transferencia de Resultados a otras cuentas patrimoniales  / GANANCIA NETA DEL PERIODO"
    )

    c_990205_30702_transferencia_de_resultados_a_otras_cuentas_patrimoniales_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30702 | Transferencia de Resultados a otras cuentas patrimoniales  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990206_301_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 301 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / CAPITAL"
    )

    c_990206_302_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 302 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990206_303_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 303 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990206_30401_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30401 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / RESERVA LEGAL"
    )

    c_990206_30402_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30402 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990206_30501_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30501 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990206_30502_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30502 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990206_30503_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30503 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990206_30504_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30504 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990206_30601_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30601 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / GANANCIAS ACUMULADAS"
    )

    c_990206_30602_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30602 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990206_30603_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30603 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990206_30604_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30604 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / RESERVA DE CAPITAL"
    )

    c_990206_30605_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30605 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta / RESERVA POR DONACIONES"
    )

    c_990206_30606_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30606 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / RESERVA POR VALUACIÓN"
    )

    c_990206_30607_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30607 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990206_30701_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30701 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / GANANCIA NETA DEL PERIODO"
    )

    c_990206_30702_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30702 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990207_301_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 301 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / CAPITAL"
    )

    c_990207_302_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 302 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990207_303_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 303 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990207_30401_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30401 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / RESERVA LEGAL"
    )

    c_990207_30402_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30402 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990207_30501_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30501 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990207_30502_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30502 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990207_30503_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30503 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990207_30504_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30504 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990207_30601_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30601 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / GANANCIAS ACUMULADAS"
    )

    c_990207_30602_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30602 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990207_30603_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30603 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990207_30604_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30604 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / RESERVA DE CAPITAL"
    )

    c_990207_30605_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30605 | Realización de la Reserva por Valuación de Propiedades, planta y equipo / RESERVA POR DONACIONES"
    )

    c_990207_30606_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30606 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / RESERVA POR VALUACIÓN"
    )

    c_990207_30607_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30607 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990207_30701_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30701 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / GANANCIA NETA DEL PERIODO"
    )

    c_990207_30702_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30702 | Realización de la Reserva por Valuación de Propiedades, planta y equipo  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990208_301_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 301 | Realización de la Reserva por Valuación de Activos Intangibles / CAPITAL"
    )

    c_990208_302_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 302 | Realización de la Reserva por Valuación de Activos Intangibles  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990208_303_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 303 | Realización de la Reserva por Valuación de Activos Intangibles  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990208_30401_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30401 | Realización de la Reserva por Valuación de Activos Intangibles / RESERVA LEGAL"
    )

    c_990208_30402_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30402 | Realización de la Reserva por Valuación de Activos Intangibles  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990208_30501_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30501 | Realización de la Reserva por Valuación de Activos Intangibles / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990208_30502_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30502 | Realización de la Reserva por Valuación de Activos Intangibles  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990208_30503_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30503 | Realización de la Reserva por Valuación de Activos Intangibles  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990208_30504_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30504 | Realización de la Reserva por Valuación de Activos Intangibles  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990208_30601_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30601 | Realización de la Reserva por Valuación de Activos Intangibles / GANANCIAS ACUMULADAS"
    )

    c_990208_30602_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30602 | Realización de la Reserva por Valuación de Activos Intangibles / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990208_30603_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30603 | Realización de la Reserva por Valuación de Activos Intangibles  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990208_30604_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30604 | Realización de la Reserva por Valuación de Activos Intangibles / RESERVA DE CAPITAL"
    )

    c_990208_30605_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30605 | Realización de la Reserva por Valuación de Activos Intangibles / RESERVA POR DONACIONES"
    )

    c_990208_30606_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30606 | Realización de la Reserva por Valuación de Activos Intangibles  / RESERVA POR VALUACIÓN"
    )

    c_990208_30607_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30607 | Realización de la Reserva por Valuación de Activos Intangibles  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990208_30701_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30701 | Realización de la Reserva por Valuación de Activos Intangibles  / GANANCIA NETA DEL PERIODO"
    )

    c_990208_30702_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30702 | Realización de la Reserva por Valuación de Activos Intangibles  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990209_301_otros_cambios_detallar_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 301 | Otros cambios (detallar) / CAPITAL"
    )

    c_990209_302_otros_cambios_detallar_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 302 | Otros cambios (detallar)  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990209_303_otros_cambios_detallar_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 303 | Otros cambios (detallar)  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990209_30401_otros_cambios_detallar_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30401 | Otros cambios (detallar) / RESERVA LEGAL"
    )

    c_990209_30402_otros_cambios_detallar_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30402 | Otros cambios (detallar)  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990209_30501_otros_cambios_detallar_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30501 | Otros cambios (detallar) / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990209_30502_otros_cambios_detallar_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30502 | Otros cambios (detallar)  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990209_30503_otros_cambios_detallar_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30503 | Otros cambios (detallar)  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990209_30504_otros_cambios_detallar_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30504 | Otros cambios (detallar)  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990209_30601_otros_cambios_detallar_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30601 | Otros cambios (detallar) / GANANCIAS ACUMULADAS"
    )

    c_990209_30602_otros_cambios_detallar_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30602 | Otros cambios (detallar) / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990209_30603_otros_cambios_detallar_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30603 | Otros cambios (detallar)  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990209_30604_otros_cambios_detallar_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30604 | Otros cambios (detallar) / RESERVA DE CAPITAL"
    )

    c_990209_30605_otros_cambios_detallar_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30605 | Otros cambios (detallar) / RESERVA POR DONACIONES"
    )

    c_990209_30606_otros_cambios_detallar_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30606 | Otros cambios (detallar)  / RESERVA POR VALUACIÓN"
    )

    c_990209_30607_otros_cambios_detallar_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30607 | Otros cambios (detallar)  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990209_30701_otros_cambios_detallar_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30701 | Otros cambios (detallar)  / GANANCIA NETA DEL PERIODO"
    )

    c_990209_30702_otros_cambios_detallar_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30702 | Otros cambios (detallar)  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_990210_301_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 301 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / CAPITAL"
    )

    c_990210_302_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_aportes_de_socios_o_accionistas_para_futura_capitalizacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 302 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / APORTES DE SOCIOS O ACCIONISTAS PARA FUTURA CAPITALIZACIÓN"
    )

    c_990210_303_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 303 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / PRIMA POR EMISIÓN PRIMARIA DE ACCIONES"
    )

    c_990210_30401_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_legal = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30401 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / RESERVA LEGAL"
    )

    c_990210_30402_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reservas_facultativa_y_estatutaria = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30402 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / RESERVAS FACULTATIVA Y ESTATUTARIA"
    )

    c_990210_30501_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_de_activos_financieros_a_valor_razonable_con_cambios_en_otro_resultado = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30501 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / SUPERAVIT DE ACTIVOS FINANCIEROS A VALOR RAZONABLE CON CAMBIOS EN OTRO RESULTADO"
    )

    c_990210_30502_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_por_revaluacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30502 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / SUPERAVIT POR REVALUACIÓN DE PROPIEDADES, PLANTA Y EQUIPO"
    )

    c_990210_30503_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_por_revaluacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30503 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / SUPERAVIT POR REVALUACION DE ACTIVOS INTANGIBLES"
    )

    c_990210_30504_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_otros_superavit_por_revaluacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30504 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / OTROS SUPERAVIT POR REVALUACION"
    )

    c_990210_30601_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_ganancias_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30601 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / GANANCIAS ACUMULADAS"
    )

    c_990210_30602_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_perdidas_acumuladas = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30602 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / (-) PÉRDIDAS ACUMULADAS"
    )

    c_990210_30603_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_resultados_acumulados_provenientes_de_la_adopcion_por_primera_vez_de_las_niif = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30603 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / RESULTADOS ACUMULADOS PROVENIENTES DE LA ADOPCION POR PRIMERA VEZ DE LAS NIIF"
    )

    c_990210_30604_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_de_capital = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30604 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / RESERVA DE CAPITAL"
    )

    c_990210_30605_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_por_donaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30605 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio) / RESERVA POR DONACIONES"
    )

    c_990210_30606_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_reserva_por_valuacion = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30606 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / RESERVA POR VALUACIÓN"
    )

    c_990210_30607_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_superavit_por_revaluacion_de_inversiones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30607 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / SUPERÁVIT POR REVALUACIÓN DE INVERSIONES"
    )

    c_990210_30701_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_ganancia_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30701 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / GANANCIA NETA DEL PERIODO"
    )

    c_990210_30702_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio_perdida_neta_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30702 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)  / (-) PÉRDIDA NETA DEL PERIODO"
    )

    c_99_30_saldo_al_final_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 30 | SALDO AL FINAL DEL PERÍODO"
    )

    c_99_31_saldo_al_final_del_periodo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 99 | Subcódigo 31 | SALDO AL FINAL DEL PERÍODO"
    )

    c_9901_30_saldo_reexpresado_del_periodo_inmediato_anterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 30 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR"
    )

    c_9901_31_saldo_reexpresado_del_periodo_inmediato_anterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9901 | Subcódigo 31 | SALDO REEXPRESADO DEL PERIODO INMEDIATO ANTERIOR"
    )

    c_9902_30_cambios_del_ano_en_el_patrimonio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 30 | CAMBIOS DEL AÑO EN EL PATRIMONIO:"
    )

    c_9902_31_cambios_del_ano_en_el_patrimonio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 9902 | Subcódigo 31 | CAMBIOS DEL AÑO EN EL PATRIMONIO:"
    )

    c_990101_30_saldo_del_periodo_inmediato_anterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 30 | SALDO DEL PERÍODO INMEDIATO ANTERIOR"
    )

    c_990101_31_saldo_del_periodo_inmediato_anterior = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990101 | Subcódigo 31 | SALDO DEL PERÍODO INMEDIATO ANTERIOR"
    )

    c_990102_30_cambios_en_politicas_contables = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 30 | CAMBIOS EN POLITICAS CONTABLES:"
    )

    c_990102_31_cambios_en_politicas_contables = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990102 | Subcódigo 31 | CAMBIOS EN POLITICAS CONTABLES:"
    )

    c_990103_30_correccion_de_errores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 30 | CORRECCION DE ERRORES"
    )

    c_990103_31_correccion_de_errores = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990103 | Subcódigo 31 | CORRECCION DE ERRORES"
    )

    c_990201_30_aumento_disminucion_de_capital_social = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 30 | Aumento (disminución) de capital social"
    )

    c_990201_31_aumento_disminucion_de_capital_social = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990201 | Subcódigo 31 | Aumento (disminución) de capital social"
    )

    c_990202_30_aportes_para_futuras_capitalizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 30 | Aportes para futuras capitalizaciones"
    )

    c_990202_31_aportes_para_futuras_capitalizaciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990202 | Subcódigo 31 | Aportes para futuras capitalizaciones"
    )

    c_990203_30_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 30 | Prima por emisión primaria de acciones"
    )

    c_990203_31_prima_por_emision_primaria_de_acciones = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990203 | Subcódigo 31 | Prima por emisión primaria de acciones"
    )

    c_990204_30_dividendos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 30 | Dividendos"
    )

    c_990204_31_dividendos = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990204 | Subcódigo 31 | Dividendos"
    )

    c_990205_30_transferencia_de_resultados_a_otras_cuentas_patrimoniales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 30 | Transferencia de Resultados a otras cuentas patrimoniales"
    )

    c_990205_31_transferencia_de_resultados_a_otras_cuentas_patrimoniales = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990205 | Subcódigo 31 | Transferencia de Resultados a otras cuentas patrimoniales"
    )

    c_990206_30_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 30 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta"
    )

    c_990206_31_realizacion_de_la_reserva_por_valuacion_de_activos_financieros_disponibles_para_la_venta = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990206 | Subcódigo 31 | Realización de la Reserva por Valuación de Activos Financieros Disponibles para la venta"
    )

    c_990207_30_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 30 | Realización de la Reserva por Valuación de Propiedades, planta y equipo"
    )

    c_990207_31_realizacion_de_la_reserva_por_valuacion_de_propiedades_planta_y_equipo = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990207 | Subcódigo 31 | Realización de la Reserva por Valuación de Propiedades, planta y equipo"
    )

    c_990208_30_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 30 | Realización de la Reserva por Valuación de Activos Intangibles"
    )

    c_990208_31_realizacion_de_la_reserva_por_valuacion_de_activos_intangibles = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990208 | Subcódigo 31 | Realización de la Reserva por Valuación de Activos Intangibles"
    )

    c_990209_30_otros_cambios_detallar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 30 | Otros cambios (detallar)"
    )

    c_990209_31_otros_cambios_detallar = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990209 | Subcódigo 31 | Otros cambios (detallar)"
    )

    c_990210_30_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 30 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)"
    )

    c_990210_31_resultado_integral_total_del_ano_ganancia_o_perdida_del_ejercicio = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Código 990210 | Subcódigo 31 | Resultado Integral Total del Año (Ganancia o pérdida del ejercicio)"
    )


    # =========================
    # METADATA
    # =========================
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    class Meta:
        unique_together = ('ruc', 'fiscal_year')
        verbose_name = "Balance: SuperIntendencia de Compañías, Valores y Seguros"
        verbose_name_plural = "Balances: SuperIntendencia de Compañías, Valores y Seguros"

    def __str__(self):
        return f"{self.company_name} - {self.fiscal_year}"

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
