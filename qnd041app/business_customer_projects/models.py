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
    PROCESS_TYPE_CHOICES = [
        ('Admin', 'Administrativo'),
        ('Fin', 'Financiero'),
        ('HR', 'Recursos Humanos'),
        ('Sales', 'Ventas'),
        ('Mkt', 'Marketing'),
        ('Ops', 'Operaciones'),
        ('CS','Cadena de Suministros'),
        ('PS','Productos y Servicios'),
    ]
    process_type = models.CharField("Tipo de proceso",max_length=10,choices=PROCESS_TYPE_CHOICES,blank=True,null=True)


    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    has_automation = models.BooleanField(default=False)
    automation_description = models.TextField(blank=True, null=True)

    has_ai = models.BooleanField(default=False)
    ai_model_description = models.TextField(
        blank=True, null=True,
        help_text="Describe el modelo de IA y su implementación en el proceso"
    )

    # 👤 Desarrollador asignado
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_processes',
        verbose_name="Desarrollador asignado"
    )

    # 📅 Nuevas fechas
    start_date = models.DateField("Fecha de inicio", null=True, blank=True)
    delivery_date = models.DateField("Fecha de entrega", null=True, blank=True)

    approved_by_client = models.BooleanField("¿Aprobado por cliente?", default=False)

    PROCESS_TYPE_CHOICES = [
        ('I', 'Investigación'),
        ('D', 'Desarrollo'),
    ]
    process_type = models.CharField(
        "Tipo de proceso",
        max_length=1,
        choices=PROCESS_TYPE_CHOICES,
        blank=True,
        null=True
    )

    TECHNOLOGY_TYPE_CHOICES = [
    ('frontend', 'Frontend'),
    ('backend', 'Backend'),
    ]
    
    technology_type = models.CharField(
    "Tipo de Tecnología",
    max_length=10,
    choices=TECHNOLOGY_TYPE_CHOICES,
    blank=True,
    null=True,
    )


    PROCESS_CLASS_CHOICES = [
        ('interview', 'Entrevistas'),
        ('erp_impl', 'Implementación SmartBusinessAnalytics®-ERP'),
        ('crm_impl', 'Implementación SmartBusinessMedia®-CRM'),
        ('uiux_dev', 'Desarrollo Interfase UI/UX'),
        ('architecture_dev', 'Desarrollo de Arquitectura'),
    ]
    process_class = models.CharField(
        "Clase del proceso",
        max_length=30,
        choices=PROCESS_CLASS_CHOICES,
        blank=True,
        null=True
    )

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
        return f"{self.name} - {self.project.name} I+D"





class BusinessAutomation(models.Model):
    project = models.ForeignKey(
        'BusinessSystemProject',
        on_delete=models.CASCADE,
        related_name='automations'
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()

    progress = models.IntegerField(help_text="Progreso del 0 al 100 (%)")

    # Tipos de automatización
    AUTOMATION_TYPE_CHOICES = [
        ('email', 'Email'),
        ('auto_auth', 'Autoidentificación'),
        ('report_gen', 'Generación de reportes'),
        ('chatbot', 'Chatbot para negocios'),
        ('data_sync', 'Sincronización de datos'),
        ('notification', 'Notificaciones automáticas'),
        ('workflow', 'Automatización de flujos de trabajo'),
    ]
    automation_type = models.CharField(
        "Tipo de automatización",
        max_length=20,
        choices=AUTOMATION_TYPE_CHOICES,
        blank=True,
        null=True
    )

    # 👤 Desarrollador asignado
    assigned_developer = models.ForeignKey(
        SmartQuailCrew,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_automations',
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
