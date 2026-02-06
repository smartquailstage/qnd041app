from django.db import models
from djmoney.models.fields import MoneyField
from decimal import Decimal
from django.utils.timezone import now


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
    # MONTOS BASE (MoneyField)
    # ======================================================
    monto_bruto = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto bruto",
        help_text="Valor total de la venta antes de descuentos e impuestos."
    )

    descuento = MoneyField(
        max_digits=10,
        decimal_places=2,
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
        null=True,
        blank=True,
        editable=False,
        verbose_name="Base imponible",
        help_text="Monto sobre el cual se calcula el IVA (calculado automáticamente)."
    )

    iva = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
        verbose_name="IVA",
        help_text="Impuesto al Valor Agregado calculado automáticamente."
    )

    monto_neto = MoneyField(
        max_digits=10,
        decimal_places=2,
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
        null=True,
        blank=True,
        verbose_name="Costo del producto",
        help_text="Costo directo del producto o servicio vendido."
    )

    gastos_asociados = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Gastos asociados",
        help_text="Gastos indirectos relacionados con la venta."
    )

    utilidad_bruta = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
        verbose_name="Utilidad bruta",
        help_text="Resultado de restar el costo del producto a la base imponible."
    )

    utilidad_neta = MoneyField(
        max_digits=10,
        decimal_places=2,
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
    # -------------------------
    # Bancos locales en Ecuador
    # -------------------------
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
    # -------------------------
    # Marcas de tarjetas de crédito
    # -------------------------
    ("visa", "Visa"),
    ("mastercard", "Mastercard"),
    ("amex", "American Express"),
    ("diners", "Diners Club"),
    ("discover", "Discover"),
    ("jcb", "JCB"),
    ("unionpay", "UnionPay"),
    # -------------------------
    # Pasarelas de pago
    # -------------------------
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
    # -------------------------
    # Opción general
    # -------------------------
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
    # CÁLCULOS AUTOMÁTICOS
    # ======================================================
    def save(self, *args, **kwargs):
        if self.monto_bruto:
            descuento = self.descuento or 0
            self.base_imponible = self.monto_bruto - descuento
            self.iva = self.base_imponible * self.tasa_iva
            self.monto_neto = self.base_imponible + self.iva

            if self.costo_producto:
                self.utilidad_bruta = self.base_imponible - self.costo_producto
                gastos = self.gastos_asociados or 0
                self.utilidad_neta = self.utilidad_bruta - gastos

        super().save(*args, **kwargs)

    class Meta:
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
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Monto bruto",
        help_text="Valor total del egreso antes de descuentos e impuestos."
    )

    descuento = MoneyField(
        max_digits=10,
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
        null=True,
        blank=True,
        editable=False,
        verbose_name="Base imponible",
        help_text="Monto sobre el cual se calcula el IVA (calculado automáticamente)."
    )

    iva = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        editable=False,
        verbose_name="IVA",
        help_text="Impuesto al Valor Agregado calculado automáticamente."
    )

    monto_neto = MoneyField(
        max_digits=10,
        decimal_places=2,
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
        verbose_name="Costo asociado",
        help_text="Costo directo relacionado con el egreso."
    )

    gastos_adicionales = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Gastos adicionales",
        help_text="Gastos indirectos relacionados con el egreso."
    )

    utilidad_bruta = MoneyField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
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
        verbose_name = "Egreso"
        verbose_name_plural = "Egresos"
        ordering = ["-fecha_devengo"]

    def __str__(self):
        return f"{self.codigo_referencia} - {self.proveedor_nombre}"
