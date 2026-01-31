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
]
