from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin, TabularInline

from .models import (
    AreaComun,
    CargoAlicuota,
    DocumentoNormativo,
    Edificio,
    FragmentoNormativo,
    OrdenMantenimiento,
    RegistroLimpieza,
    Unidad,
)


class AreaComunInline(TabularInline):
    model = AreaComun
    extra = 0
    fields = ("nombre", "tipo_area", "frecuencia_limpieza_dias")


class UnidadInline(TabularInline):
    model = Unidad
    extra = 0
    fields = ("codigo", "piso_o_torre", "alicuota_porcentaje")


class FragmentoNormativoInline(TabularInline):
    model = FragmentoNormativo
    extra = 0
    fields = ("referencia", "contenido")


@admin.register(Edificio)
class EdificioAdmin(ModelAdmin):
    list_display = ("nombre", "codigo", "direccion", "activo")
    list_filter = ("activo",)
    search_fields = ("nombre", "codigo", "direccion")
    prepopulated_fields = {"codigo": ("nombre",)}
    list_editable = ("activo",)
    inlines = [AreaComunInline, UnidadInline]


@admin.register(AreaComun)
class AreaComunAdmin(ModelAdmin):
    list_display = ("nombre", "edificio", "tipo_area", "frecuencia_limpieza_dias")
    list_filter = ("tipo_area", "edificio")
    search_fields = ("nombre", "edificio__nombre", "edificio__codigo")
    autocomplete_fields = ("edificio",)


@admin.register(RegistroLimpieza)
class RegistroLimpiezaAdmin(ModelAdmin):
    list_display = (
        "id",
        "area_comun",
        "fecha_ejecucion",
        "responsable",
        "estado",
        "observaciones_cortas",
    )
    list_filter = ("estado", "fecha_ejecucion", "area_comun__edificio", "area_comun__tipo_area")
    search_fields = (
        "responsable",
        "observaciones",
        "area_comun__nombre",
        "area_comun__edificio__nombre",
    )
    autocomplete_fields = ("area_comun",)
    date_hierarchy = "fecha_ejecucion"
    list_editable = ("estado",)

    @admin.display(description=_("Observaciones"))
    def observaciones_cortas(self, obj):
        if not obj.observaciones:
            return "-"
        return obj.observaciones if len(obj.observaciones) <= 60 else f"{obj.observaciones[:57]}..."


@admin.register(OrdenMantenimiento)
class OrdenMantenimientoAdmin(ModelAdmin):
    list_display = (
        "titulo",
        "edificio",
        "area_comun",
        "tipo",
        "estado",
        "fecha_programada",
        "fecha_cierre",
        "costo_estimado",
        "costo_real",
    )
    list_filter = ("tipo", "estado", "fecha_programada", "edificio")
    search_fields = ("titulo", "descripcion", "edificio__nombre", "area_comun__nombre")
    autocomplete_fields = ("edificio", "area_comun")
    date_hierarchy = "fecha_programada"
    list_editable = ("estado", "costo_real")
    fieldsets = (
        (
            _("Ubicación y clasificación"),
            {"fields": ("edificio", "area_comun", "tipo", "estado")},
        ),
        (
            _("Detalle de la orden"),
            {"fields": ("titulo", "descripcion")},
        ),
        (
            _("Programación y costos"),
            {
                "fields": (
                    "fecha_programada",
                    "fecha_cierre",
                    "costo_estimado",
                    "costo_real",
                )
            },
        ),
    )


@admin.register(Unidad)
class UnidadAdmin(ModelAdmin):
    list_display = ("codigo", "edificio", "piso_o_torre", "alicuota_porcentaje")
    list_filter = ("edificio", "piso_o_torre")
    search_fields = ("codigo", "piso_o_torre", "edificio__nombre", "edificio__codigo")
    autocomplete_fields = ("edificio",)


@admin.register(CargoAlicuota)
class CargoAlicuotaAdmin(ModelAdmin):
    list_display = (
        "unidad",
        "periodo",
        "monto_alicuota",
        "monto_expensas_extra",
        "monto_pagado",
        "saldo_pendiente",
        "estado",
        "fecha_vencimiento",
    )
    list_filter = ("estado", "periodo", "fecha_vencimiento", "unidad__edificio")
    search_fields = ("periodo", "unidad__codigo", "unidad__edificio__nombre")
    autocomplete_fields = ("unidad",)
    date_hierarchy = "fecha_vencimiento"
    list_editable = ("estado", "monto_pagado")

    @admin.display(description=_("Saldo pendiente"))
    def saldo_pendiente(self, obj):
        total = (obj.monto_alicuota or 0) + (obj.monto_expensas_extra or 0)
        return total - (obj.monto_pagado or 0)


@admin.register(DocumentoNormativo)
class DocumentoNormativoAdmin(ModelAdmin):
    list_display = ("titulo", "tipo_documento", "edificio", "vigente", "actualizado_en")
    list_filter = ("tipo_documento", "vigente", "edificio")
    search_fields = ("titulo", "edificio__nombre")
    autocomplete_fields = ("edificio",)
    list_editable = ("vigente",)
    inlines = [FragmentoNormativoInline]


@admin.register(FragmentoNormativo)
class FragmentoNormativoAdmin(ModelAdmin):
    list_display = ("referencia", "documento", "extracto_contenido")
    list_filter = ("documento__tipo_documento", "documento__vigente", "documento")
    search_fields = ("referencia", "contenido", "documento__titulo")
    autocomplete_fields = ("documento",)

    @admin.display(description=_("Contenido"))
    def extracto_contenido(self, obj):
        if not obj.contenido:
            return ""
        return obj.contenido if len(obj.contenido) <= 90 else f"{obj.contenido[:87]}..."