from django.shortcuts import render
from .forms import CostCalculatorForm
from .models import ProductCalculation

from .forms import InfrastructureForm
from .models import InfrastructureQuote

def calculate_infra_cost(infra_type, cpu, ram, storage, bandwidth):
    base = {
        'onprem': 500,     # Costo base por servidor físico
        'public': 100,     # Costo base mensual
        'hybrid': 300      # Coste intermedio
    }.get(infra_type, 100)

    cost = base
    cost += cpu * 25
    cost += ram * 15
    cost += storage * 0.5
    cost += bandwidth * 1.2

    return round(cost, 2)

def infra_calculator_view(request):
    total = None
    if request.method == 'POST':
        form = InfrastructureForm(request.POST)
        if form.is_valid():
            infra_type = form.cleaned_data['infra_type']
            cpu = form.cleaned_data['cpu_cores']
            ram = form.cleaned_data['ram_gb']
            storage = form.cleaned_data['storage_gb']
            bandwidth = form.cleaned_data['bandwidth_mbps']

            total = calculate_infra_cost(infra_type, cpu, ram, storage, bandwidth)

            # Guardar en DB
            InfrastructureQuote.objects.create(
                infra_type=infra_type,
                cpu_cores=cpu,
                ram_gb=ram,
                storage_gb=storage,
                bandwidth_mbps=bandwidth,
                estimated_cost=total
            )

            return render(request, 'infra_calculator.html', {
                'form': form,
                'total': total,
                'saved': True,
            })
    else:
        form = InfrastructureForm()
    return render(request, 'infra_calculator.html', {'form': form})
    

def calculate_total(product, rd, auto, ai, processes, data, complexity):
    base_costs = {
        'SBA': 100,
        'SBM': 80,
        'SBL': 90,
        'SBT': 120,
    }

    cost = base_costs.get(product, 100)

    if rd:
        cost += 25 * processes * complexity
    if auto:
        cost += 35 * processes
    if ai:
        cost += 150 + (data * 0.5) + (complexity * 40)

    return round(cost, 2)

def calculator_view(request):
    total_cost = None
    if request.method == 'POST':
        form = CostCalculatorForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            rd = form.cleaned_data['include_rd']
            auto = form.cleaned_data['include_automation']
            ai = form.cleaned_data['include_ai']
            processes = form.cleaned_data['num_processes']
            data = form.cleaned_data['data_volume']
            complexity = form.cleaned_data['complexity']

            total_cost = calculate_total(product, rd, auto, ai, processes, data, complexity)

            ProductCalculation.objects.create(
                product=product,
                include_rd=rd,
                include_automation=auto,
                include_ai=ai,
                num_processes=processes,
                data_volume=data,
                complexity=complexity,
                result_cost=total_cost
            )

            return render(request, 'calculator.html', {
                'form': form,
                'total_cost': total_cost,
                'saved': True,
            })
    else:
        form = CostCalculatorForm()

    return render(request, 'calculator.html', {'form': form, 'total_cost': total_cost})
