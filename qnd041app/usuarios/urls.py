from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


from django.urls import path
from . import views

urlpatterns = [
    # otras rutas...
    
]



app_name = 'usuarios'

urlpatterns = [
    # previous login view
    
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar_cuenta'),
    
    path('dashboard', views.dashboard, name='dashboard'),
    path("dashboard/micro/", views.dashboard_micro, name="dashboard_micro"),
    path("dashboard/pequena/", views.dashboard_pequena, name="dashboard_pequena"),
    path("dashboard/mediana/", views.dashboard_mediana, name="dashboard_mediana"),
    path("dashboard/enterprise/", views.dashboard_enterprise, name="dashboard_enterprise"),

    path(
        'politicas-terminos/',
        views.politicas_terminos,
        name='politicas_terminos'
    ),

    path("preview/login-email/", views.preview_login_notification_email, name="preview_login_email"),
    path("preview/email/password-reset/", views.preview_password_reset_email, name="preview_password_reset_email"),
    path('preview/activation-email/', views.preview_account_activation_email, name='preview_activation_email'),



    path('recuperar/', views.password_reset_request, name='password_reset_request'),
    path('restablecer/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
     
  
    path('perfil_de_usuario/', views.profile_edit_view , name='perfil'),

    path('Citas/', views.gestionar_citas_view, name='citas'),
    path('citas/<int:cita_id>/cancelar/', views.cancelar_cita_view, name='cancelar_cita'),
    path('citas/<int:cita_id>/editar/', views.editar_cita_view, name='editar_cita'),

    path('citas/nueva/', views.agendar_cita, name='agendar_cita'),
    path('citas/success/', views.cita_success, name='cita_success'),  

    path('calendario/', views.citas_agendadas_total , name='citas_total'),
    path('calendario_total/', views.citas_record , name='citas_record'),
    path('citas/ver/<int:pk>/', views.ver_cita, name='ver_cita'),
    path('cita/<int:pk>/confirmar/', views.confirmar_cita, name='confirmar_cita'),
    path('cita/<int:pk>/cancelar/', views.cancelar_cita, name='cancelar_cita'),


    path('tareas/nuevas/', views.tareas_list, name='lista_tareas'),
    path('tareas/asignadas/', views.tareas_asignadas, name='tareas_asignadas'),
    path('tareas/realizadas/', views.tareas_realizadas, name='tareas_realizadas'),
    path('tareas/<int:pk>/marcar_realizada/', views.marcar_tarea_realizada, name='marcar_tarea_realizada'),


    path('tarea/<int:pk>/', views.ver_tarea, name='ver_tarea'),
    path('tarea/<int:pk>/interactiva/', views.ver_tarea_interactiva, name='ver_tarea_interactiva'),

    path('pagos/', views.lista_pagos, name='lista_pagos'),
    path('pagos/pendientes/', views.pagos_pendientes_view, name='pagos_pendientes'),
    path('pagos/adeudados/', views.pagos_vencidos_view, name='pagos_vencidos'),

    path('pagos/<int:pk>/', views.ver_pago, name='ver_pago'),
    path('pagos/<int:pk>/subir-comprobante/', views.subir_comprobante_pago, name='subir_comprobante_pago'),

    path('certificados/', views.vista_certificados, name='vista_certificados'),



    path('inbox/', views.inbox_view , name='inbox'),
    path('inbox_total/', views.inbox_record , name='inbox_total'),
    path('mensajes/ver/<int:pk>/', views.ver_mensaje, name='ver_mensaje'),
    path('nuevo_mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('Confirmacion/', views.msj_success, name='success'),
    path('configuracion_de_usuario/', views.config_view , name='configuraciones'),

    path('tareas/', views.TareaListView.as_view(), name='tarea_list'),
    path('tareas/<int:pk>/', views.TareaDetailView.as_view(), name='tarea_detail'),

    path('actividades/', views.ActividadListView.as_view(), name='actividad_list'),
    path('actividades/<int:pk>/', views.ActividadDetailView.as_view(), name='actividad_detail'),

    path('terapias/', views.TerapiaListView.as_view(), name='terapia_list'),
    path('terapias/<int:pk>/', views.TerapiaDetailView.as_view(), name='terapia_detail'),

    path('asistidas/', views.CitasAsistidasListView.as_view(), name='citas_asistidas'),
    path('no-asistidas/', views.CitasNoAsistidasListView.as_view(), name='citas_no_asistidas'),
    path('pendientes/', views.CitasPendientesListView.as_view(), name='citas_pendientes'),
    path('<int:pk>/', views.CitaDetailView.as_view(), name='detalle'),

   # path('actividades_espacio_publico/', views.user_activity_login, name='login_activity'),
   # path('Reserva_de_espacio_publico/', views.user_activity_login, name='login_activity'),
  
   # path('dashboard', views.dashboard, name='dashboard'),
   # path('perfil_de_usuario/', views.profile_view , name='perfil'),
   # path('configuracion_de_usuario/', views.config_view , name='configuraciones'),
  
    # change password urls

    # alternative way to include authentication views
    # path('', include('django.contrib.auth.urls')),
   # path('registro_para_postulacion_a_convocatorias/', views.register, name='register'),
   # path('registro_para_proponer_actividades_culturales__espacios_publicos/', views.activity_register, name='activity_register'),
   # path('registro_para_uso_espacio_publico/', views.register_public, name='register_public'),
   # path('edit/', views.edit, name='edit'),
  #  path('edit_contacto_1/', views.edit_contact, name='edit_contact1'),
 #   path('edit_contacto_2/', views.edit_contact2, name='edit_contact2'),
  #  path('edit_contacto_3/', views.edit_contact3, name='edit_contact3'),
 #   path('edit_contacto_4/', views.edit_contact4, name='edit_contact4'),
  #  path('Actividad_Cultural/', views.edit_activity, name='edit_activity'),
 #   path('edit_legal1/', views.edit_legal, name='edit_legal'),
  #  path('edit_legal2/', views.edit_legal2, name='edit_legal2'),
 #   path('Declaratoria/', views.edit_declaratoria, name='edit_declaratoria'),
 #   path('confirmacion/', views.confirmacion, name='confirmacion'),
#    path('privacy/', views.privacy_policy_view , name='privacy_policy'),
#    path('terms/', views.terms_of_use_view , name='terms_of_use'),
 #   path('Activityprivacy/', views.activity_privacy_policy_view , name='activity_privacy_policy'),
#    path('Activityterms/', views.activity_terms_of_use_view , name='activity_terms_of_use'),
#    path('inicio_crear_convocatoria/', views.manual_crear_convocatoria, name='inicio_crear_convocatoria'),
#    path('inicio_editar_convocatoria/', views.manual_editar_convocatoria, name='inicio_editar_convocatoria'),
 #   path('inicio_Mis_convocatoria/', views.manual_mis_convocatoria, name='inicio_mis_convocatoria'),
 #   path('inicio_Inscripciones/', views.manual_inscripcion, name='inicio_inscripcion'),
   # path('inicio_postulacion/', views.manual_postulation, name='inicio_postulation'),  # Corrected name
 #   path('inicio_Mis_postulaciones/', views.manual_mis_postulaciones, name='inicio_mis_postulaciones'),
 #   path('inicio_crear_Proyecto/', views.manual_crear_proyecto, name='inicio_crear_proyecto'),
 #   path('inicio_editar_Proyecto/', views.manual_editar_proyecto, name='inicio_editar_proyecto'),
#    path('inicio_Mis_Proyecto/', views.manual_mis_proyectos, name='inicio_mis_proyectos'),

   # path('admin/profile/<int:profile_id>/pdf/', views.admin_profile_pdf, name='admin_profile_pdf'),
]
