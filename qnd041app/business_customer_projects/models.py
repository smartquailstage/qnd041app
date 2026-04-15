from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from usuarios.models  import SmartQuailCrew
from saas_shop.models import Product
from saas_orders.models import SaaSOrder



from django.db import models
from django.conf import settings
from django.urls import reverse

class BusinessSystemProject(models.Model):
    # Campo para el usuario logueado (asociado con el modelo de usuario)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='business_projects',
        verbose_name='Producto asociado'
    )
    usuarios_max = models.IntegerField(default=1, verbose_name='Número máximo de usuarios simultáneos')
    has_automation = models.BooleanField(default=False, verbose_name='¿Incluye automatización?')
    has_ai = models.BooleanField(default=False, verbose_name='¿Incluye inteligencia artificial?')
    is_active = models.BooleanField(default=True, verbose_name='¿Proyecto activo?')
    is_domain_configured = models.BooleanField(default=False, verbose_name='¿Dispone de dominio privado?')
    domain_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nombre de dominio privado')
    public_domain = models.URLField(blank=True, null=True, verbose_name='Dominio público asignado')
    velocity_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, verbose_name='Puntuación de velocidad del sistema')

    saas_order = models.OneToOneField(
        SaaSOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_project",
        verbose_name="Orden SaaS relacionada"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        #editable=False,  # evita errores similares al de 'executed_at'
        related_name='business_projects',
        verbose_name='Producto asociado'
    )



    # Nombre y descripción del proyecto
    name = models.CharField(max_length=200, help_text="Nombre del proyecto de sistema empresarial",default="Iniciando")
    description = models.TextField()

    # Fecha de creación
    created_at = models.DateTimeField(auto_now_add=True)

    # Equipo SmartQuail
    crew_members = models.ManyToManyField(
        'usuarios.SmartQuailCrew',
        related_name='projects',
        blank=True,
        verbose_name='Equipo asignado'
    )

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)", default=10)

    # Sector de negocio
    SECTOR_CHOICES = [
        ('gastronomico', 'Gastronómico'),
        ('servicios', 'Servicios'),
        ('administrativo', 'Administrativo'),
        ('finanzas', 'Finanzas'),
        ('banca', 'Banca'),
        ('gubernamental', 'Organización Gubernamental'),
        ('no_gubernamental', 'No Gubernamental'),
        ('comercio_electronico', 'Comercio Electrónico'),
        ('marketing_publicidad', 'Marketing y Publicidad'),
        ('educativo', 'Educativo'),
        ('medico_salud', 'Médico y Salud'),
        ('transporte', 'Transporte'),
        ('cadena_suministros', 'Cadena de Suministros'),
        ('agricultura', 'Agricultura'),
    ]

    business_sector = models.CharField(
        max_length=50,
        choices=SECTOR_CHOICES,
        default='gastronomico',
        verbose_name='Sector de Negocio'
    )

    # ✅ NUEVOS CAMPOS DE LOGOTIPOS
    logo_rectangular = models.ImageField(
        upload_to="business/logos/rectangular/",
        null=True,
        blank=True,
        verbose_name="Logotipo rectangular",
        help_text="Formato recomendado: 4:1 (ancho:alto)"
    )

    logo_cuadrado = models.ImageField(
        upload_to="business/logos/cuadrado/",
        null=True,
        blank=True,
        verbose_name="Logotipo cuadrado",
        help_text="Formato recomendado: 1:1 (ancho:alto)"
    )

    latencia_aproximada_ms = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Latencia aproximada (ms)",
        help_text="Latencia estimada del sistema en milisegundos"
    )
    procesamiento_aproximado_vcpu = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Procesamiento aproximado (vCPU milicore)",
        help_text="Procesamiento estimado en vCPU milicore"
    )
    procesamiento_total_aproximado_millicore = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Procesamiento total aproximado (millicore)",
        help_text="Procesamiento total estimado en millicore"
    )
    memoria_aproximada_gb = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Memoria aproximada (GB)",
        help_text="Memoria estimada en GB"
    )
    memoria_total = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Memoria total (MB)",
        help_text="Memoria total en MB"
    )
    almacenamiento_aproximado_gb = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Almacenamiento aproximado (GB)",
        help_text="Almacenamiento estimado en GB"
    )

    almacenamiento_total_mb = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Almacenamiento total (GB)",
        help_text="Almacenamiento total en GB"
    )
    active_processes_aproximados = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Procesos activos aproximados",
        help_text="Número estimado de procesos activos"
    )

    porcentaje_almacenamiento = models.FloatField(null=True, blank=True)
    porcentaje_procesamiento = models.FloatField(null=True, blank=True)
    porcentaje_memoria = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("business_customer_projects:project_detail", kwargs={"pk": self.pk})


    def save(self, *args, **kwargs):
        
        if self.saas_order:
            item = self.saas_order.items.first()
            if item:
                self.product = item.product

        if self.almacenamiento_aproximado_gb and self.almacenamiento_total_mb:
            total_gb = self.almacenamiento_total_mb / 1024
            if total_gb > 0:
                self.porcentaje_almacenamiento = round(
                    (self.almacenamiento_aproximado_gb / total_gb) * 100, 2)
                    
        if self.procesamiento_aproximado_vcpu and self.procesamiento_total_aproximado_millicore:
            if self.procesamiento_total_aproximado_millicore > 0:
                self.porcentaje_procesamiento = round(
                    (self.procesamiento_aproximado_vcpu /
                    self.procesamiento_total_aproximado_millicore) * 100, 2
                    )
                    
        if self.memoria_aproximada_gb and self.memoria_total:
            total_gb = self.memoria_total / 1024
            if total_gb > 0:
                self.porcentaje_memoria = round(
                    (self.memoria_aproximada_gb / total_gb) * 100, 2)
                    
        super().save(*args, **kwargs)


@property
def porcentaje_almacenamiento(self):
    if self.almacenamiento_aproximado_gb and self.almacenamiento_total_mb:
        total_gb = self.almacenamiento_total_mb / 1024
        if total_gb > 0:
            return round((self.almacenamiento_aproximado_gb / total_gb) * 100, 2)
    return None


@property
def porcentaje_procesamiento(self):
    if self.procesamiento_aproximado_vcpu and self.procesamiento_total_aproximado_millicore:
        if self.procesamiento_total_aproximado_millicore > 0:
            return round((self.procesamiento_aproximado_vcpu /
                          self.procesamiento_total_aproximado_millicore) * 100, 2)
    return None


@property
def porcentaje_memoria(self):
    if self.memoria_aproximada_gb and self.memoria_total:
        total_gb = self.memoria_total / 1024
        if total_gb > 0:
            return round((self.memoria_aproximada_gb / total_gb) * 100, 2)
    return None




from django.db import models

from django.db import models
from django.utils import timezone


class MonthlySystemMetrics(models.Model):
    project = models.ForeignKey(
        BusinessSystemProject,
        on_delete=models.CASCADE,
        related_name="monthly_metrics"
    )
    date = models.DateTimeField(null=True, blank=True)
    date_final = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    almacenamiento_gb = models.FloatField(null=True, blank=True)
    procesamiento_millicore = models.FloatField(null=True, blank=True)
    memoria_gb = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["date"]

    @property
    def total_hours(self):
        if not self.date or not self.date_final:
            return 0
        delta = self.date_final - self.date
        return round(delta.total_seconds() / 3600, 2)

    def __str__(self):
        return f"{self.project.name} - {self.date}"





from django.db import models


class BusinessProcess(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='processes'
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    numero_maximo_procesos = models.IntegerField(default=1)

    # ✅ Consumo de recursos
    memory_consumption = models.FloatField("Consumo de memoria (MB)", default=0)
    cpu_consumption = models.FloatField("Consumo de procesamiento (Cores)", default=0)
    storage_consumption = models.FloatField("Consumo de almacenamiento (GB)", default=0)

    # ✅ Recursos disponibles
    total_memory_available = models.FloatField("Memoria total disponible (MB)", default=1024)
    total_cpu_available = models.FloatField("Procesamiento total disponible (Cores)", default=8)
    total_storage_available = models.FloatField("Almacenamiento total disponible (GB)", default=8)

    # ✅ Porcentajes
    memory_percent_used = models.FloatField("Porcentaje de memoria usada (%)", editable=False, default=0)
    cpu_percent_used = models.FloatField("Porcentaje de CPU usada (%)", editable=False, default=0)
    storage_percent_used = models.FloatField("Porcentaje de almacenamiento usado (%)", editable=False, default=0)

    # ✅ Tipos
    PROCESS_TYPE_CHOICES = [
        ('Administrativo', 'Administrativo'),
        ('Financiero', 'Financiero'),
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Ventas', 'Ventas'),
        ('Marketing', 'Marketing'),
        ('Operaciones', 'Operaciones'),
        ('Cadena de Suministros', 'Cadena de Suministros'),
        ('Productos y Servicios', 'Productos y Servicios'),
    ]

    process_type = models.CharField(
        "Tipo de proceso",
        max_length=32,
        choices=PROCESS_TYPE_CHOICES,
        blank=True,
        null=True
    )

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    has_automation = models.BooleanField(default=False)
    automation_description = models.TextField(blank=True, null=True)

    has_ai = models.BooleanField(default=False)
    ai_model_description = models.TextField(
        blank=True,
        null=True,
        help_text="Describe el modelo de IA y su implementación en el proceso"
    )

    # ✅ 🔥 CORREGIDO (sin error de carga)
    assigned_developer = models.ForeignKey(
        'usuarios.SmartQuailCrew',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_processes',
        verbose_name="Desarrollador asignado"
    )

    # ✅ Fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)

    total_development_days = models.PositiveIntegerField(
        "Días de desarrollo",
        null=True,
        blank=True,
        editable=False
    )

    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    # ✅ Clasificación
    process_class = models.CharField(
        "Clase del proceso",
        max_length=20,
        choices=[('Investigación', 'Investigación'), ('Desarrollo', 'Desarrollo')],
        blank=True,
        null=True
    )

    technology_type = models.CharField(
        "Tipo de Tecnología",
        max_length=60,
        choices=[('frontend', 'Frontend'), ('backend', 'Backend')],
        blank=True,
        null=True,
    )

    process_event = models.CharField(
        "Evento del proceso",
        max_length=120,
        choices=[
            ('Entrevistas', 'Entrevistas'),
            ('Implementación SmartBusinessAnalytics®-ERP', 'Implementación SmartBusinessAnalytics®-ERP'),
            ('Implementación SmartBusinessMedia®-CRM', 'Implementación SmartBusinessMedia®-CRM'),
            ('Desarrollo Interfase UI/UX', 'Desarrollo Interfase UI/UX'),
            ('Desarrollo de Arquitectura', 'Desarrollo de Arquitectura'),
        ],
        blank=True,
        null=True
    )

    final_url = models.URLField("URL final", blank=True, null=True)

    def save(self, *args, **kwargs):

        # ✅ Días de desarrollo
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = max(delta.days, 0)
        else:
            self.total_development_days = None

        # ✅ % memoria
        self.memory_percent_used = (
            round((self.memory_consumption / self.total_memory_available) * 100, 2)
            if self.total_memory_available > 0 else 0
        )

        # ✅ % CPU
        self.cpu_percent_used = (
            round((self.cpu_consumption / self.total_cpu_available) * 100, 2)
            if self.total_cpu_available > 0 else 0
        )

        # ✅ % almacenamiento
        self.storage_percent_used = (
            round((self.storage_consumption / self.total_storage_available) * 100, 2)
            if self.total_storage_available > 0 else 0
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.project.name} I+D"



class BusinessAutomation(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='automations'
    )

    # Información general
    name = models.CharField(max_length=200)
    title = models.CharField("Título de la automatización", max_length=200, null=True, blank=True)
    description = models.TextField("Descripción de la automatización")

    progress = models.IntegerField("Progreso (%)", help_text="Valor entre 0 y 100")

    # Categorías generales de automatización
    AUTOMATION_CATEGORY_CHOICES = [
        ('communication', 'Automatización de comunicación'),
        ('workflow', 'Flujos de trabajo'),
        ('integration', 'Integraciones entre sistemas'),
        ('monitoring', 'Monitoreo y alertas'),
        ('security', 'Seguridad y autenticación'),
        ('data_ops', 'Operaciones de datos'),
        ('business_ops', 'Operaciones de negocio'),
        ('etl', 'Pipelines ETL'),
    ]

    automation_category = models.CharField(
        "Categoría de automatización",
        max_length=40,
        choices=AUTOMATION_CATEGORY_CHOICES,
        blank=True,
        null=True
    )

    # Tipos de automatización
    AUTOMATION_TYPE_CHOICES = [
        ('email_auto', 'Envío automático de emails'),
        ('sms_auto', 'Envío automático de SMS'),
        ('whatsapp_bot', 'Bot automatizado de WhatsApp'),
        ('push_notifications', 'Notificaciones push'),
        ('email_marketing', 'Email marketing'),
        ('task_automation', 'Automatización de tareas'),
        ('approval_workflow', 'Flujos de aprobación'),
        ('document_workflow', 'Flujos de documentos'),
        ('cron_job', 'Tareas programadas'),
        ('user_onboarding', 'Onboarding de usuarios'),
        ('api_sync', 'Sincronización con APIs'),
        ('crm_sync', 'Integración con CRM'),
        ('erp_sync', 'Integración con ERP'),
        ('webhook_forward', 'Enrutamiento de webhooks'),
        ('slack_integration', 'Integración con Slack'),
        ('teams_integration', 'Integración con Teams'),
        ('uptime_monitor', 'Monitoreo de disponibilidad'),
        ('error_alerts', 'Alertas de errores'),
        ('system_logs', 'Procesamiento de logs'),
        ('two_factor_flow', 'Flujos 2FA'),
        ('data_import', 'Importación de datos'),
        ('data_export', 'Exportación de datos'),
        ('db_backup', 'Backups automáticos'),
        ('csv_processing', 'Procesamiento de CSV/Excel'),
        ('pipeline_etl', 'ETL Pipelines'),
        ('data_cleaning', 'Limpieza de datos'),
        ('invoice_automation', 'Automatización de facturación'),
        ('inventory_update', 'Actualización de inventario'),
        ('order_processing', 'Procesamiento de pedidos'),
        ('contract_generation', 'Generación automática de documentos'),
        ('reminders', 'Recordatorios automáticos'),
    ]

    automation_type = models.CharField(
        "Tipo de automatización",
        max_length=50,
        choices=AUTOMATION_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # 🔥 Microservicios ampliados
    MICROSERVICE_TYPE_CHOICES = [
        ('django_task', 'Microservicio Django / Celery'),
        ('n8n', 'Workflow n8n'),
        ('rabbitmq', 'Colas RabbitMQ'),
        ('redis_queue', 'Redis Queue / Pub-Sub'),
        ('kafka', 'Apache Kafka — Streaming de datos'),
        ('elasticsearch', 'Elasticsearch — Logs y monitoreo'),
        ('logstash', 'Logstash — Procesamiento de logs'),
        ('kibana', 'Kibana — Dashboards'),
        ('postfix', 'Postfix — Servidor SMTP'),
        ('dovecot', 'Dovecot — Servidor IMAP'),
        ('cron_service', 'Sistema de cron / scheduler'),
        ('external_api', 'Microservicio de automatización externo'),
        ('standalone_service', 'Servicio independiente'),
        ('hybrid', 'Híbrido Django + n8n + colas'),
    ]

    microservice_type = models.CharField(
        "Microservicio utilizado",
        max_length=40,
        choices=MICROSERVICE_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # Asignación de desarrollador
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_automations',
        verbose_name="Desarrollador asignado"
    )

    # Tipo de integración a terceros
    INTEGRATION_TYPE_CHOICES = [
        ('gov_api', 'APIs gubernamentales'),
        ('social_media', 'Redes sociales'),
        ('electronic_billing', 'Facturación electrónica'),
        ('contract_certification', 'Certificación de contratos'),
    ]

    integration_type = models.CharField(
        "Tipo de integración a terceros",
        max_length=50,
        choices=INTEGRATION_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # Fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)
    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)
    final_url = models.URLField("URL final", blank=True, null=True)

    total_development_days = models.PositiveIntegerField(
        "Días de desarrollo",
        null=True, blank=True,
        editable=False
    )

    def save(self, *args, **kwargs):
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = max(delta.days, 0)
        else:
            self.total_development_days = None

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.project.name}"



from datetime import date

class BusinessIntelligent(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='intelligents'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    # Tipos de inteligencia artificial
    AI_TYPE_CHOICES = [

    # -----------------------------
    # 🔵 MODELOS SUPERVISADOS (scikit-learn, TensorFlow, Keras)
    # -----------------------------
    ('binary_classification', 'Clasificación Binaria (scikit-learn / TF / Keras)'),
    ('multiclass_classification', 'Clasificación Multiclase'),
    ('regression', 'Regresión Numérica'),
    ('logistic_regression', 'Regresión Logística'),
    ('svm_classifier', 'Clasificador SVM'),
    ('random_forest', 'Bosque Aleatorio'),
    ('gradient_boosting', 'Gradient Boosting (XGBoost / LightGBM)'),


    # -----------------------------
    # 🟣 MODELOS NO SUPERVISADOS (scikit-learn)
    # -----------------------------
    ('clustering', 'Clustering (K-Means / DBSCAN / GMM)'),
    ('dimensionality_reduction', 'Reducción de Dimensionalidad (PCA / t-SNE)'),
    ('anomaly_detection', 'Detección de Anomalías (Isolation Forest)'),


    # -----------------------------
    # 🟠 DEEP LEARNING (TensorFlow / Keras)
    # -----------------------------
    ('cnn', 'Redes Convolucionales (CNN)'),
    ('rnn', 'Redes Recurrentes (RNN / LSTM / GRU)'),
    ('transformer_custom', 'Transformers personalizados'),
    ('autoencoders', 'Autoencoders para compresión / detección de anomalías'),
    ('gan', 'Generative Adversarial Networks (GAN)'),


    # -----------------------------
    # 🟢 MODELOS DE SERIE TEMPORAL
    # -----------------------------
    ('time_series', 'Predicción de Series Temporales (LSTM / Prophet / ARIMA)'),


    # -----------------------------
    # 🔤 NLP (scikit-learn, TensorFlow, Keras, Gemini)
    # -----------------------------
    ('nlp', 'Procesamiento de Lenguaje Natural'),
    ('text_classification', 'Clasificación de Texto'),
    ('sentiment_analysis', 'Análisis de Sentimiento'),
    ('topic_modeling', 'Modelado de Temas (LDA)'),
    ('text_generation', 'Generación de Texto (Transformers / Gemini)'),
    ('named_entity_recognition', 'NER - Reconocimiento de Entidades'),
    ('embedding_models', 'Modelos de Embeddings (Word2Vec / BERT / Gemini)'),


    # -----------------------------
    # 🖼️ VISIÓN POR COMPUTADOR (TensorFlow / Keras)
    # -----------------------------
    ('image_recognition', 'Reconocimiento de Imágenes'),
    ('object_detection', 'Detección de Objetos (YOLO / EfficientDet)'),
    ('image_segmentation', 'Segmentación de Imágenes (UNet)'),
    ('ocr', 'OCR Inteligente (Tesseract / Vision AI)'),


    # -----------------------------
    # 🧠 RECOMMENDER SYSTEMS
    # -----------------------------
    ('recommendation', 'Sistema de Recomendación (ML / Deep Learning)'),
    ('content_based_filtering', 'Recomendación por Contenido'),
    ('collaborative_filtering', 'Filtering Colaborativo'),
    ('hybrid_recommender', 'Sistema de Recomendación Híbrido'),


    # -----------------------------
    # 🟡 REINFORCEMENT LEARNING (TensorFlow/keras-rl)
    # -----------------------------
    ('reinforcement_learning', 'Reinforcement Learning'),
    ('q_learning', 'Q-Learning'),
    ('policy_gradient', 'Policy Gradient'),
    ('ddpg', 'Deep Deterministic Policy Gradient'),


    # -----------------------------
    # 🔴 AGENTES INTELIGENTES (Gemini / LLMs)
    # -----------------------------
    ('chatbot_agent', 'Agente Conversacional (Gemini / LLMs)'),
    ('autonomous_agent', 'Agente Autónomo (Planificación + Acción)'),
    ('decision_agent', 'Agente de Toma de Decisiones'),
    ('documentation_agent', 'Agente Generador de Documentación Técnica'),
    ('data_analysis_agent', 'Agente Analítico de Datos'),
    ('code_generation_agent', 'Agente Generador de Código (Gemini Code)'),
    ('integration_agent', 'Agente Integrador con APIs externas'),
    ('workflow_agent', 'Agente que ejecuta flujos completos de trabajo'),
    ('customer_support_agent', 'Agente de Atención al Cliente'),
    ('business_intelligence_agent', 'Agente de Inteligencia de Negocio'),


    # -----------------------------
    # 🟤 MODELOS PARA AUDIO
    # -----------------------------
    ('audio_classification', 'Clasificación de Audio'),
    ('speech_to_text', 'Speech-to-Text (Gemini Audio)'),
    ('text_to_speech', 'Text-to-Speech (TTS)'),


    # -----------------------------
    # ⚫ OTROS MODELOS AVANZADOS
    # -----------------------------
    ('graph_neural_network', 'Graph Neural Networks (GNN)'),
    ('probabilistic_models', 'Modelos Probabilísticos (Bayesianos)'),
    ('large_language_model', 'Fine-Tuning de LLMs (Gemini Finetuning Tool)'),


    # -----------------------------
    # ⚙️ SISTEMAS HÍBRIDOS / INDUSTRIA
    # -----------------------------
    ('predictive_maintenance', 'Mantenimiento Predictivo'),
    ('fraud_detection', 'Detección de Fraude'),
    ('pricing_optimization', 'Optimización de Precios'),
    ('inventory_forecasting', 'Predicción de Inventarios'),
    ]

    ai_type = models.CharField(
        "Tipo de Inteligencia Artificial",
        max_length=30,
        choices=AI_TYPE_CHOICES,
        blank=True,
        null=True
    )

    requires_gpu = models.BooleanField(
        "¿Requiere GPU?",
        default=False,
        help_text="Indica si el proyecto necesita procesamiento con GPU"
    )

    # Datos técnicos del modelo
    model_accuracy = models.DecimalField(
        "Precisión del modelo (%)",
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Precisión o métrica relevante del modelo"
    )
    decision_maps = models.TextField(
        "Mapas de decisión / diagramas",
        blank=True,
        null=True,
        help_text="Descripción o links a mapas de decisión, diagramas de árbol, u otras visualizaciones"
    )
    technical_notes = models.TextField(
        "Notas técnicas adicionales",
        blank=True,
        null=True,
        help_text="Información técnica para garantizar la escalabilidad y confiabilidad del modelo"
    )

    # 👤 Desarrollador asignado
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_intelligences',
        verbose_name="Desarrollador asignado"
    )

    # 📅 Fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)

    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    final_url = models.URLField("URL final", blank=True, null=True)

    # 🕓 Cálculo de duración
    total_development_days = models.PositiveIntegerField(
        "Días de desarrollo", null=True, blank=True, editable=False
    )

    def save(self, *args, **kwargs):
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = delta.days if delta.days >= 0 else 0
        else:
            self.total_development_days = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.project.name}"



class QATest(models.Model):
    process = models.ForeignKey(BusinessProcess, on_delete=models.CASCADE, related_name='qa_tests')
    max_users = models.IntegerField(default=1)
    date_reviewed = models.DateField(null=True, blank=True)
    storage_used_gb = models.FloatField(help_text="Almacenamiento usado en GB",null=True,blank=True)
    vCPUs_used = models.IntegerField(help_text="vCPUs usadas milicore",null=True,blank=True)
    ram_used_gb = models.FloatField(help_text="RAM usada en GB",null=True,blank=True)
    GPUs_used = models.CharField(max_length=100, help_text="GPUs usadas milicore",null=True,blank=True)
    TPUs_used = models.CharField(max_length=100, help_text="Tensor usadas milicore",null=True,blank=True)
    update_resources_used_pocentage = models.FloatField(help_text="Porcentaje de uso de recursos durante la prueba",null=True,blank=True)
    latency_ms = models.FloatField(help_text="Latencia en milisegundos",null=True,blank=True)
    uptime_percentage = models.FloatField(help_text="Porcentaje de tiempo activo durante la prueba",null=True,blank=True)
    SERVER_CHOICE = [
        ('dedicated', 'Servidor privado Dedicado'),
        ('shared', 'Servidor hibrido Compartido'),
        ('cloud', 'Servidor público en la Nube'),
    ]
    server_type = models.CharField(max_length=20, choices=SERVER_CHOICE, help_text="Tipo de servidor utilizado",null=True,blank=True)
    sketch_notes_stores = models.CharField(max_length=255, help_text="Cronograma de backups DataBase",null=True,blank=True)
    test_case = models.CharField(max_length=255,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    result = models.CharField(max_length=50, choices=[('passed', 'Aprobado'), ('failed', 'Fallido'), ('pending', 'Pendiente')])
    executed_at = models.DateTimeField(auto_now_add=True, null=True,blank=True,editable=False)
    executed_by = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.test_case} - {self.result}"


class CloudResource(models.Model):
    project = models.ForeignKey(BusinessSystemProject, on_delete=models.CASCADE, related_name='cloud_resources')

    RESOURCE_TYPES = [
        ('compute', 'Compute (VM, EC2, etc.)'),
        ('storage', 'Almacenamiento'),
        ('database', 'Base de Datos'),
        ('network', 'Red'),
        ('other', 'Otro'),
    ]

    storage_used_gb = models.FloatField(help_text="Almacenamiento usado en GB",null=True,blank=True)
    vCPUs_used = models.IntegerField(help_text="vCPUs usadas milicore",null=True,blank=True)
    ram_used_gb = models.FloatField(help_text="RAM usada en GB",null=True,blank=True)
    GPUs_used = models.CharField(max_length=100, help_text="GPUs usadas milicore",null=True,blank=True)
    TPUs_used = models.CharField(max_length=100, help_text="Tensor usadas milicore",null=True,blank=True)
    update_resources_used_pocentage = models.FloatField(help_text="Porcentaje de uso de recursos durante la prueba final",null=True,blank=True)

    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPES)
    provider = models.CharField(max_length=100)  # Ej: AWS, GCP, Azure
    resource_name = models.CharField(max_length=100)
    monthly_cost_usd = models.DecimalField(max_digits=10, decimal_places=2)

    monitoring_tool = models.CharField(max_length=100, blank=True, null=True)
    monitoring_status = models.CharField(max_length=50, choices=[('healthy', 'Operativo'), ('warning', 'Advertencia'), ('critical', 'Crítico')], default='healthy')
    alert_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.resource_name} ({self.provider})"


# models.py
from django.db import models

class BusinessContracts(models.Model):
        project = models.ForeignKey(
            'BusinessSystemProject',
            on_delete=models.CASCADE,
            related_name='contracts'
        )
        # Tipos de contrato
        CONTRACT_TYPE_CHOICES = [
            ("ip", "Contrato de Propiedad Intelectual"),
            ("cloud_services", "Contrato de Servicios de Nube"),
            ("development", "Contrato de Desarrollo e Implementación de Procesos"),
        ]

        titulo = models.CharField(max_length=255, verbose_name="Título del Contrato")
        tipo = models.CharField(max_length=50, choices=CONTRACT_TYPE_CHOICES, verbose_name="Tipo de Contrato")
        archivo = models.FileField(upload_to="contracts/", verbose_name="Archivo del Contrato")

        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.titulo} ({self.get_tipo_display()})"


from django.db import models
from django.utils import timezone
from datetime import timedelta
from saas_shop.models import Product
from django.db import models
from django.conf import settings
from django.utils import timezone

class PaymentOrder(models.Model):
    # Tipos de servicio
    SERVICE_TYPE_CHOICES = [
        ("cloud_services", "Servicios de Nube"),
        ("consulting_ticket", "Ticket de Consulta"),
        ("strategic_agreement", "Convenio Estratégico"),
        ("infrastructure", "Infraestructura"),
        ("monitoring", "Monitoreo"),
        ("security_support", "Seguridad y Soporte"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_orders',
        verbose_name='Usuario',
        null=True,
        blank=True,
    )

    productos = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Producto asociado'
    )

    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        verbose_name='Proyecto asociado',
        null=True,
        blank=True
    )

    # Información de la empresa
    company_name = models.CharField(max_length=255, verbose_name="Nombre de la Empresa")
    company_ruc = models.CharField(max_length=20, verbose_name="RUC")

    # Información de la orden
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, verbose_name="Tipo de Servicio")
    cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Costo")
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="IVA (%)")
    date_issued = models.DateField(default=timezone.now, verbose_name="Fecha de Emisión")
    expiration_date = models.DateField(verbose_name="Fecha de Expiración")
    pago_verificado = models.BooleanField(default=False, verbose_name="¿Pago Verificado en Bancos?")

    # Nuevos campos para facturación
    invoice_number = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Número de Serie de Factura"
    )
    invoice_file = models.FileField(
        upload_to='invoices/',
        null=True,
        blank=True,
        verbose_name="Archivo de Factura"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = "Orden de Pago"
        verbose_name_plural = "Órdenes de Pago"

    def __str__(self):
        return f"{self.company_name} - {self.get_service_type_display()}"

    # ------------------------
    # MÉTODOS ÚTILES
    # ------------------------

    @property
    def cost_with_iva(self):
        if self.cost is None or self.iva is None:
            return 0
        return self.cost + self.iva

    @property
    def hourly_cost(self):
        if self.cost is None:
            return 0
        return self.cost / 720

    @property
    def second_expiration_date(self):
        if not self.expiration_date:
            return None
        return self.expiration_date + timedelta(days=15)

    def get_name(self):
        return f"Orden #{self.id} - {self.company_name}"

    def get_price(self):
        return self.cost_with_iva

    def get_absolute_url(self):
        return reverse(
            "paymentorder_detail",
            args=[self.id]
        )


    def save(self, *args, **kwargs):
        """Si no se define expiration_date, se asigna automáticamente 30 días desde la emisión"""
        if not self.expiration_date:
            self.expiration_date = self.date_issued + timedelta(days=30)
        super().save(*args, **kwargs)




from django.db import models
from django.utils.text import slugify


class CategoriaNoticia(models.Model):

    ITC = 'ITC'
    ID = 'ID'
    AUTOMATIZACION = 'AUT'
    IA = 'IA'
    SEGURIDAD = 'SAFE'
    MONITORING = 'monitoring'
    PRIVACIDAD = 'privacidad'

    CATEGORIA_CHOICES = [
        (ITC, 'Tecnologías de Información y Comunicación en la Nube'),
        (ID, 'Investigación y Desarrollo'),
        (AUTOMATIZACION, 'Automatización de Procesos de Información'),
        (IA, 'Inteligencia Artificial y Machine Learning'),
        (SEGURIDAD, 'Seguridad'),
        (MONITORING, 'monitoring'),
        (PRIVACIDAD, 'privacidad'),
    ]

    nombre = models.CharField(
        max_length=10,
        choices=CATEGORIA_CHOICES,
        unique=True
    )

    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True
    )

    activa = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoría de Noticia'
        verbose_name_plural = 'Categorías de Noticias'
        ordering = ['nombre']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.get_nombre_display())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_nombre_display()



from django.db import models

class Noticia(models.Model):

    categoria = models.ForeignKey(
        CategoriaNoticia,
        on_delete=models.SET_NULL,
        null=True,
        related_name='noticias'
    )
    # =========================
    # IMÁGENES
    # =========================
    imagen_portada = models.ImageField(
        upload_to='noticias/portadas/',
        blank=True,
        null=True
    )

    imagen_comercial = models.ImageField(
        upload_to='noticias/comercial/',
        blank=True,
        null=True
    )

    imagen_datos_estadisticos = models.ImageField(
        upload_to='noticias/estadisticas/',
        blank=True,
        null=True
    )

    imagen_informativo = models.ImageField(
        upload_to='noticias/informativo/',
        blank=True,
        null=True
    )

    # =========================
    # TÍTULOS
    # =========================
    titulo_1 = models.CharField(max_length=255)
    titulo_2 = models.CharField(max_length=255, blank=True, null=True)
    titulo_3 = models.CharField(max_length=255, blank=True, null=True)

    # =========================
    # SUBTÍTULOS
    # =========================
    subtitulo_1 = models.CharField(max_length=255, blank=True, null=True)
    subtitulo_2 = models.CharField(max_length=255, blank=True, null=True)
    subtitulo_3 = models.CharField(max_length=255, blank=True, null=True)
    subtitulo_4 = models.CharField(max_length=255, blank=True, null=True)
    subtitulo_5 = models.CharField(max_length=255, blank=True, null=True)
    subtitulo_6 = models.CharField(max_length=255, blank=True, null=True)

    # =========================
    # CUERPOS DE TEXTO
    # =========================
    cuerpo_1 = models.TextField()
    cuerpo_2 = models.TextField(blank=True, null=True)
    cuerpo_3 = models.TextField(blank=True, null=True)
    cuerpo_4 = models.TextField(blank=True, null=True)
    cuerpo_5 = models.TextField(blank=True, null=True)
    cuerpo_6 = models.TextField(blank=True, null=True)
    cuerpo_7 = models.TextField(blank=True, null=True)
    cuerpo_8 = models.TextField(blank=True, null=True)
    cuerpo_9 = models.TextField(blank=True, null=True)

    # =========================
    # AUTOR
    # =========================
    autor_nombre = models.CharField(max_length=150)
    autor_bio = models.TextField(blank=True, null=True)
    autor_email = models.EmailField(blank=True, null=True)
    autor_foto = models.ImageField(
        upload_to='noticias/autores/',
        blank=True,
        null=True
    )

    refencia_1 = models.CharField(max_length=150,null=True, blank=True)
    refencia_2 = models.CharField(max_length=150,null=True, blank=True)
    refencia_3 = models.CharField(max_length=150,null=True, blank=True)
    refencia_4 = models.CharField(max_length=150,null=True, blank=True)
    # =========================
    # METADATOS
    # =========================
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return self.titulo_1


from django.db import models
from django.conf import settings

class ComentarioNoticia(models.Model):
    noticia = models.ForeignKey(
        Noticia,
        on_delete=models.CASCADE,
        related_name='comentarios'
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    comentario = models.TextField()

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'Comentario de {self.usuario} en {self.noticia}'


from django.db import models
from django.utils import timezone


class NoticiaMetricas(models.Model):
    noticia = models.OneToOneField(
        'Noticia',
        on_delete=models.CASCADE,
        related_name='metricas'
    )

    # =========================
    # MÉTRICAS
    # =========================
    likes = models.PositiveIntegerField(default=0)
    compartidos_redes = models.PositiveIntegerField(default=0)
    compartidos_email = models.PositiveIntegerField(default=0)
    descargas = models.PositiveIntegerField(default=0)

    # =========================
    # METADATOS
    # =========================
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Métricas - {self.noticia.titulo_1}"







from django.conf import settings
from django.db import models


class ConsultationType(models.Model):
    """
    Tipos de consulta disponibles
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    has_cost = models.BooleanField(default=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.name} - {'Con costo' if self.has_cost else 'Sin costo'}"


class ConsultationQuestion(models.Model):
    """
    Preguntas sugeridas según el área de consulta
    """
    AREA_CHOICES = [
        ('cloud', 'Computación en la nube'),
        ('courses', 'Talleres y cursos de arquitectura cloud'),
        ('design', 'Diseño de soluciones'),
        ('security', 'Respaldo y seguridad'),
        ('ai', 'Inteligencia Artificial'),
        ('ml', 'Machine Learning'),
    ]

    area = models.CharField(max_length=20, choices=AREA_CHOICES)
    question = models.TextField()

    def __str__(self):
        return f"[{self.get_area_display()}] {self.question[:50]}"



from django.conf import settings
from django.db import models


class SupportTicket(models.Model):

    # =========================
    # TIPO DE CONSULTA
    # =========================
    CONSULTATION_TYPE_CHOICES = [
        ('cloud_free', 'Consulta sobre tecnologías cloud (Sin costo)'),
        ('courses_free', 'Consultas sobre talleres y cursos cloud (Sin costo)'),
        ('design_paid', 'Diseño de arquitecturas cloud (Con costo)'),
        ('security_paid', 'Respaldo y seguridad (Con costo)'),
        ('ai_paid', 'Inteligencia Artificial (Con costo)'),
        ('ml_paid', 'Machine Learning (Con costo)'),
    ]

    # =========================
    # ÁREA
    # =========================
    AREA_CHOICES = [
        ('cloud', 'Computación en la nube'),
        ('courses', 'Talleres y cursos'),
        ('design', 'Diseño de soluciones'),
        ('security', 'Respaldo y seguridad'),
        ('ai', 'Inteligencia Artificial'),
        ('ml', 'Machine Learning'),
    ]

    # =========================
    # PREGUNTAS FRECUENTES
    # =========================
    QUESTION_CHOICES = [
        # CLOUD
        ('q_cloud_1', '¿Qué proveedor de nube es más conveniente según mi presupuesto?'),
        ('q_cloud_2', '¿Cómo migrar una aplicación local a la nube?'),
        ('q_cloud_3', '¿Qué diferencia hay entre IaaS, PaaS y SaaS?'),
        ('q_cloud_4', '¿Cómo escalar automáticamente una aplicación en la nube?'),
        ('q_cloud_5', '¿Cómo reducir costos en infraestructura cloud?'),
        ('q_cloud_6', '¿Qué región de nube debo elegir y por qué?'),

        # CURSOS
        ('q_course_1', '¿Qué conocimientos previos necesito para tomar un curso de arquitectura cloud?'),
        ('q_course_2', '¿Los talleres incluyen prácticas reales?'),
        ('q_course_3', '¿Qué certificaciones cloud recomiendan después del curso?'),
        ('q_course_4', '¿Los cursos están orientados a AWS, Azure o Google Cloud?'),
        ('q_course_5', '¿Se entregan materiales o grabaciones de las sesiones?'),
        ('q_course_6', '¿Los cursos sirven para certificaciones oficiales?'),

        # DISEÑO
        ('q_design_1', '¿Cómo diseñar una arquitectura altamente disponible?'),
        ('q_design_2', '¿Qué patrón de arquitectura es adecuado para mi aplicación?'),
        ('q_design_3', '¿Cómo implementar balanceo de carga y alta disponibilidad?'),
        ('q_design_4', '¿Cómo diseñar una solución cloud segura y escalable?'),

        # SEGURIDAD
        ('q_security_1', '¿Cómo implementar un plan de respaldo y recuperación ante desastres?'),
        ('q_security_2', '¿Cómo proteger datos sensibles en la nube?'),
        ('q_security_3', '¿Cómo cifrar datos en tránsito y en reposo?'),
        ('q_security_4', '¿Cómo detectar y responder a incidentes de seguridad?'),

        # IA
        ('q_ai_1', '¿Cómo aplicar inteligencia artificial a mi negocio?'),
        ('q_ai_2', '¿Qué datos necesito para implementar un sistema de IA?'),
        ('q_ai_3', '¿Qué servicios cloud ofrecen IA preentrenada?'),

        # ML
        ('q_ml_1', '¿Qué diferencia hay entre IA y Machine Learning?'),
        ('q_ml_2', '¿Cómo entrenar un modelo de machine learning en la nube?'),
        ('q_ml_3', '¿Cómo desplegar un modelo de ML en producción?'),
    ]

    # =========================
    # ESTADO DEL TICKET
    # =========================
    STATUS_CHOICES = [
        ('active', 'Activo'),
        ('finished', 'Terminado'),
    ]

    # =========================
    # CAMPOS
    # =========================
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    consultation_type = models.CharField(
        max_length=30,
        choices=CONSULTATION_TYPE_CHOICES
    )

    area = models.CharField(
        max_length=20,
        choices=AREA_CHOICES
    )

    question = models.CharField(
        max_length=20,
        choices=QUESTION_CHOICES
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    scheduled_datetime = models.DateTimeField(
        help_text="Fecha y hora seleccionada por el usuario para la consulta"
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.get_status_display()}"
