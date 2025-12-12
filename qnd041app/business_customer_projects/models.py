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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("business_customer_projects:project_detail", kwargs={"pk": self.pk})


    def save(self, *args, **kwargs):
        if self.saas_order:
            item = self.saas_order.items.first()
            if item:
                self.product = item.product
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



from usuarios.models import SmartQuailCrew  # Asegúrate de que esta importación es correcta

from django.db import models
from usuarios.models import SmartQuailCrew
from datetime import date

class BusinessProcess(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='processes'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    numero_maximo_procesos = models.IntegerField(default=1)

    # Campos de memoria y CPU
    memory_consumption = models.FloatField("Consumo de memoria (MB)", default=0)
    cpu_consumption = models.FloatField("Consumo de procesamiento (Cores)", default=0)
    total_memory_available = models.FloatField("Memoria total disponible (MB)", default=1024)
    total_cpu_available = models.FloatField("Procesamiento total disponible (Cores)", default=8)

    memory_percent_used = models.FloatField("Porcentaje de memoria usada (%)", editable=False, default=0)
    cpu_percent_used = models.FloatField("Porcentaje de CPU usada (%)", editable=False, default=0)

    # Resto de campos existentes...
    PROCESS_TYPE_CHOICES = [
        ('Administrativo', 'Administrativo'),
        ('Financiero', 'Financiero'),
        ('Recursos Humanos', 'Recursos Humanos'),
        ('Ventas', 'Ventas'),
        ('Marketing', 'Marketing'),
        ('Operaciones', 'Operaciones'),
        ('Cadena de Suministros','Cadena de Suministros'),
        ('Productos y Servicios','Productos y Servicios'),
    ]
    process_type = models.CharField("Tipo de proceso", max_length=32, choices=PROCESS_TYPE_CHOICES, blank=True, null=True)
    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")
    has_automation = models.BooleanField(default=False)
    automation_description = models.TextField(blank=True, null=True)
    has_ai = models.BooleanField(default=False)
    ai_model_description = models.TextField(blank=True, null=True, help_text="Describe el modelo de IA y su implementación en el proceso")
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_processes',
        verbose_name="Desarrollador asignado"
    )

    # Fechas y aprobación
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)
    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    process_class = models.CharField(
        "Tipo de proceso",
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
        "Clase del proceso",
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
    total_development_days = models.PositiveIntegerField("Días de desarrollo", null=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        # Calcular días de desarrollo
        if self.start_date and self.delivery_date:
            delta = self.delivery_date - self.start_date
            self.total_development_days = delta.days if delta.days >= 0 else 0
        else:
            self.total_development_days = None

        # Calcular porcentaje de uso de memoria y CPU
        if self.total_memory_available > 0:
            self.memory_percent_used = round((self.memory_consumption / self.total_memory_available) * 100, 2)
        else:
            self.memory_percent_used = 0

        if self.total_cpu_available > 0:
            self.cpu_percent_used = round((self.cpu_consumption / self.total_cpu_available) * 100, 2)
        else:
            self.cpu_percent_used = 0

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


    def save(self, *args, **kwargs):
        """Si no se define expiration_date, se asigna automáticamente 30 días desde la emisión"""
        if not self.expiration_date:
            self.expiration_date = self.date_issued + timedelta(days=30)
        super().save(*args, **kwargs)
