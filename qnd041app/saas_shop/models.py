from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=True, blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name or str(self.id)

    def get_absolute_url(self):
        return reverse('saas_shop:product_list_by_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True, null=True, blank=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='products/%Y/%m/%d', null=True, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    available = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name or str(self.id)

    def get_absolute_url(self):
        return reverse('saas_shop:product_detail', args=[self.id, self.slug])
