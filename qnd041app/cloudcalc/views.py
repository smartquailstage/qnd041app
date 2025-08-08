from django.shortcuts import render, redirect
from .forms import EstimacionForm
from .models import Estimacion, Servicio
import random
from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal

def calcular_recursos(usuarios, tipo_uso):
    """Lógica sencilla de estimación (puedes mejorarla luego)"""
    base_vcpu = 1
    base_ram = 2
    base_storage = 50

    factor = {
        'transaccional': 1.2,
        'analitico': 1.5,
        'mixto': 1.35,
    }[tipo_uso]

    vcpu = base_vcpu + usuarios * 0.001 * factor
    ram = base_ram + usuarios * 0.002 * factor
    storage = base_storage + usuarios * 0.01

    costo = (vcpu * 10) + (ram * 5) + (storage * 0.1)

    return round(vcpu, 2), round(ram, 2), round(storage, 2), round(costo, 2)


def estimar_recursos(request):
    if request.method == 'POST':
        form = EstimacionForm(request.POST)
        if form.is_valid():
            servicio = form.cleaned_data['servicio']
            usuarios = form.cleaned_data['usuarios_estimados']
            tipo_uso = form.cleaned_data['tipo_uso']
            proveedor = form.cleaned_data['proveedor']

            # Estimaciones básicas
            vcpu = usuarios * 0.1
            ram = usuarios * 0.2
            almacenamiento = usuarios * 1.5
            costo_base = (vcpu * 10) + (ram * 5) + (almacenamiento * 0.1)

            # Sumar costo adicional del servicio
            costo_total = Decimal(costo_base) + servicio.costo_adicional

            estimacion = Estimacion.objects.create(
                servicio=servicio,
                usuarios_estimados=usuarios,
                tipo_uso=tipo_uso,
                proveedor=proveedor,
                vcpu=vcpu,
                ram_gb=ram,
                almacenamiento_gb=almacenamiento,
                costo_estimado=costo_total
            )

            return redirect('cloudcalc:resultado_estimacion', estimacion.id)
    else:
        form = EstimacionForm()

    return render(request, 'estimador/formulario.html', {'form': form})

def resultado_estimacion(request, estimacion_id):
    estimacion = Estimacion.objects.get(id=estimacion_id)
    return render(request, 'estimador/resultado.html', {'estimacion': estimacion})
