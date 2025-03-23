from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views


app_name = 'usuarios'

urlpatterns = [
    # previous login view
    path('ingresar/', views.user_login, name='login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('perfil_de_usuario/', views.profile_view , name='perfil'),
    path('configuracion_de_usuario/', views.config_view , name='configuraciones'),
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
