from django.db import models
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.models import Orderable


@register_setting
class InstagramSettings(BaseGenericSetting, ClusterableModel):
    panels = [
        InlinePanel('categories', label="Categorías disponibles (I+D)")
    ]


class CategoryItem(Orderable):
    settings = ParentalKey(
        InstagramSettings,
        on_delete=models.CASCADE,
        related_name='categories',
        null=True, blank=True
    )

    name = models.CharField(
        max_length=50,
        verbose_name="Nombre",
        help_text="Define una categoría disponible para los posts."
    )

    panels = [
        FieldPanel('name'),
    ]

    def __str__(self):
        return self.name