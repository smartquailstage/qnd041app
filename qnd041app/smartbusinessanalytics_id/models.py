from django.db import models
from djmoney.models.fields import MoneyField
from decimal import Decimal
from django.utils.timezone import now
from django.db.models import Sum
from djmoney.money import Money
from decimal import Decimal
import uuid
import hashlib


class MovimientoFinanciero(models.Model):
    """
    Modelo financiero unificado para Ingresos y Egresos
    """

    # ======================================================
    # IDENTIFICACIÓN
    # ======================================================
    hash_registro = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        null=True,
        blank=True,
        help_text="Hash único del movimiento financiero, generado automáticamente para trazabilidad."
    )

    codigo_referencia = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Código de referencia del documento (factura, recibo, comprobante, etc.)."
    )

    fecha_devengo = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha en la que el movimiento se reconoce contablemente."
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        help_text="Fecha y hora en que el movimiento fue registrado en el sistema."
    )

    es_ingreso = models.BooleanField(
        default=True,
        help_text="Indica si el movimiento corresponde a un ingreso (True) o a un egreso (False)."
    )

    es_egreso = models.BooleanField(
        default=False,
        help_text="Indica si el movimiento corresponde a un ingreso (False) o a un egreso (True)."
    )

    # ======================================================
    # CLASIFICACIÓN CONTABLE
    # ======================================================
    CATEGORIA_CHOICES = [
        ("gastos_fijos", "Gastos fijos (servicios)"),
        ("gastos_operativos", "Gastos operativos"),
        ("gastos_publicitarios", "Gastos publicitarios"),
        ("gastos_legales", "Gastos legales"),
        ("gastos_nomina", "Gastos de nómina"),
        ("gastos_tributarios", "Gastos tributarios"),
        ("pago_deuda", "Pago de Deuda"),
       
    ]

    CATEGORIA_INGRESOS_CHOICES = [
        ("ventas", "Ventas"),
        ("deducciones", "Deducción Tributaria"),
        ("inversion", "Inversión"),
        ("acciones_legales", "Acción Legal"),
    ]

    categoria = models.CharField(
        max_length=30,
        choices=CATEGORIA_CHOICES,
        null=True,
        blank=True,
        help_text="Clasificación contable del movimiento financiero."
    )

    categoria_ingresos = models.CharField(
        max_length=30,
        choices=CATEGORIA_INGRESOS_CHOICES,
        null=True,
        blank=True,
        help_text="Clasificación contable del movimiento financiero."
    )

    descripcion = models.TextField(
        null=True,
        blank=True,
        help_text="Descripción detallada del movimiento financiero."
    )

    # ======================================================
    # CONTRAPARTE
    # ======================================================
    contraparte_nombre = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        help_text="Nombre del cliente, proveedor o entidad relacionada con el movimiento."
    )

    contraparte_identificacion_fiscal = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Identificación fiscal de la contraparte (RFC, NIT, CIF, etc.)."
    )

    # ======================================================
    # MONTOS BASE
    # ======================================================
    monto_bruto = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text="Monto bruto del movimiento antes de descuentos e impuestos."
    )

    descuento = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text="Descuento aplicado al monto bruto."
    )

    tasa_iva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        null=True,
        blank=True,
        help_text="Tasa de IVA aplicada al movimiento. Ejemplo: 0.16 para 16%."
    )

    # ======================================================
    # RESULTADOS TRIBUTARIOS (AUTO)
    # ======================================================
    base_imponible = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        editable=False,
        help_text="Monto sobre el cual se calcula el IVA."
    )

    iva = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        editable=False,
        help_text="IVA calculado automáticamente."
    )

    monto_neto = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        editable=False,
        help_text="Monto total final del movimiento con impuestos incluidos."
    )

    # ======================================================
    # COSTOS Y UTILIDADES
    # ======================================================
    costo_directo = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text="Costo directo asociado al movimiento."
    )

    gastos_indirectos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        help_text="Gastos indirectos asociados al movimiento."
    )

    utilidad_bruta = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        editable=False,
        help_text="Resultado de restar el costo directo a la base imponible."
    )

    utilidad_neta = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency="USD",
        null=True,
        blank=True,
        editable=False,
        help_text="Resultado final después de descontar gastos indirectos."
    )

    # ======================================================
    # ESTADO DEL MOVIMIENTO
    # ======================================================
    confirmado = models.BooleanField(
        default=False,
        help_text="Indica si el movimiento ya fue confirmado/validado contablemente.",
        verbose_name="Acreditado"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación",
        help_text="Fecha y hora en que el movimiento se creó en el sistema.",
        null=True, blank=True
    )

    # ======================================================
    # MÉTODOS INTERNOS
    # ======================================================
    def generar_hash(self):
        raw = f"{uuid.uuid4()}-{self.codigo_referencia}-{self.fecha_devengo}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def calcular_finanzas(self):
        moneda = self.monto_bruto.currency if self.monto_bruto else "USD"

        bruto = self.monto_bruto or Money(0, moneda)
        descuento = self.descuento or Money(0, moneda)
        costo = self.costo_directo or Money(0, moneda)
        gastos = self.gastos_indirectos or Money(0, moneda)
        tasa = self.tasa_iva or Decimal("0.00")

        self.base_imponible = bruto - descuento
        self.iva = self.base_imponible * tasa
        self.monto_neto = self.base_imponible + self.iva
        self.utilidad_bruta = self.base_imponible - costo
        self.utilidad_neta = self.utilidad_bruta - gastos

    def clean(self):
        """
        Validaciones antes de guardar:
        - Debe ser ingreso o egreso.
        - Solo uno puede ser True.
        - monto_bruto nunca debe ser None.
        """
        if not self.es_ingreso and not self.es_egreso:
            raise ValidationError("El movimiento debe ser ingreso o egreso.")
        if self.es_ingreso and self.es_egreso:
            raise ValidationError("Un movimiento no puede ser ingreso y egreso al mismo tiempo.")

        # Asegurarse que monto_bruto tenga valor
        if self.monto_bruto is None:
            from djmoney.money import Money
            self.monto_bruto = Money(0, 'USD')
        if self.descuento is None:
            from djmoney.money import Money
            self.descuento = Money(0, 'USD')
        if self.costo_directo is None:
            from djmoney.money import Money
            self.costo_directo = Money(0, 'USD')
        if self.gastos_indirectos is None:
            from djmoney.money import Money
            self.gastos_indirectos = Money(0, 'USD')

    def save(self, *args, **kwargs):
        # Validar reglas de negocio antes de guardar
        self.clean()

        # Generar hash si no existe
        if not self.hash_registro:
            self.hash_registro = self.generar_hash()

        # Calcular montos automáticamente
        self.calcular_finanzas()

        super().save(*args, **kwargs)


    # ======================================================
    # METADATA
    # ======================================================
    class Meta:
        app_label = "smartbusinessanalytics_id"
        verbose_name = "Movimiento Financiero"
        verbose_name_plural = "Movimientos Financieros"
        ordering = ["-fecha_devengo"]

    def __str__(self):
        tipo = "Ingreso" if self.es_ingreso else "Egreso"
        return f"{tipo} | {self.codigo_referencia or self.hash_registro[:8]}"






class Ingreso(models.Model):
    # ======================================================
    # IDENTIFICACIÓN
    # ======================================================
    codigo_referencia = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código de referencia",
        help_text="Identificador único del ingreso, como número de factura o recibo."
    )

    descripcion = models.TextField(
        verbose_name="Descripción del ingreso",
        help_text="Detalle del producto o servicio vendido."
    )

    fecha_devengo = models.DateField(
        verbose_name="Fecha de devengo",
        help_text="Fecha en la que el ingreso se reconoce contablemente."
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
        help_text="Fecha y hora en que el ingreso se registra en el sistema."
    )

    # ======================================================
    # CLASIFICACIÓN
    # ======================================================
    TIPO_INGRESO_CHOICES = [
        ('producto', 'Venta de producto'),
        ('servicio', 'Prestación de servicio'),
        ('suscripcion', 'Ingreso recurrente'),
        ('otro', 'Otro'),
    ]

    tipo_ingreso = models.CharField(
        max_length=20,
        choices=TIPO_INGRESO_CHOICES,
        verbose_name="Tipo de ingreso",
        help_text="Clasificación contable del ingreso."
    )

    producto_servicio = models.CharField(
        max_length=150,
        verbose_name="Producto o servicio",
        help_text="Producto o servicio que genera el ingreso."
    )

    # ======================================================
    # CLIENTE
    # ======================================================
    cliente_nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre del cliente",
        help_text="Nombre del cliente que realiza el pago."
    )

    cliente_identificacion_fiscal = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Identificación fiscal del cliente",
        help_text="RFC, NIT, CIF u otro identificador fiscal."
    )

    # ======================================================
    # MONTOS BASE
    # ======================================================
    monto_bruto = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Monto bruto",
        help_text="Valor total de la venta antes de descuentos e impuestos."
    )

    descuento = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Descuento",
        help_text="Descuento aplicado a la venta."
    )

    tasa_iva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.16"),
        verbose_name="Tasa de IVA",
        help_text="Porcentaje de IVA aplicable. Ejemplo: 0.16 para 16%."
    )

    # ======================================================
    # RESULTADOS TRIBUTARIOS (AUTO)
    # ======================================================
    base_imponible = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="Base imponible",
        help_text="Monto sobre el cual se calcula el IVA (calculado automáticamente)."
    )

    iva = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="IVA",
        help_text="Impuesto al Valor Agregado calculado automáticamente."
    )

    monto_neto = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="Monto neto",
        help_text="Monto final del ingreso con impuestos incluidos."
    )

    # ======================================================
    # COSTOS Y UTILIDADES (AUTO)
    # ======================================================
    costo_producto = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Costo del producto",
        help_text="Costo directo del producto o servicio vendido."
    )

    gastos_asociados = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos asociados",
        help_text="Gastos indirectos relacionados con la venta."
    )

    utilidad_bruta = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="Utilidad bruta",
        help_text="Resultado de restar el costo del producto a la base imponible."
    )

    utilidad_neta = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="Utilidad neta",
        help_text="Utilidad final luego de descontar costos y gastos asociados."
    )

    # ======================================================
    # COBRO
    # ======================================================
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia bancaria'),
        ('tarjeta', 'Tarjeta'),
        ('pago_electronico', 'Pago electrónico'),
    ]

    BANCOS_CHOICES = [
        ("banco_pichincha", "Banco Pichincha"),
        ("banco_guayaquil", "Banco de Guayaquil"),
        ("produbanco", "Produbanco"),
        ("banco_internacional", "Banco Internacional"),
        ("banco_del_austro", "Banco del Austro"),
        ("banco_provincial", "Banco del Pacífico"),
        ("coopac", "Cooperativa COOPAC"),
        ("banco_bolivariano", "Banco Bolivariano"),
        ("banco_dell_sol", "Banco del Sol"),
        ("banco_machala", "Banco Machala"),
        ("banco_farmacias", "Banco de las Farmacias"),
        ("banco_florencia", "Banco Florencia"),
        ("banco_ambato", "Banco Ambato"),
        ("visa", "Visa"),
        ("mastercard", "Mastercard"),
        ("amex", "American Express"),
        ("diners", "Diners Club"),
        ("discover", "Discover"),
        ("jcb", "JCB"),
        ("unionpay", "UnionPay"),
        ("paymentez", "Paymentez"),
        ("datafast", "Datafast"),
        ("payphone", "PayPhone"),
        ("banco_pichincha_online", "Banco Pichincha Online"),
        ("banco_guayaquil_online", "Banco de Guayaquil Online"),
        ("redeban", "Redeban"),
        ("paypal", "PayPal"),
        ("stripe", "Stripe"),
        ("mercadopago", "MercadoPago"),
        ("square", "Square"),
        ("otros", "Otro"),
    ]

    banco = models.CharField(
        max_length=30,
        choices=BANCOS_CHOICES,
        null=True,
        blank=True,
        verbose_name="Institución Bancaria",
        help_text="Banco donde se realiza el cobro."
    )

    codigo_referencia_pago = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        verbose_name="Código de referencia de pago",
        help_text="Número de referencia de la transacción bancaria o comprobante de pago."
    )

    metodo_pago = models.CharField(
        max_length=30,
        choices=METODO_PAGO_CHOICES,
        verbose_name="Método de pago",
        help_text="Forma en la que el cliente realiza el pago."
    )

    fecha_cobro = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de cobro",
        help_text="Fecha en la que se recibió el pago."
    )

    cobrado = models.BooleanField(
        default=False,
        verbose_name="Ingreso cobrado",
        help_text="Indica si el ingreso ya fue cobrado."
    )

    # ======================================================
    # MÉTODO SAVE CORREGIDO
    # ======================================================
    def save(self, *args, **kwargs):
        moneda = self.monto_bruto.currency if self.monto_bruto else 'USD'

        # Valores seguros
        monto_bruto = self.monto_bruto or Money(0, moneda)
        descuento = self.descuento or Money(0, moneda)
        costo = self.costo_producto or Money(0, moneda)
        gastos = self.gastos_asociados or Money(0, moneda)
        tasa = self.tasa_iva or 0

        # Cálculos automáticos
        self.base_imponible = monto_bruto - descuento
        self.iva = self.base_imponible * tasa
        self.monto_neto = self.base_imponible + self.iva
        self.utilidad_bruta = self.base_imponible - costo
        self.utilidad_neta = self.utilidad_bruta - gastos

        super().save(*args, **kwargs)

    # ======================================================
    # METADATA Y STR
    # ======================================================
    class Meta:
        app_label = "smartbusinessanalytics_id"
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"
        ordering = ["-fecha_devengo"]

    def __str__(self):
        return f"{self.codigo_referencia} - {self.cliente_nombre}"





from django.db import models
from djmoney.models.fields import MoneyField
from decimal import Decimal


class Egreso(models.Model):
    # ======================================================
    # IDENTIFICACIÓN
    # ======================================================
    codigo_referencia = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Código de referencia",
        help_text="Identificador único del egreso, como número de factura o comprobante."
    )

    concepto = models.TextField(
        verbose_name="Concepto del egreso",
        help_text="Detalle del gasto o servicio pagado."
    )

    fecha_devengo = models.DateField(
        verbose_name="Fecha de devengo",
        help_text="Fecha en la que se reconoce contablemente el egreso."
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de registro",
        help_text="Fecha y hora en que el egreso se registra en el sistema."
    )

    # ======================================================
    # CLASIFICACIÓN
    # ======================================================
    TIPO_EGRESO_CHOICES = [
        ('compra', 'Compra de producto'),
        ('servicio', 'Pago de servicio'),
        ('nomina', 'Nómina y remuneraciones'),
        ('otro', 'Otro'),
    ]

    tipo_egreso = models.CharField(
        max_length=20,
        choices=TIPO_EGRESO_CHOICES,
        verbose_name="Tipo de egreso",
        help_text="Clasificación contable del egreso."
    )

    # ======================================================
    # PROVEEDOR / BENEFICIARIO
    # ======================================================
    proveedor_nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre del proveedor",
        help_text="Nombre de la persona o empresa beneficiaria del pago."
    )

    proveedor_identificacion_fiscal = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Identificación fiscal",
        help_text="RFC, NIT, CIF u otro identificador fiscal del proveedor."
    )

    # ======================================================
    # MONTOS BASE (MoneyField)
    # ======================================================
    monto_bruto = MoneyField(
        max_digits=10,
        default_currency='USD',
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto bruto",
        help_text="Valor total del egreso antes de descuentos e impuestos."
    )

    descuento = MoneyField(
        max_digits=10,
        default_currency='USD',
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Descuento",
        help_text="Descuento aplicado al egreso."
    )

    tasa_iva = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.12"),
        verbose_name="Tasa de IVA",
        help_text="Porcentaje de IVA aplicable. Ejemplo: 0.12 para 12%."
    )

    # ======================================================
    # RESULTADOS TRIBUTARIOS (AUTO)
    # ======================================================
    base_imponible = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="Base imponible",
        help_text="Monto sobre el cual se calcula el IVA (calculado automáticamente)."
    )

    iva = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="IVA",
        help_text="Impuesto al Valor Agregado calculado automáticamente."
    )

    monto_neto = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        editable=False,
        verbose_name="Monto neto",
        help_text="Monto final del egreso con impuestos incluidos."
    )

    # ======================================================
    # COSTOS Y UTILIDADES (AUTO)
    # ======================================================
    costo_asociado = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency='USD',
        verbose_name="Costo asociado",
        help_text="Costo directo relacionado con el egreso."
    )

    gastos_adicionales = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency='USD',
        verbose_name="Gastos adicionales",
        help_text="Gastos indirectos relacionados con el egreso."
    )

    utilidad_bruta = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default_currency='USD',
        editable=False,
        verbose_name="Utilidad bruta",
        help_text="Resultado de restar los costos a la base imponible."
    )

    utilidad_neta = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
        default_currency='USD',
        verbose_name="Utilidad neta",
        help_text="Utilidad final luego de descontar gastos adicionales."
    )

    # ======================================================
    # PAGO
    # ======================================================
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia bancaria'),
        ('tarjeta', 'Tarjeta'),
        ('pago_electronico', 'Pago electrónico'),
    ]

    metodo_pago = models.CharField(
        max_length=30,
        choices=METODO_PAGO_CHOICES,
        verbose_name="Método de pago",
        help_text="Forma en la que se realizó el pago."
    )

    pagado = models.BooleanField(
        default=False,
        verbose_name="Pagado",
        help_text="Indica si el egreso ya fue pagado."
    )

    fecha_pago = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de pago",
        help_text="Fecha en la que se realizó el pago."
    )

    # ======================================================
    # CÁLCULOS AUTOMÁTICOS
    # ======================================================
    def save(self, *args, **kwargs):
        if self.monto_bruto:
            descuento = self.descuento or 0
            self.base_imponible = self.monto_bruto - descuento
            self.iva = self.base_imponible * self.tasa_iva
            self.monto_neto = self.base_imponible + self.iva

            if self.costo_asociado:
                self.utilidad_bruta = self.base_imponible - self.costo_asociado
                gastos = self.gastos_adicionales or 0
                self.utilidad_neta = self.utilidad_bruta - gastos

        super().save(*args, **kwargs)

    class Meta:
        app_label = "smartbusinessanalytics_id"
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"
        ordering = ["-fecha_devengo"]

    def __str__(self):
        return f"{self.codigo_referencia} - {self.proveedor_nombre}"




from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from .models import Ingreso, Egreso
from django.db.models.signals import post_save
from django.dispatch import receiver

from decimal import Decimal, ROUND_HALF_UP
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money

from decimal import Decimal, ROUND_HALF_UP
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from django.db import models


from django.db import models
from decimal import Decimal
from djmoney.models.fields import MoneyField


class EstadoFinanciero(models.Model):

    BANCOS_CHOICES = [
        ("banco_pichincha", "Banco Pichincha"),
        ("Banco Guayaquil", "Banco de Guayaquil"),
        ("produbanco", "Produbanco"),
        ("banco_internacional", "Banco Internacional"),
        ("banco_del_austro", "Banco del Austro"),
        ("banco_provincial", "Banco del Pacífico"),
        ("coopac", "Cooperativa COOPAC"),
        ("banco_bolivariano", "Banco Bolivariano"),
        ("banco_dell_sol", "Banco del Sol"),
        ("banco_machala", "Banco Machala"),
        ("banco_farmacias", "Banco de las Farmacias"),
        ("banco_florencia", "Banco Florencia"),
        ("banco_ambato", "Banco Ambato"),
        ("visa", "Visa"),
        ("mastercard", "Mastercard"),
        ("amex", "American Express"),
        ("diners", "Diners Club"),
        ("discover", "Discover"),
        ("jcb", "JCB"),
        ("unionpay", "UnionPay"),
        ("paymentez", "Paymentez"),
        ("datafast", "Datafast"),
        ("payphone", "PayPhone"),
        ("banco_pichincha_online", "Banco Pichincha Online"),
        ("banco_guayaquil_online", "Banco de Guayaquil Online"),
        ("redeban", "Redeban"),
        ("paypal", "PayPal"),
        ("stripe", "Stripe"),
        ("mercadopago", "MercadoPago"),
        ("square", "Square"),
        ("otros", "Otro"),
    ]

    # PERÍODO DE ANÁLISIS
    fecha_inicio = models.DateField(
        verbose_name="Elegir fecha de inicio para análisis",
        help_text="Fecha inicial del período contable analizado"
    )

    fecha_fin = models.DateField(
        verbose_name="Elegir fecha de inicio para análisis",
        help_text="Fecha de corte del período contable analizado"
    )

    # MOVIMIENTOS BANCARIOS
    total_ingresos_bancos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        verbose_name="Ingresos bancarios",
        null=True,
        blank=True,
        help_text="Escriba el valor total de ingresos registrados e identificados en las cuentas bancarias, Ej: 1000.2"
    )

    total_egresos_bancos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Egresos bancarios",
        help_text="Escriba el valor total de egresos registrados e identificados en las cuentas bancarias, Ej: 1000.2"
    )

    nombre_banco =  models.CharField(
        max_length=30,
        choices=BANCOS_CHOICES,
        default ="banco_guayaquil",
        null=True,
        blank=True,
        verbose_name="Institución Bancaria",
        help_text="Identifique el banco correspondiente para analizar."
    )

    # RESULTADOS CONTABLES AGREGADOS
    total_efectivo_bancos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Efectivo Bancos",
        help_text="Total efectivo en bancos registrados"
    )

    total_efectivo = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Efectivo Contable",
        help_text="Total de Efectivo  contable"
    )

    total_ingresos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Ingresos contables",
        help_text="Total de ingresos registrados en la contabilidad"
    )

    total_egresos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Egresos contables",
        help_text="Total de egresos registrados en la contabilidad"
    )

    utilidad_bruta = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Utilidad bruta",
        help_text="Resultado de ingresos menos costos directos"
    )

    utilidad_neta = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Utilidad neta",
        help_text="Resultado final después de impuestos y gastos"
    )

    # CONCILIACIÓN BANCARIA
    diferencia_ingresos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Diferencia de ingresos",
        help_text="Diferencia absoluta entre ingresos bancarios y contables"
    )


    diferencia_egresos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Diferencia de egresos",
        help_text="Diferencia absoluta entre egresos bancarios y contables"
    )

    error_conciliacion_porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Error de conciliación (%)",
        help_text="Porcentaje de error entre ingresos bancarios y contables"
    )

    umbral_conciliacion = models.DecimalField(
    max_digits=5,
    decimal_places=2,
    default=Decimal('1.00'),
    verbose_name="Umbral de conciliación (%)",
    help_text="Porcentaje máximo permitido para considerar conciliado"
    )


    conciliado = models.BooleanField(
        default=False,
        verbose_name="Conciliado",
        help_text="Indica si la conciliación bancaria es aceptable"
    )

    # INDICADORES FINANCIEROS
    margen_utilidad_bruta = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Margen de utilidad bruta (%)",
        help_text="Porcentaje de utilidad bruta sobre los ingresos totales"
    )

    margen_utilidad_neta = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Margen de utilidad neta (%)",
        help_text="Porcentaje de utilidad neta sobre los ingresos totales"
    )

    rentabilidad = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Rentabilidad (%)",
        help_text="Indicador de rendimiento financiero del período"
    )

    ratio_cobertura = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Ratio de cobertura",
        help_text="Capacidad de cubrir obligaciones financieras"
    )

    # GASTOS Y APLICACIONES
    ventas = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Ventas",
        help_text="Total de ingresos por ventas"
    )

    porcentaje_ventas = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal('0.00'),
        verbose_name="Porcentaje de ventas (%)",
        help_text="Porcentaje de ventas sobre la utilidad neta"
    )

    inversiones = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Inversiones",
        help_text="Monto destinado a inversiones"
    )

    acciones_legales = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Acciones legales",
        help_text="Gastos asociados a procesos legales"
    )

    gastos_fijos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos fijos",
        help_text="Gastos recurrentes y permanentes"
    )

    gastos_operativos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos operativos",
        help_text="Gastos necesarios para la operación del negocio"
    )

    gastos_publicitarios = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos publicitarios",
        help_text="Inversión en publicidad y marketing"
    )

    gastos_legales = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos legales",
        help_text="Honorarios y costos legales"
    )

    gastos_nomina = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos de nómina",
        help_text="Costos salariales y prestaciones"
    )

    gastos_tributarios = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Gastos tributarios",
        help_text="Impuestos y obligaciones fiscales"
    )

    deudas_pagar = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Deudas por pagar",
        help_text="Obligaciones financieras pendientes"
    )

    declaracion_iva = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Declaración de IVA",
        help_text="Monto correspondiente al impuesto al valor agregado"
    )

    deduccion_gastos = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Deducción de gastos",
        help_text="Gastos deducibles para efectos fiscales"
    )

    cuentas_pagar = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Cuentas por pagar",
        help_text="Obligaciones pendientes con proveedores"
    )

    cuentas_cobrar = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Cuentas por cobrar",
        help_text="Montos pendientes de cobro a clientes"
    )

    # CAMPOS AVANZADOS
    punto_equilibrio = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Punto de equilibrio",
        help_text="Nivel de ingresos donde no hay pérdidas ni ganancias"
    )

    dividendos_accionistas = MoneyField(
        max_digits=12,
        decimal_places=2,
        default_currency='USD',
        null=True,
        blank=True,
        verbose_name="Dividendos a accionistas",
        help_text="Monto distribuido a los accionistas"
    )

    analisis_flujo_financiero = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Análisis de flujo financiero",
        help_text="Información detallada del flujo de caja en formato estructurado"
    )


    # ==============================
    # MÉTODO PRINCIPAL
    # ==============================
    def calcular_estado_financiero(self, tasa_dividendo=Decimal('0.50')):
        if not self.fecha_inicio or not self.fecha_fin:
            return

        from smartbusinessanalytics_id.models import MovimientoFinanciero

        ingresos = MovimientoFinanciero.objects.filter(
            fecha_devengo__range=(self.fecha_inicio, self.fecha_fin),
            es_ingreso=True
        )

        egresos = MovimientoFinanciero.objects.filter(
            fecha_devengo__range=(self.fecha_inicio, self.fecha_fin),
            es_egreso=True
        )

        # ------------------------------
        # Helpers
        # ------------------------------
        def sumar_money(qs, campo):
            total = Money(0, 'USD')
            for obj in qs:
                val = getattr(obj, campo, None)
                if isinstance(val, Money):
                    total += val
            return total

        def d(value):
            return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP) if value else Decimal('0.00')

        def sumar_por_categoria(qs, categoria, campo='monto_neto'):
            total = Money(0, 'USD')
            for obj in qs.filter(categoria=categoria):
                val = getattr(obj, campo, None)
                if isinstance(val, Money):
                    total += val
            return total

        def sumar_por_categoria_ingresos(qs, categoria_ingresos, campo='monto_neto'):
            total = Money(0, 'USD')
            for obj in qs.filter(categoria_ingresos=categoria_ingresos):
                val = getattr(obj, campo, None)
                if isinstance(val, Money):
                    total += val
            return total

        def sumar_iva_duduccion(qs):
            total = Money(0, 'USD')
            
            for obj in qs.filter(
                es_egreso=True):
                if obj.iva:
                    total += obj.iva
                    
            return total

        def sumar_iva_declaracion(qs):
            total = Money(0, 'USD')
            
            for obj in qs.filter(
                es_ingreso=True):
                if obj.iva:
                    total += obj.iva
                    
            return total

        def sumar_cuentas_pagar(qs):
            total = Money(0, 'USD')
            
            for obj in qs.filter(
                es_egreso=True,confirmado=False):
                if obj.monto_neto:
                    total += obj.monto_neto
                    
            return total

        def sumar_cuentas_cobrar(qs):
            total = Money(0, 'USD')
            
            for obj in qs.filter(
                es_ingreso=True,confirmado=False):
                if obj.monto_neto:
                    total += obj.monto_neto
                    
            return total

        def sumar_deudas_pagar(qs):
            total = Money(0, 'USD')
            
            for obj in qs.filter(
                es_egreso=True,categoria='pago_deuda'):
                if obj.monto_neto:
                    total += obj.monto_neto
                    
            return total

        def sumar_acciones_legales_pagar(qs):
            total = Money(0, 'USD')
            
            for obj in qs.filter(
                es_ingreso=True,categoria_ingresos='acciones_legales'):
                if obj.monto_neto:
                    total += obj.monto_neto
                    
            return total


        def ratio(num, den):
            if den <= 0:
                return Decimal('0.00')
            return (num / den * Decimal('100')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # ------------------------------
        # GASTOS y VENTAS primero
        # ------------------------------
        self.ventas = sumar_por_categoria_ingresos(ingresos, 'ventas')
        self.inversiones = sumar_por_categoria_ingresos(ingresos, 'inversion')
        self.acciones_legales =sumar_acciones_legales_pagar(ingresos)
        self.gastos_operativos = sumar_por_categoria(egresos, 'gastos_operativos')
        self.gastos_nomina = sumar_por_categoria(egresos, 'gastos_nomina')
        self.gastos_tributarios = sumar_por_categoria(egresos, 'gastos_tributarios')
        self.gastos_publicitarios = sumar_por_categoria(egresos, 'gastos_publicitarios')
        self.gastos_legales = sumar_por_categoria(egresos, 'gastos_legales')
        self.declaracion_iva = sumar_iva_declaracion(ingresos)
        self.deduccion_gastos = sumar_iva_duduccion(egresos)
        self.cuentas_pagar = sumar_cuentas_pagar(egresos)
        self.deudas_pagar = sumar_cuentas_cobrar(egresos)
        self.cuentas_cobrar = sumar_cuentas_cobrar(ingresos)
        self.deudas_pagar = sumar_deudas_pagar(egresos)


        # ------------------------------
        # Totales
        # ------------------------------
        self.total_ingresos = sumar_money(ingresos, 'monto_neto')
        self.total_egresos = sumar_money(egresos, 'monto_neto')
        self.utilidad_bruta = sumar_money(ingresos, 'utilidad_bruta') - sumar_money(egresos, 'costo_directo')
        self.utilidad_neta = sumar_money(ingresos, 'utilidad_neta')

        ingresos_v = d(self.total_ingresos.amount)
        egresos_v = d(self.total_egresos.amount)
        utilidad_neta_v = d(self.utilidad_neta.amount)
        ventas_v = d(self.ventas.amount) if self.ventas else Decimal('0')

        # ------------------------------
        # Porcentaje Ventas / Utilidad Neta
        # ------------------------------
        self.porcentaje_ventas = ratio(ventas_v, utilidad_neta_v).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        # ------------------------------
        # Indicadores
        # ------------------------------
        self.margen_utilidad_bruta = ratio(d(self.utilidad_bruta.amount), ingresos_v)
        self.margen_utilidad_neta = ratio(utilidad_neta_v, ingresos_v)
        self.rentabilidad = ratio(utilidad_neta_v, ingresos_v)
        self.ratio_cobertura = ratio(ingresos_v, egresos_v)

        # ------------------------------
        # Punto de equilibrio
        # ------------------------------
        margen_contribucion = ingresos_v - d(sumar_money(egresos, 'costo_directo').amount)
        self.punto_equilibrio = Money(
            (d(sumar_money(egresos, 'monto_neto').amount) / margen_contribucion * ingresos_v).quantize(Decimal('0.01'))
            if margen_contribucion > 0 else 0,
            'USD'
        )

        # ------------------------------
        # Dividendos
        # ------------------------------
        self.dividendos_accionistas = Money(
            (utilidad_neta_v * tasa_dividendo).quantize(Decimal('0.01')) if utilidad_neta_v > 0 else 0,
            'USD'
        )

        # ------------------------------
        # Flujo financiero
        # ------------------------------
        flujo_total = ingresos_v + egresos_v
        self.analisis_flujo_financiero = {
            "ingresos": float(ingresos_v),
            "egresos": float(egresos_v),
            "utilidad_neta": float(utilidad_neta_v),
            "ingresos_pct": float(ratio(ingresos_v, flujo_total)),
            "egresos_pct": float(ratio(egresos_v, flujo_total)),
        }


        # ------------------------------
        # CONCILIACIÓN BANCARIA
        # ------------------------------

        # Efectivo contable
        self.total_efectivo = Money(
            (ingresos_v - egresos_v).quantize(Decimal('0.01')),
            'USD'
        )

        # Efectivo bancario
        bancos_ing = d(self.total_ingresos_bancos.amount) if self.total_ingresos_bancos else Decimal('0')
        bancos_egr = d(self.total_egresos_bancos.amount) if self.total_egresos_bancos else Decimal('0')

        self.total_efectivo_bancos = Money(
            (bancos_ing - bancos_egr).quantize(Decimal('0.01')),
            'USD'
        )

        # Diferencia absoluta de ingresos
        diferencia = abs(bancos_ing - ingresos_v)

        self.diferencia_ingresos = Money(
            diferencia.quantize(Decimal('0.01')),
            'USD'
        )

        # Diferencia absoluta de ingresos
        diferencia_egresos = abs(bancos_egr - egresos_v)

        self.diferencia_egresos = Money(
            diferencia_egresos.quantize(Decimal('0.01')),
            'USD'
        )

        # Error de conciliación (%)
        if ingresos_v > 0:
            self.error_conciliacion_porcentaje = (
                (diferencia / ingresos_v) * Decimal('100')
            ).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            self.error_conciliacion_porcentaje = Decimal('0.00')

        umbral = (
            self.umbral_conciliacion
            if self.umbral_conciliacion is not None
            else Decimal('1.00')
        )

        self.conciliado = (
            self.error_conciliacion_porcentaje <= umbral
        )


    # ==============================
    # Meta y Métodos
    # ==============================
    class Meta:
        app_label = "smartbusinessanalytics_id"
        ordering = ["-fecha_inicio"]

    def save(self, *args, **kwargs):
        recalcular = kwargs.pop("recalcular", True)
        if recalcular and self.fecha_inicio and self.fecha_fin:
            self.calcular_estado_financiero()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Estado Financiero {self.fecha_inicio} - {self.fecha_fin}"
