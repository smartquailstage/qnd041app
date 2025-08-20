from django.db import models

PRODUCT_CHOICES = [
    ('SBA', 'SmartBusinessAnalytics'),
    ('SBM', 'SmartBusinessMedia'),
    ('SBL', 'SmartBusinessLaw'),
    ('SBT', 'SmartBusinessTechnologies'),
]

class ProductCalculation(models.Model):
    product = models.CharField(max_length=3, choices=PRODUCT_CHOICES)
    include_rd = models.BooleanField(default=False)
    include_automation = models.BooleanField(default=False)
    include_ai = models.BooleanField(default=False)
    num_processes = models.PositiveIntegerField(default=1)
    data_volume = models.PositiveIntegerField(default=0, help_text="En MB")
    complexity = models.IntegerField(default=1, help_text="1-5")
    result_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_product_display()} - ${self.result_cost} - {self.created_at.date()}"
    class Meta:
        verbose_name = "Product Calculation"
        verbose_name_plural = "Product Calculations"
        ordering = ['-created_at']


INFRA_CHOICES = [
    ('onprem', 'Nube Privada / On-Premises'),
    ('public', 'Nube Pública'),
    ('hybrid', 'Arquitectura Híbrida'),
]

class InfrastructureQuote(models.Model):
    infra_type = models.CharField(max_length=10, choices=INFRA_CHOICES)
    cpu_cores = models.PositiveIntegerField()
    ram_gb = models.PositiveIntegerField()
    storage_gb = models.PositiveIntegerField()
    bandwidth_mbps = models.PositiveIntegerField()
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_infra_type_display()} - ${self.estimated_cost} ({self.created_at.date()})"