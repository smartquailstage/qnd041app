# views.py

from django.views.generic import ListView, DetailView
from .models import Facturation

class FacturationListView(ListView):
    model = Facturation
    template_name = 'facturation/facturation_list.html'
    context_object_name = 'facturas'
    paginate_by = 10  # Puedes ajustar o quitar la paginación

    def get_queryset(self):
        return Facturation.objects.select_related('project').prefetch_related('concept')


class FacturationDetailView(DetailView):
    model = Facturation
    template_name = 'facturation/facturation_detail.html'
    context_object_name = 'factura'