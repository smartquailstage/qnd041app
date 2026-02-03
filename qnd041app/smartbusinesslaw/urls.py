from django.urls import path
from . import views

app_name = 'smartbusinesslaw'

urlpatterns = [
    # ----------------------------
    # PDF Delegado (DPD)
    # ----------------------------
    path(
        'delegado/<int:delegado_id>/pdf/',
        views.delegado_pdf,
        name='admin_delegado_pdf'
    ),

    # ----------------------------
    # PDF RAT
    # ----------------------------
    path(
        'rat/<int:delegado_id>/pdf/',
        views.rat_pdf,
        name='admin_rat_pdf'
    ),

    # ----------------------------
    # PDF Incidentes
    # ----------------------------
    path(
        'incidente/<int:delegado_id>/pdf/',
        views.incidente_pdf,
        name='admin_incidente_pdf'
    ),

    # ----------------------------
    # PDF Regulacion / Artículos LOPDP
    # ----------------------------
    path(
        'regulacion/<int:regulacion_id>/pdf/',
        views.regulacion_pdf,
        name='admin_regulacion_pdf'
    ),


    path('scvs/<int:pk>/txt/datos_generales/', views.txt_datos_generales, name='txt_datos_generales'),
    path('scvs/<int:pk>/txt/balance_general/', views.txt_balance_general, name='txt_balance_general'),
    path('scvs/<int:pk>/txt/estado_resultados/', views.txt_estado_resultados, name='txt_estado_resultados'),
    path('scvs/<int:pk>/txt/cambios_patrimonio/', views.txt_cambios_patrimonio, name='txt_cambios_patrimonio'),
    path('scvs/<int:pk>/txt/flujo_anexos/', views.txt_flujo_anexos, name='txt_flujo_anexos'),

    path('scvs/<int:pk>/pdf/datos-generales/', views.pdf_datos_generales, name='pdf_datos_generales'),


        # ---------- PDF Balance ----------
    path('pdf/balance/<int:pk>/', views.pdf_balance, name='pdf_balance'),

    # ---------- PDF Estado de Resultados ----------
    path('pdf/estado_resultados/<int:pk>/', views.pdf_estado_resultados, name='pdf_estado_resultados'),

    # ---------- PDF Cambios en el Patrimonio ----------
    path('pdf/cambios_patrimonio/<int:pk>/', views.pdf_cambios_patrimonio, name='pdf_cambios_patrimonio'),

    # ---------- PDF Flujo de Efectivo ----------
    path('pdf/flujo_efectivo/<int:pk>/', views.pdf_flujo_efectivo, name='pdf_flujo_efectivo'),

    # ---------- PDF Anexos SCVS ----------
    path('pdf/anexos/<int:pk>/', views.pdf_anexos, name='pdf_anexos'),
]



