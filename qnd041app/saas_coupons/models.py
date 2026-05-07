from django.db import models
from django.core.validators import MinValueValidator, \
                                   MaxValueValidator


from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Coupon(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='coupons',
        null=True,
        blank=True
    )

    code = models.CharField(
            max_length=50,
    unique=True,
    null=True,
    blank=True
    )

    valid_from = models.DateTimeField(null=True,
        blank=True)

    valid_to = models.DateTimeField(null=True,
        blank=True)

    discount = models.IntegerField(null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )

    active = models.BooleanField(default=True)

    # ===============================
    # NUEVOS CAMPOS
    # ===============================

    ingresos_anuales = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Ingresos anuales'
    )

    presupuesto_real = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Presupuesto real disponible'
    )

    descripcion_valor_agregado = models.TextField(
        null=True,
        blank=True,
        verbose_name='Descripción del valor agregado del proyecto'
    )

    created = models.DateTimeField(
        auto_now_add=True, null=True, blank=True
    )

    updated = models.DateTimeField(
        auto_now=True,null=True, blank=True
    )

    def __str__(self):
        return self.code or "Cupón pendiente"