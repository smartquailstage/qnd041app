from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
from django.conf import settings
import uuid
import hashlib
from django.utils import timezone
from django.conf import settings



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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SCVS_Estatutos",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='scvs_estatutos_demo')
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

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SCVS_ActasAsamblea",
        blank=True,
        null=True,
    )

    # =========================
    # RELACIÓN REGULATORIA
    # =========================
    regulacion = models.ForeignKey(
        'Regulacion',
        on_delete=models.CASCADE,
        related_name='scvs_actas_demo',
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


    # =====================================================
    # METADATA
    # =====================================================
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True,null=True, blank=True)

    def get_document_name(self):
        return f"ActaJuntaSCVS_{self.fecha_asamblea.strftime('%Y%m%d') if self.fecha_asamblea else 'SIN_FECHA'}"

    class Meta:
        verbose_name = "Acta de Junta General SCVS"
        verbose_name_plural = "Actas de Junta General SCVS"

    def __str__(self):
        return self.get_document_name()




class SCVSFinancialReport(models.Model):

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SCVSFinancialReport",
        blank=True,
        null=True,
    )
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
        max_length=10,
        choices=[
            ('SA', 'Sociedad Anónima'),
            ('LTDA', 'Compañía Limitada'),
            ('SAS', 'SAS'),
        ],
        null=True, blank=True,
        help_text="Tipo legal de la sociedad según registro mercantil."
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
    cash_and_equivalents = models.DecimalField(
        "Efectivo y equivalentes", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Suma del efectivo en caja y bancos, más inversiones a corto plazo fácilmente convertibles en efectivo."
    )
    short_term_investments = models.DecimalField(
        "Inversiones a corto plazo", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Inversiones temporales y valores negociables con vencimiento menor a un año."
    )
    accounts_receivable = models.DecimalField(
        "Cuentas por cobrar", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto total que clientes deben a la compañía por ventas a crédito."
    )
    inventories = models.DecimalField(
        "Inventarios", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Valor de inventarios de bienes, materias primas y productos terminados listos para la venta."
    )
    other_current_assets = models.DecimalField(
        "Otros activos corrientes", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Otros activos que se espera convertir en efectivo o usar dentro del año fiscal."
    )
    property_plant_equipment = models.DecimalField(
        "Propiedad, planta y equipo", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Valor de terrenos, edificios, maquinaria y equipo utilizados en las operaciones de la empresa."
    )
    accumulated_depreciation = models.DecimalField(
        "Depreciación acumulada", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Suma de la depreciación aplicada a los activos fijos desde su adquisición."
    )
    intangible_assets = models.DecimalField(
        "Activos intangibles", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Activos no físicos con valor económico, como patentes, marcas o software."
    )
    other_non_current_assets = models.DecimalField(
        "Otros activos no corrientes", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Activos que no se espera convertir en efectivo en menos de un año, distintos a los ya mencionados."
    )

    accounts_payable = models.DecimalField(
        "Cuentas por pagar", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Deudas con proveedores por compras de bienes o servicios a crédito."
    )
    short_term_loans = models.DecimalField(
        "Préstamos a corto plazo", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Obligaciones financieras con vencimiento menor a un año."
    )
    tax_payables = models.DecimalField(
        "Obligaciones tributarias", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Impuestos por pagar, incluyendo IVA, retenciones y otros tributos pendientes."
    )
    labor_obligations = models.DecimalField(
        "Obligaciones laborales", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Deudas con empleados, como salarios, bonos, prestaciones sociales o vacaciones pendientes."
    )
    other_current_liabilities = models.DecimalField(
        "Otros pasivos corrientes", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Otras obligaciones a corto plazo que la empresa debe cumplir dentro del año fiscal."
    )

    long_term_loans = models.DecimalField(
        "Préstamos a largo plazo", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Obligaciones financieras con vencimiento mayor a un año."
    )
    provisions = models.DecimalField(
        "Provisiones", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Reservas de dinero para cubrir pasivos futuros o contingencias previstas."
    )
    other_non_current_liabilities = models.DecimalField(
        "Otros pasivos no corrientes", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Obligaciones financieras y no financieras con vencimiento mayor a un año distintas a las ya mencionadas."
    )

    share_capital = models.DecimalField(
        "Capital social", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto de aportes de los socios o accionistas registrado legalmente como capital social."
    )
    legal_reserve = models.DecimalField(
        "Reserva legal", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Porción de las utilidades retenidas que la ley exige mantener como reserva legal."
    )
    retained_earnings = models.DecimalField(
        "Resultados acumulados", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Utilidades o pérdidas acumuladas de ejercicios anteriores que se mantienen en la empresa."
    )
    net_income = models.DecimalField(
        "Resultado neto", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Resultado neto del periodo fiscal: ingresos menos gastos e impuestos."
    )

    # =========================
    # ESTADO DE RESULTADOS
    # =========================
    operating_revenue = models.DecimalField(
        "Ingresos operativos", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Ingresos generados por la actividad principal de la compañía (ventas de productos o servicios)."
    )
    cost_of_sales = models.DecimalField(
        "Costo de ventas", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Costos directamente relacionados con la producción o adquisición de bienes vendidos."
    )
    gross_profit = models.DecimalField(
        "Utilidad bruta", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Ingresos operativos menos el costo de ventas."
    )

    administrative_expenses = models.DecimalField(
        "Gastos administrativos", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Gastos relacionados con la administración general de la empresa (sueldos de gerencia, servicios, etc.)"
    )
    selling_expenses = models.DecimalField(
        "Gastos de ventas", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Gastos relacionados con la comercialización y distribución de productos o servicios."
    )
    financial_expenses = models.DecimalField(
        "Gastos financieros", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Intereses pagados y otros costos financieros relacionados con deudas."
    )

    other_income = models.DecimalField(
        "Otros ingresos", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Ingresos no operativos, como venta de activos, dividendos o ganancias extraordinarias."
    )
    other_expenses = models.DecimalField(
        "Otros gastos", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Gastos no operativos, como pérdidas por venta de activos o gastos extraordinarios."
    )

    income_tax = models.DecimalField(
        "Impuesto a la renta", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto del impuesto a la renta correspondiente al periodo fiscal."
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
    cashflow_operating = models.DecimalField(
        "Flujos de operación", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Entrada y salida de efectivo por operaciones normales de la compañía."
    )
    cashflow_investing = models.DecimalField(
        "Flujos de inversión", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Entrada y salida de efectivo relacionadas con la compra o venta de activos a largo plazo."
    )
    cashflow_financing = models.DecimalField(
        "Flujos de financiamiento", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Entrada y salida de efectivo relacionadas con préstamos, emisión de acciones o dividendos."
    )
    net_cash_flow = models.DecimalField(
        "Flujo neto de efectivo", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Variación neta del efectivo durante el periodo: flujo de operación + inversión + financiamiento."
    )

    # =========================
    # ANEXOS SCVS
    # =========================
    accounts_receivable_related = models.DecimalField(
        "Cuentas por cobrar relacionadas", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Cuentas por cobrar a empresas relacionadas o vinculadas a la compañía."
    )
    accounts_payable_related = models.DecimalField(
        "Cuentas por pagar relacionadas", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Cuentas por pagar a empresas relacionadas o vinculadas a la compañía."
    )
    fixed_assets_cost = models.DecimalField(
        "Costo de activos fijos", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Valor de adquisición de todos los activos fijos antes de depreciación."
    )
    fixed_assets_depreciation = models.DecimalField(
        "Depreciación de activos fijos", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Depreciación acumulada de los activos fijos hasta la fecha del reporte."
    )
    financial_obligations_total = models.DecimalField(
        "Obligaciones financieras totales", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Total de todas las deudas y préstamos, tanto a corto como a largo plazo."
    )
    employee_profit_sharing = models.DecimalField(
        "Participación de empleados", max_digits=18, decimal_places=2, null=True, blank=True,
        help_text="Monto de utilidades destinado a la participación de los trabajadores según ley."
    )

    # =========================
    # METADATA
    # =========================
    created_at = models.DateTimeField("Fecha de creación", auto_now_add=True)
    updated_at = models.DateTimeField("Última actualización", auto_now=True)

    class Meta:
        unique_together = ('ruc', 'fiscal_year')
        app_label = "smartbusinesslaw_demo"
        verbose_name = "Balance: SuperIntendencia de Compañías, Valores y Seguros"
        verbose_name_plural = "Balances: SuperIntendencia de Compañías, Valores y Seguros"

    def __str__(self):
        return f"{self.company_name} - {self.fiscal_year}"

# ===========================
# SPDP - Superintendencia de Protección de Datos Personales
# ===========================
class SPDP_Consentimiento(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SPDP_Consentimiento",
        blank=True,
        null=True,
    )

    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_consentimientos_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SPDP_RAT",
        blank=True,
        null=True,
    )

    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_rat_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="SPDP_DPIA",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_dpia_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="SPDP_ARCO",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_arco_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="SPDP_Incidente",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_incidentes_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="SPDP_PoliticaInterna",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='spdp_politicas_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SPDP_ActaDelegado",
        blank=True,
        null=True,
    )

    regulacion = models.ForeignKey(
        Regulacion,
        on_delete=models.CASCADE,
        related_name='spdp_delegado_demo'
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
    related_name='rat_tratamientos_demo',
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
    related_name='rat_titulares_demo'
   
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

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SRI_RUC",
        blank=True,
        null=True,
    )
    
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='sri_ruc_demo')
    ruc = models.CharField(max_length=13)
    fecha_emision = models.DateField()
    archivo = models.FileField(upload_to='sri/ruc/', blank=True, null=True)

    def get_document_name(self):
        return f"RUC_{self.ruc}_{self.fecha_emision.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "RUC SRI"
        verbose_name_plural = "RUC SRI"



class SRI_Retenciones(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SRI_Retenciones",
        blank=True,
        null=True,
    )
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

class SRI_AnexosTributarios(models.Model):
    """
    MODELO ÚNICO DE ANEXOS TRIBUTARIOS SRI – ECUADOR
    Incluye: ATS, RDEP, Dividendos, Partes Relacionadas, Conciliación Tributaria
    y REBEFICS (Beneficiarios Finales y Composición Societaria).
    Cada campo cuenta con verbose_name y help_text para claridad.
    """
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SRI_AnexosTributarios",
        blank=True,
        null=True,
    )
    # ==================================================
    # I. IDENTIFICACIÓN DEL CONTRIBUYENTE
    # ==================================================
    ruc = models.CharField(
        max_length=13,
        verbose_name="RUC",
        help_text="Registro Único de Contribuyentes de la sociedad, 13 dígitos."
    )
    cantidad_empleados = models.IntegerField(default=0)  # Make sure this exists!
    razon_social = models.CharField(
        max_length=255,
        verbose_name="Razón social",
        help_text="Nombre legal completo de la sociedad o contribuyente."
    )
    ejercicio_fiscal = models.PositiveIntegerField(
        verbose_name="Ejercicio fiscal",
        help_text="Año fiscal al que corresponde la información."
    )
    mes = models.PositiveIntegerField(
        choices=[(i, f"{i:02d}") for i in range(1, 13)],
        verbose_name="Mes",
        help_text="Mes correspondiente a los anexos (01=Enero, 12=Diciembre)."
    )
    obligado_contabilidad = models.BooleanField(
        default=True,
        verbose_name="Obligado a llevar contabilidad",
        help_text="Indica si la sociedad está obligada a llevar contabilidad completa."
    )

    # ==================================================
    # II. ATS – COMPRAS
    # ==================================================
    compras_tipo_comprobante = models.CharField(max_length=2, null=True, blank=True)
    compras_tipo_id_proveedor = models.CharField(max_length=2, null=True, blank=True)
    compras_id_proveedor = models.CharField(max_length=13, null=True, blank=True)
    compras_razon_social_proveedor = models.CharField(max_length=255, null=True, blank=True)
    compras_fecha_emision = models.DateField(null=True, blank=True)
    compras_establecimiento = models.CharField(max_length=3, null=True, blank=True)
    compras_punto_emision = models.CharField(max_length=3, null=True, blank=True)
    compras_secuencial = models.CharField(max_length=9, null=True, blank=True)
    compras_autorizacion = models.CharField(max_length=49, null=True, blank=True)
    compras_base_no_objeto_iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    compras_base_iva_0 = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    compras_base_iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    compras_monto_iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    compras_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    # ==================================================
    # III. ATS – RETENCIONES
    # ==================================================
    retencion_ir_codigo = models.CharField(max_length=3, null=True, blank=True)
    retencion_ir_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    retencion_ir_valor = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    retencion_iva_codigo = models.CharField(max_length=3, null=True, blank=True)
    retencion_iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    retencion_iva_valor = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    # ==================================================
    # IV. ATS – VENTAS
    # ==================================================
    ventas_tipo_id_cliente = models.CharField(max_length=2, null=True, blank=True)
    ventas_id_cliente = models.CharField(max_length=13, null=True, blank=True)
    ventas_razon_social_cliente = models.CharField(max_length=255, null=True, blank=True)
    ventas_base_iva_0 = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ventas_base_iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ventas_monto_iva = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    ventas_total = models.DecimalField(max_digits=18, decimal_places=2, default=0)

    # ==================================================
    # V. RDEP – RELACIÓN DE DEPENDENCIA
    # ==================================================
    tiene_empleados = models.BooleanField(default=False)
    empleado_tipo_id = models.CharField(max_length=2, null=True, blank=True)
    empleado_identificacion = models.CharField(max_length=13, null=True, blank=True)
    empleado_nombres = models.CharField(max_length=255, null=True, blank=True)
    empleado_cargo = models.CharField(max_length=255, null=True, blank=True)
    empleado_sueldo_anual = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    empleado_aporte_iess = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    empleado_ir_retenido = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    # ==================================================
    # VI. DIVIDENDOS
    # ==================================================
    distribuyo_dividendos = models.BooleanField(default=False)
    socio_tipo_id = models.CharField(max_length=2, null=True, blank=True)
    socio_identificacion = models.CharField(max_length=13, null=True, blank=True)
    socio_nombre = models.CharField(max_length=255, null=True, blank=True)
    socio_porcentaje_participacion = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dividendo_pagado = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    impuesto_dividendo = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    # ==================================================
    # VII. PARTES RELACIONADAS
    # ==================================================
    tiene_partes_relacionadas = models.BooleanField(default=False)
    parte_relacionada_identificacion = models.CharField(max_length=13, null=True, blank=True)
    parte_relacionada_nombre = models.CharField(max_length=255, null=True, blank=True)
    monto_operacion_parte_relacionada = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    tipo_operacion = models.CharField(max_length=100, null=True, blank=True)

    # ==================================================
    # VIII. CONCILIACIÓN TRIBUTARIA
    # ==================================================
    utilidad_contable = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    gastos_no_deducibles = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    ingresos_exentos = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    base_imponible = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    impuesto_renta_causado = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)

    # ==================================================
    # IX. FIRMAS Y RESPONSABILIDAD
    # ==================================================
    representante_legal = models.CharField(max_length=255)
    contador = models.CharField(max_length=255)
    fecha_certificacion = models.DateField()

    # ==================================================
    # X. REBEFICS – BENEFICIARIOS FINALES Y SOCIOS
    # ==================================================
    beneficiarios_finales = models.CharField(max_length=255,
        verbose_name="Beneficiarios Finales", null=True, blank=True,
        help_text="Lista de beneficiarios finales con todos sus datos: nombre, ID, nacionalidad, fecha de nacimiento, porcentaje y control indirecto."
    )

    socios = models.CharField(max_length=255,
        verbose_name="Socios/Accionistas",null=True, blank=True,
        help_text="Lista de socios o accionistas con sus datos: nombre, ID, porcentaje de participación y tipo de participación."
    )

    # ==================================================
    # XI. METADATA
    # ==================================================
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="MT_Contratos",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='mt_contratos_demo')
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

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="MT_Nominas",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='mt_nominas_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="MT_Planillas",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='mt_planillas_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="IESS_Afiliaciones",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='iess_afiliaciones_demo')
    empleado = models.CharField(max_length=255)
    fecha_afiliacion = models.DateField()
    archivo = models.FileField(upload_to='iess/afiliaciones/', blank=True, null=True)

    def get_document_name(self):
        return f"Afiliacion_{self.empleado}_{self.fecha_afiliacion.strftime('%Y%m%d')}"

    class Meta:
        verbose_name = "Afiliación IESS"
        verbose_name_plural = "Afiliaciones IESS"

class IESS_Aportes(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="IESS_Aportes",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='iess_aportes_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Usuario Propietario",
        related_name="IESS_HistorialAportes",
        blank=True,
        null=True,
    )
    regulacion = models.ForeignKey(Regulacion, on_delete=models.CASCADE, related_name='iess_historial_demo')
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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="SRI_DeclaracionImpuestos",
        blank=True,
        null=True,
    )

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
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT, # Evita borrar transacciones si se elimina el usuario (       Gobernanza)
        verbose_name="Usuario Propietario",
        related_name="ContratoLaboral",
        blank=True,
        null=True,
    )
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
        verbose_name="Nombres completos del trabajador",
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





    class Meta:
        verbose_name = "Contrato Laboral"
        verbose_name_plural = "Contratos Laborales"
        ordering = ["-fecha_inicio"]

    def __str__(self):
        return f"{self.trabajador_nombres} – {self.cargo} ({self.tipo_contrato})"

    def save(self, *args, **kwargs):
        if not self.hash_contrato:
            raw = f"{self.empleador_ruc}|{self.trabajador_identificacion}|{self.fecha_inicio}|{uuid.uuid4()}|{now().isoformat()}"
            self.hash_contrato = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        super().save(*args, **kwargs)
