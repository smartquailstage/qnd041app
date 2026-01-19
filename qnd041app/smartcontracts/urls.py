from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _


app_name = 'smartcontracts'

urlpatterns = [

    path('admin/contrato/<int:contrato_id>', views.admin_contract_pdf, name='admin_contract_pdf'),


]