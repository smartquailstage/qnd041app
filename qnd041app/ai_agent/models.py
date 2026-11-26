from django.db import models


class AgentSoul(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    descripcion = models.TextField(blank=True)
    contenido_md = models.TextField(
        help_text="Identidad, tono, guardrails y reglas base del agente en formato Markdown."
    )
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class AgentSkill(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    trigger_descripcion = models.CharField(
        max_length=255,
        help_text="Cuándo debe aplicarse esta skill (ej. 'Consulta de huecos en agenda').",
    )
    contenido_md = models.TextField(
        help_text="Instrucciones, formato de salida y herramientas permitidas en Markdown."
    )
    herramientas_permitidas = models.JSONField(
        default=list,
        blank=True,
        help_text="Lista de nombres de tools/MCP permitidas para esta skill.",
    )
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class AIAgent(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    modelo_ollama = models.CharField(max_length=100, default="qwen2.5:1.5b")
    temperatura = models.FloatField(default=0.2)
    soul = models.ForeignKey(AgentSoul, on_delete=models.PROTECT, related_name="agentes")
    skills = models.ManyToManyField(AgentSkill, blank=True, related_name="agentes")
    activo = models.BooleanField(default=True)

    def compilar_system_prompt(self, skills_filtradas=None) -> str:
        secciones = [
            f"# SOUL: {self.soul.nombre}\n\n{self.soul.contenido_md.strip()}"
        ]
        skills_qs = (
            skills_filtradas
            if skills_filtradas is not None
            else self.skills.filter(activa=True)
        )
        bloques_skills = []
        for skill in skills_qs:
            tools_txt = (
                f"\n**Herramientas permitidas:** `{', '.join(skill.herramientas_permitidas)}`"
                if skill.herramientas_permitidas
                else "\n**Herramientas permitidas:** `ninguna`"
            )
            bloques_skills.append(
                f"## SKILL: {skill.nombre}\n"
                f"**Cuándo aplicar:** {skill.trigger_descripcion}{tools_txt}\n\n"
                f"{skill.contenido_md.strip()}"
            )
        if bloques_skills:
            secciones.append(
                "# SKILLS DISPONIBLES\n\n" + "\n\n---\n\n".join(bloques_skills)
            )
        return "\n\n====================================\n\n".join(secciones)

    def __str__(self):
        return f"{self.nombre} ({self.modelo_ollama})"