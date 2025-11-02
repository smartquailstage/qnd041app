from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import CompanyInfo, PendingAppointment

# ========================
# Admin para CompanyInfo
# ========================
@admin.register(CompanyInfo)
class CompanyInfoAdmin(ModelAdmin):
    list_display = ('title', 'active')
    list_filter = ('active',)
    search_fields = ('title', 'content')
    ordering = ('title',)
    unfold_fields = ('content',)  # Campo que se puede expandir en la lista

    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(active=True)
    activate.short_description = "Activar seleccionadas"

    def deactivate(self, request, queryset):
        queryset.update(active=False)
    deactivate.short_description = "Desactivar seleccionadas"


# ==============================
# Admin para PendingAppointment
# ==============================
@admin.register(PendingAppointment)
class PendingAppointmentAdmin(ModelAdmin):
    list_display = ('phone', 'user_name', 'desired_date', 'step')
    list_filter = ('step',)
    search_fields = ('phone', 'user_name')
    ordering = ('step', 'desired_date')
    unfold_fields = ('user_name',)  # Campo expandible para ver el nombre completo
