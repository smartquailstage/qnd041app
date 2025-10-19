from django.db import models
from business_customer_projects.models import BusinessSystemProject
from saas_shop.models import Product

# Create your models here.
class Facturation(models.Model):
    project = models.ForeignKey(BusinessSystemProject, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=100)
    concept = models.ManyToManyField(Product, related_name='invoices')
    detail = models.TextField()
    amount_without_tax = models.DecimalField(max_digits=12, decimal_places=2)
    amount_with_tax = models.DecimalField(max_digits=12, decimal_places=2)
    invoice_file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturación'
        ordering = ['-created_at']

    def __str__(self):
        return f'Factura {self.invoice_number} - {self.project.name}'