from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm                    
from .models import Profile
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from pathlib import Path
from django.core.cache import cache
from .models import Dashboard


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    user_profile = Profile.objects.get(user=user)
                    return redirect('usuarios:perfil')
                else:
                    return HttpResponse('Disabled account')
            else:
                form = LoginForm()
                return render(request, 'registration/editorial_literario/login_fail.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'registration/editorial_literario/login.html', {'form': form})

@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)    
    return render(request, 'usuarios/dashboard.html', {
        'section': 'dashboard',
    })



@login_required
def profile_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/profile.html', {'profile': profile})

@login_required
def config_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/config.html', {'profile': profile})