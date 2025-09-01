import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from django.template.loader import render_to_string
from unfold.components import BaseComponent, register_component
from orders.models import Order


@register_component
class OrdenesFrecuenciaComponent(BaseComponent):
    name = "Distribución de Órdenes en el Tiempo"
    template_name = "admin/order_frecuencia_chart.html"

    def __init__(self, request, instance=None):
        self.request = request
        self.instance = instance

    def get_context_data(self, **kwargs):
        # Obtener todas las fechas de creación de órdenes
        fechas = list(Order.objects.values_list("created", flat=True))

        if not fechas:
            return {
                "title": self.name,
                "grafico_base64": None,
                "mensaje": "No hay datos disponibles."
            }

        # Convertir a días
        dias = [(f.date() - min(fechas).date()).days for f in fechas]
        max_dia = max(dias) if dias else 0

        # Calcular frecuencia
        bins = np.arange(0, max_dia + 2)  # un bin por día
        frecuencia, _ = np.histogram(dias, bins=bins)

        # Graficar
        fig, ax = plt.subplots()
        ax.bar(bins[:-1], frecuencia, width=1, color='skyblue')
        ax.set_xlabel("Días desde la primera orden")
        ax.set_ylabel("Número de órdenes")
        ax.set_title("Distribución de Órdenes")

        # Convertir gráfico a base64
        buffer = io.BytesIO()
        plt.tight_layout()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        imagen_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return {
            "title": self.name,
            "grafico_base64": imagen_base64,
        }

    def render(self):
        return render_to_string(self.template_name, self.get_context_data())
