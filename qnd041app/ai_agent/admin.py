from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from unfold.admin import ModelAdmin
from .models import AIAgent, AgentSkill, AgentSoul





@admin.register(AgentSoul)
class AgentSoulAdmin(ModelAdmin):
    list_display = ("nombre", "slug", "actualizado_en")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(AgentSkill)
class AgentSkillAdmin(ModelAdmin):
    list_display = ("nombre", "slug", "trigger_descripcion", "activa")
    list_filter = ("activa",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(AIAgent)
class AIAgentAdmin(ModelAdmin):
    list_display = ("nombre", "slug", "modelo_ollama", "soul", "activo")
    list_filter = ("activo", "modelo_ollama")
    filter_horizontal = ("skills",)
    prepopulated_fields = {"slug": ("nombre",)}