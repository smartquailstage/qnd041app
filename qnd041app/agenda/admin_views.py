# agenda/admin_views.py
from django.shortcuts import render
from .models import Cita  # Assuming you have a Cita model for appointments

def admin_cita_detail(request, cita_id):
    # Fetch the 'cita' object based on the cita_id
    cita = Cita.objects.get(id=cita_id)
    
    # Pass the cita object to the template (or return JSON, etc.)
    return render(request, "admin/cita_detail.html", {"cita": cita})
