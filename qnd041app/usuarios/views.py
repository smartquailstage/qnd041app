from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .forms import LoginForm,UserRegistrationForm,MensajeForm,CitaForm,TareaComentarioForm               
from .models import Profile, Cita
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
import weasyprint
from django.conf import settings
from pathlib import Path
from django.core.cache import cache
from .models import Dashboard, Mensaje, InformesTerapeuticos
from django.shortcuts import render
from .models import Cita,tareas, pagos  # Asegúrate de usar la ruta correcta
from django.http import HttpResponseForbidden
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import render, redirect
# from django.contrib.auth import login  # Descomenta si vas a usar login()

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from urllib.parse import unquote
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

def activar_cuenta(request, uidb64, token):
    try:
        # Decodificar UID y limpiar token de caracteres especiales
        uid = force_str(urlsafe_base64_decode(unquote(uidb64)))
        token = unquote(token)

        # Obtener el usuario
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        logger.warning("Error al decodificar UID o buscar usuario: %s", e)
        user = None

    # Validar token y usuario
    if user is not None and default_token_generator.check_token(user, token):
        if not user.is_active:
            user.is_active = True
            user.save()
            logger.info("Usuario %s activado correctamente.", user.email)
        else:
            logger.info("Usuario %s ya estaba activo.", user.email)
        return redirect('usuarios:login')
    else:
        logger.warning("Token inválido o usuario no encontrado. uid=%s token=%s", uidb64, token)
        return render(request, 'usuarios/activation_invalid.html')



from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from usuarios.forms import UserRegistrationForm

User = get_user_model()

# usuarios/views.py
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .tasks import enviar_correo_activacion  # 👈 Importar tarea


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.is_active = False  # Se activa por correo

            # Campos adicionales
            new_user.acepta_terminos = user_form.cleaned_data.get('acepta_terminos', False)
            new_user.suscripcion_noticias = user_form.cleaned_data.get('suscripcion_noticias', False)
            new_user.save()

            # 🌐 Dominio base (para construir URL dentro de la tarea)
            domain = request.build_absolute_uri('/')[:-1]  # Quita la última barra

            # 🚀 Enviar correo de activación de forma asíncrona
            enviar_correo_activacion.delay(new_user.id, domain)

            # ✅ Mostrar mensaje final
            return render(request, 'usuarios/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()

    return render(request, 'usuarios/register.html', {'user_form': user_form})



User = get_user_model()

def preview_account_activation_email(request):
    """Vista temporal para previsualizar el correo de activación de cuenta."""
    
    # Creamos un usuario ficticio para la vista
    user = User(email="usuario.ejemplo@smartquail.com", first_name="Usuario")

    # URL de activación de ejemplo
    activation_url = "http://localhost:8000/es/activar/UID123TOKEN456"

    # Link de WhatsApp de ejemplo
    whatsapp_link = "https://wa.me/593963521262?text=Hola%20SmartQuail,%20quiero%20asistencia%20para%20activar%20mi%20cuenta%20(usuario.ejemplo@smartquail.com)"

    return render(request, "emails/activation/account_activation_email.html", {
        "user": user,
        "activation_url": activation_url,
        "whatsapp_link": whatsapp_link
    })





# usuarios/views.py
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
from .models import CustomUser
from .forms import PasswordResetRequestForm
from .tasks import enviar_correo_recuperacion, enviar_sms_recuperacion  # 👈 Importar tareas


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            telefono = form.cleaned_data['telefono']

            # Buscar usuario
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, 'No existe ninguna cuenta registrada con ese correo electrónico.')
                return render(request, 'usuarios/password_reset_request.html', {'form': form})

            # Validar número de teléfono
            if not getattr(user, 'telefono', None):
                messages.error(request, 'El usuario no tiene un número de teléfono registrado en el sistema.')
                return render(request, 'usuarios/password_reset_request.html', {'form': form})

            if str(user.telefono) != str(telefono):
                messages.error(request, 'El número de teléfono ingresado no coincide con el registrado para esta cuenta.')
                return render(request, 'usuarios/password_reset_request.html', {'form': form})

            # 🌐 Obtener dominio base
            domain = request.build_absolute_uri('/')[:-1]

            # 🚀 Enviar correo y SMS en segundo plano
            enviar_correo_recuperacion.delay(user.id, domain)
            enviar_sms_recuperacion.delay(user.id, domain)

            # ✅ Mensaje de éxito inmediato
            messages.success(
                request,
                'Se ha enviado un enlace de restablecimiento a su correo electrónico y un SMS a su número registrado.'
            )
            return redirect('usuarios:login')

    else:
        form = PasswordResetRequestForm()

    return render(request, 'usuarios/password_reset_request.html', {'form': form})


# usuarios/views.py
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

def preview_password_reset_email(request):
    """Vista temporal para previsualizar el correo de restablecimiento."""
    user = User(email="usuario.ejemplo@smartquail.com")
    reset_url = "https://ec.smartquail.io/es/reset/ABC123XYZ"

    return render(request, "emails/password_reset/password_reset_email.html", {
        "user": user,
        "reset_url": reset_url
    })





# views.py (continuación)
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model

User = get_user_model()

def password_reset_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 and password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, 'Su contraseña ha sido restablecida correctamente.')
                return redirect('usuarios:login')
            else:
                messages.error(request, 'Las contraseñas no coinciden.')
        return render(request, 'usuarios/password_reset_confirm.html')
    else:
        messages.error(request, 'El enlace de restablecimiento no es válido o ha expirado.')
        return redirect('usuarios:password_reset_request')



@login_required
def ultima_cita(request):
    profile = Profile.objects.filter(user=request.user).first()

    if not profile:
        return render(request, 'usuarios/panel_usuario2.html', {
            'mensaje': 'No se encontró el perfil del usuario.'
        })

    # Obtener la última tarea pendiente (envio_tarea=False)
    ultima_cita = (
        tareas.objects
        .filter(profile=profile, envio_tarea=False)
        .order_by('cita_terapeutica_asignada', 'hora')
        .first()
    )

    if not ultima_cita:
        return render(request, 'usuarios/panel_usuario2.html', {
            'mensaje': 'No tienes sesiones pendientes.'
        })

    return render(request, 'usuarios/panel_usuario2.html', {
        'ultima_cita': ultima_cita
    })



def politicas_terminos(request):
    """
    Vista que renderiza la página de Políticas de Seguridad,
    Uso de la Información y Términos y Condiciones.
    """
    return render(request, 'politicas_terminos.html')



@login_required
def ultima_tarea(request):
    try:
        profile = Profile.objects.get(user=request.user)

        # Última tarea enviada
        ultima_tarea_enviada = tareas.objects.filter(
            profile=profile,
            envio_tarea=True
        ).order_by('-fecha_envio', '-fecha_entrega').first()

        # Última tarea pendiente por enviar
        ultima_tarea_pendiente = tareas.objects.filter(
            profile=profile,
            envio_tarea=False
        ).order_by('-fecha_envio', '-fecha_entrega').first()

        contexto = {
            'ultima_tarea_enviada': ultima_tarea_enviada,
            'ultima_tarea_pendiente': ultima_tarea_pendiente
        }

        if not ultima_tarea_enviada and not ultima_tarea_pendiente:
            contexto['mensaje'] = 'No tienes tareas asignadas todavía.'

        return render(request, 'usuarios/panel_usuario2.html', contexto)

    except Profile.DoesNotExist:
        return render(request, 'usuarios/panel_usuario2.html', {
            'mensaje': 'No se encontró el perfil del usuario.'
        })


@staff_member_required
def dashboard_view(request):
    return render(request, "admin/custom_dashboard.html")

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context



@login_required
def user_logout(request):
    logout(request)
    return redirect('usuarios:login')


from django.contrib.auth import authenticate, login, get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.conf import settings

User = get_user_model()


from .tasks import enviar_correo_login  # 👈 importa la tarea

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            # Buscar el usuario por email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, "❌ No existe ningún usuario registrado con ese correo electrónico.")
                return render(request, 'registration/editorial_literario/login.html', {'form': form})

            # Autenticar
            user_auth = authenticate(request, username=user.email, password=password)
            if user_auth is None:
                messages.error(request, "⚠️ La contraseña no corresponde al usuario registrado.")
                return render(request, 'registration/editorial_literario/login.html', {'form': form})

            # Validar si está activo
            if not user_auth.is_active:
                messages.warning(
                    request,
                    "⚠️ Su cuenta todavía no ha sido activada. "
                    "Por favor revise su correo o contacte al administrador del sistema."
                )
                return render(request, 'registration/editorial_literario/login.html', {'form': form})

            # ================================
            # 🔥 Iniciar sesión
            # ================================
            login(request, user_auth)

            # ================================
            # 🔥 Enviar correo login (SE MANTIENE)
            # ================================
            fecha_hora = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M:%S")
            user_ip = request.META.get('REMOTE_ADDR', 'IP no disponible')
            enviar_correo_login.delay(user_auth.id, fecha_hora, user_ip)

            messages.success(request, f"✅ Bienvenido, {user_auth.first_name or user_auth.email}")

            # ================================
            # 🔥 Redirección inteligente
            # ================================
            # Si NO tiene perfil → crear perfil
            if not hasattr(user_auth, "profile"):
                return redirect('usuarios:perfil')

            # Si tiene perfil, evaluamos
            profile = user_auth.profile

            # ================================
            # 🔥 Redirección según tamaño de empresa
            # ================================
            if profile.tamano_empresa == "1-10 usuarios":
                return redirect("usuarios:dashboard_micro")

            elif profile.tamano_empresa == "11-50 usuarios":
                return redirect("usuarios:dashboard_pequena")

            elif profile.tamano_empresa == "51-200 usuarios":
                return redirect("usuarios:dashboard_mediana")

            elif profile.tamano_empresa == "200+ usuarios":
                return redirect("usuarios:dashboard_enterprise")

            # Si no tiene tamaño registrado → dashboard general
            return redirect("usuarios:perfil")

    else:
        form = LoginForm()

    return render(request, 'registration/editorial_literario/login.html', {'form': form})


from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()

def preview_login_notification_email(request):
    """Vista temporal para previsualizar la plantilla del correo de notificación de inicio de sesión."""
    # Usuario simulado
    user = User(
        first_name="Juan",
        email="juan.perez@smartquail.com"
    )

    # Datos simulados
    fecha_hora = timezone.localtime(timezone.now()).strftime("%d/%m/%Y %H:%M:%S")
    user_ip = "192.168.1.45"

    return render(request, "emails/login_notification/login_notification_email.html", {
        "user": user,
        "fecha_hora": fecha_hora,
        "user_ip": user_ip
    })





@login_required
@staff_member_required
def admin_cita_detail(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    context = {
        "title": f"Cita #{cita.id}",
        "breadcrumbs": [
            {"url": "/admin/", "label": "Admin"},
            {"url": "", "label": f"Cita #{cita.id}"},
        ],
        "cards": [
            {
                "title": "Detalle de la cita",
                "icon": "event",
                "items": [
                    {"title": "destinatario", "description": str(cita.destinatario)},
                    {"title": "Fecha", "description": str(cita.fecha)},
                    {"title": "Estado", "description": str(cita.estado or "No definido")}
                ],
            }
        ],
        "cita": cita,
    }
    return render(request, "admin/test.html", context)

@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)


    return render(request, 'usuarios/profile.html', {
        'profile': profile,
    })



# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm


@login_required
def dashboard(request):
    profile = Profile.objects.get(user=request.user)    
    return render(request, 'usuarios/dashboard.html', {
        'section': 'dashboard',
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard_micro(request):
    """
    Dashboard para empresas pequeñas (1-10 usuarios)
    """
    profile = request.user.profile
    return render(request, "usuarios/dashboards/dashboard_micro.html", {
        "profile": profile,
    })


@login_required
def dashboard_pequena(request):
    """
    Dashboard para empresas pequeñas (11-50 usuarios)
    """
    profile = request.user.profile
    return render(request, "usuarios/dashboards/dashboard_pequena.html", {
        "profile": profile,
    })


@login_required
def dashboard_mediana(request):
    """
    Dashboard para empresas medianas (51-200 usuarios)
    """
    profile = request.user.profile
    return render(request, "usuarios/dashboards/dashboard_mediana.html", {
        "profile": profile,
    })


@login_required
def dashboard_enterprise(request):
    """
    Dashboard para empresas grandes (200+ usuarios)
    """
    profile = request.user.profile
    return render(request, "usuarios/dashboards/dashboard_enterprise.html", {
        "profile": profile,
    })





@login_required
def profile_edit_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user = request.user  # CustomUser

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Guardar cambios en Profile
            profile = form.save(commit=False)
            profile.save()

            # Sincronizar con CustomUser
            user.first_name = form.cleaned_data.get("nombre_completo", "").split(' ')[0] if form.cleaned_data.get("nombre_completo") else user.first_name
            user.last_name = ' '.join(form.cleaned_data.get("nombre_completo", "").split(' ')[1:]) if form.cleaned_data.get("nombre_completo") else user.last_name
            user.email = form.cleaned_data.get("email_corporativo", user.email)
            user.telefono = form.cleaned_data.get("telefono", user.telefono)
            user.save()

            return redirect('usuarios:dashboard')  # Cambia al nombre real de tu URL
    else:
        # Precargar datos desde CustomUser y Profile
        form = ProfileForm(
            instance=profile,
            initial={
                "nombre_completo": f"{user.first_name} {user.last_name}".strip(),
                "email_corporativo": user.email,
                "telefono": user.telefono
            }
        )

    return render(request, 'usuarios/profile.html', {
        'form': form,
        'profile': profile,
    })





@login_required
def header(request):
    # Ejemplo: contar pedidos creados en las últimas 24 horas
    last_24_hours = timezone.now() - timedelta(hours=24)
    new_notify_count = Mensaje.objects.filter(receptor=request.user, leido=False).count()

    return render(request, 'usuarios/header.html', {
        'new_notify_count': new_notify_count
    })

@login_required
def msj_success(request):
    return render(request, 'usuarios/success.html')
    
def ver_mensaje(request, pk):
    mensaje = get_object_or_404(Mensaje, pk=pk)

    # Si el mensaje no ha sido leído, lo marcamos como leído
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()

    return render(request, 'usuarios/mensaje.html', {'mensaje': mensaje})

@login_required
def enviar_mensaje(request):
    destinatario = User.objects.get(id=1)  # <--- usuario fijo al que se envían los mensajes

    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.emisor = request.user
            mensaje.receptor = User.objects.get(id=1)  # <-- se asigna automáticamente
            mensaje.save()
            return redirect('usuarios:success')  # o donde prefieras
    else:
        form = MensajeForm()
    
    return render(request, 'usuarios/enviar_mensaje.html', {'form': form})

@login_required
def inbox_view(request):
    profile = Profile.objects.get(user=request.user)
    mensajes = Mensaje.objects.filter(receptor=profile)

    leidos = mensajes.filter(leido=True).count()
    no_leidos = mensajes.filter(leido=False).count()
    total = mensajes.count()

    return render(request, 'usuarios/inbox.html', {
        'mensajes': mensajes,
        'profile': profile,
        'leidos': leidos,
        'no_leidos': no_leidos,
        'total': total,
    })

@login_required
def inbox_record(request):
    profile = get_object_or_404(Profile, user=request.user)

    # Todos los mensajes recibidos asignados al perfil del usuario
    mensajes = Mensaje.objects.filter(receptor=profile)

    leidos = mensajes.filter(leido=True).count()
    no_leidos = mensajes.filter(leido=False).count()
    total = mensajes.count()

    return render(request, 'usuarios/inbox_total.html', {
        'mensajes': mensajes,
        'profile': profile,
        'leidos': leidos,
        'no_leidos': no_leidos,
        'total': total,
    })



@login_required
def cita_success(request):
    return render(request, 'usuarios/citas/success.html')
    



@login_required
def citas_record(request):
    profile = get_object_or_404(Profile, user=request.user)

    citas = (
        Cita.objects
        .filter(profile=profile)
        .select_related('creador', 'profile')
        .order_by('-fecha', '-hora')
    )

    confirmadas = citas.filter(confirmada=True, pendiente=False, cancelada=False)
    pendientes = citas.filter(pendiente=True, confirmada=False, cancelada=False)
    canceladas = citas.filter(cancelada=True, pendiente=False, confirmada=False)

    context = {
        'citas': citas,
        'profile': profile,
        'confirmadas': confirmadas.count(),
        'pendientes': pendientes.count(),
        'canceladas': canceladas.count(),
        'total': citas.count(),
    }

    return render(request, 'usuarios/citas/calendar_total.html', context)


@login_required
def citas_agendadas_total(request):
    profile = get_object_or_404(Profile, user=request.user)

    # 🔸 Filtrar solo las citas pendientes usando el campo profile
    citas_pendientes = Cita.objects.filter(profile=profile, pendiente=True)

    # 🔸 Contar solo las citas del usuario actual (usando profile)
    confirmadas = Cita.objects.filter(profile=profile, confirmada=True).count()
    no_confirmadas = Cita.objects.filter(profile=profile, confirmada=False).count()
    total = Cita.objects.filter(profile=profile).count()

    return render(request, 'usuarios/citas/calendar_agendadas.html', {
        'citas': citas_pendientes,  # solo las pendientes
        'profile': profile,
        'confirmadas': confirmadas,
        'no_confirmadas': no_confirmadas,
        'total': total,
    })


from .forms import CitaPacienteForm

@login_required
def agendar_cita(request):
    profile = getattr(request.user, 'profile', None)

    if request.method == 'POST':
        form = CitaPacienteForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.creador = request.user
            cita.profile = profile
            cita.pendiente = True  # Estado inicial
            cita.save()
            return redirect('usuarios:ver_cita', pk=cita.pk)
    else:
        form = CitaPacienteForm()

    return render(request, 'usuarios/citas/agendar_cita.html', {'form': form})





@login_required
def ver_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk)

    # Solo el creador o destinatario puede acceder
    if request.user != cita.creador and request.user != cita.profile.user:
        return HttpResponseForbidden("No tienes permiso para ver esta cita.")

    if request.method == "POST":
        accion = request.POST.get("accion")

        if accion == "confirmar":
            cita.confirmada = True
            cita.pendiente = False
            cita.cancelada = False
            messages.success(request, "Cita confirmada correctamente.")
        elif accion == "cancelar":
            cita.cancelada = True
            cita.confirmada = False
            cita.pendiente = False
            messages.warning(request, "Cita cancelada correctamente.")

        cita.save()
        return redirect('usuarios:ver_cita', pk=cita.pk)

    return render(request, 'usuarios/citas/cita.html', {'cita': cita})


@login_required
def confirmar_cita(request, pk):
    # Obtener el profile del usuario actual
    profile = Profile.objects.filter(user=request.user).first()

    if not profile:
        return redirect('usuarios:panel_usuario')  # O muestra un error si lo prefieres

    # Obtener la cita solo si pertenece al profile del usuario
    cita = get_object_or_404(Cita, pk=pk, profile=profile)

    if request.method == 'POST':
        cita.confirmada = True
        cita.pendiente = False
        cita.cancelada = False
        cita.save()
        messages.success(request, "Cita confirmada correctamente.")

    return redirect('usuarios:ver_cita', pk=pk)

@login_required
def cancelar_cita(request, pk):
    cita = get_object_or_404(Cita, pk=pk, destinatario=request.user)
    if request.method == 'POST':
        # Cambiar los campos booleanos para reflejar que la cita está cancelada
        cita.pendiente = False
        cita.confirmada = False
        cita.cancelada = True
        cita.save()
    return redirect('usuarios:ver_cita', pk=pk)


@login_required
def config_view(request):
    # Obtener el perfil del usuario actualmente autenticado
    profile = Profile.objects.get(user=request.user)
    return render(request, 'usuarios/config.html', {'profile': profile})




@login_required
def gestionar_citas_view(request):
    citas = Cita.objects.filter(destinatario=request.user).order_by('-fecha')

    citas_confirmadas = citas.filter(confirmada=True).count()
    citas_pendientes = citas.filter(pendiente=True).count()
    citas_canceladas = citas.filter(cancelada=True).count()

    return render(request, 'usuarios/citas/calendar.html', {
        'citas': citas,
        'citas_confirmadas': citas_confirmadas,
        'citas_pendientes': citas_pendientes,
        'citas_canceladas': citas_canceladas,
    })

@login_required
def cancelar_cita_view(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, destinatario=request.user)
    
    if cita.estado == 'cancelada':
        messages.info(request, 'La cita ya está cancelada.')
    else:
        cita.estado = 'cancelada'
        cita.save()
        messages.success(request, 'La cita ha sido cancelada correctamente.')

    return redirect('gestionar_citas')

@login_required
def editar_cita_view(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, destinatario=request.user)

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'La cita ha sido actualizada correctamente.')
            return redirect('gestionar_citas')
    else:
        form = CitaForm(instance=cita)

    return render(request, 'usuarios/editar_cita.html', {'form': form, 'cita': cita})



@login_required
def tareas_asignadas(request):
    # Filtra todas las tareas asignadas al usuario logueado
    tareas_usuario = tareas.objects.filter(profile__user=request.user)

    # Separar por estado
    tareas_realizadas = tareas_usuario.filter(actividad_realizada=True)
    tareas_pendientes = tareas_usuario.filter(actividad_realizada=False)

    context = {
        'tareas_realizadas': tareas_realizadas,
        'tareas_pendientes': tareas_pendientes,
        'total': tareas_usuario.count(),
        'total_realizadas': tareas_realizadas.count(),
        'total_pendientes': tareas_pendientes.count(),
    }

    return render(request, 'usuarios/tareas/tareas_asignadas.html', context)


@login_required
def tareas_list(request):
    tareas_nuevas = tareas.objects.filter(
        profile__user=request.user,
        actividad_realizada=False
    ).order_by('-fecha_envio')
    tareas_usuario = tareas.objects.filter(profile__user=request.user)
    
    tareas_realizadas = tareas_usuario.filter(actividad_realizada=True)
    tareas_pendientes = tareas_usuario.filter(actividad_realizada=False)

    return render(request, 'usuarios/tareas/tareas_list.html', {
        'tareas_nuevas': tareas_nuevas,
        'total': tareas_usuario.count(),
        'total_realizadas': tareas_realizadas.count(),
        'total_pendientes': tareas_pendientes.count(),

    })


@login_required
def ver_tarea(request, pk):
    # Buscar la tarea asegurando que el usuario autenticado es el dueño (paciente)
    tarea = get_object_or_404(tareas, pk=pk, profile__user=request.user)

    comentarios = tarea.comentarios.all()
    form = TareaComentarioForm()

    if request.method == 'POST':
        form = TareaComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarea = tarea
            comentario.save()

            # Marcar como realizada si el usuario autenticado es el paciente
            tarea.realizada = True
            tarea.save()

            return redirect('usuarios:ver_tarea', pk=tarea.pk)

    return render(request, 'usuarios/tareas/tarea.html', {
        'tarea': tarea,
        'comentarios': comentarios,
        'form': form,
    })



@login_required
def ver_tarea_interactiva(request, pk):
    tarea = get_object_or_404(tareas, pk=pk)

    comentarios = tarea.comentarios.all()
    form = TareaComentarioForm()

    if request.method == 'POST':
        form = TareaComentarioForm(request.POST, request.FILES)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarea = tarea
            comentario.save()

            # Opcional: marcar como realizada si el comentario lo hace el paciente
            if request.user == tarea.paciente:
                tarea.realizada = True
                tarea.save()

            return redirect('usuarios:ver_tarea_interactiva', pk=tarea.pk)

    return render(request, 'usuarios/tareas/tarea_interactiva.html', {
        'tarea': tarea,
        'comentarios': comentarios,
        'form': form,
    })



@login_required
def tareas_realizadas(request):
    # Filtra tareas que fueron realizadas por el usuario autenticado
    tareas_completadas = tareas.objects.filter(profile__user=request.user, actividad_realizada=True)

    return render(request, 'usuarios/tareas/tareas_realizadas.html', {
        'tareas_completadas': tareas_completadas,
    })


@login_required
def marcar_tarea_realizada(request, pk):
    # Verifica que la tarea pertenezca al usuario
    tarea = get_object_or_404(tareas, pk=pk, profile__user=request.user)

    if request.method == 'POST':
        tarea.realizada = True
        tarea.save()
        return redirect('usuarios:tareas_realizadas')  # Redirige a la lista de tareas realizadas

    return redirect('usuarios:ver_tarea', pk=pk)



@login_required
def lista_pagos(request):
    # Filtrar los pagos relacionados al usuario actual (vía profile.user)
    pagos_usuario = pagos.objects.filter(profile__user=request.user).order_by('-created_at')

    # Clasificar según los booleanos
    pagos_pendientes = pagos_usuario.filter(pendiente=True)
    pagos_vencidos = pagos_usuario.filter(vencido=True)
    pagos_realizados = pagos_usuario.filter(al_dia=True)

    return render(request, 'usuarios/pagos/lista_pagos.html', {
        'pagos_usuario': pagos_usuario,
        'pagos_pendientes': pagos_pendientes,
        'pagos_vencidos': pagos_vencidos,
        'pagos_realizados': pagos_realizados,
    })


@login_required
def pagos_pendientes_view(request):
    pagos_pendientes = pagos.objects.filter(profile__user=request.user, pendiente=True).order_by('-fecha_vencimiento')

    return render(request, 'usuarios/pagos/pagos_pendientes.html', {
        'pagos_pendientes': pagos_pendientes,
    })



@login_required
def pagos_vencidos_view(request):
    pagos_vencidos = pagos.objects.filter(profile__user=request.user, vencido=True).order_by('-fecha_vencimiento')

    return render(request, 'usuarios/pagos/pagos_vencidos.html', {
        'pagos_vencidos': pagos_vencidos,
    })




@login_required
def ver_pago(request, pk):
    pago = get_object_or_404(pagos, pk=pk)

    # Verificar que el pago pertenezca al usuario autenticado
    if not pago.profile or pago.profile.user != request.user:
        return render(request, '403.html', status=403)

    # Procesar el formulario de carga de comprobante
    if request.method == 'POST' and not pago.comprobante_pago:
        comprobante = request.FILES.get('comprobante_pago')
        numero = request.POST.get('numero_de_comprobante')

        if comprobante:
            pago.comprobante_pago = comprobante
            pago.numero_de_comprobante = numero
            pago.save()
            messages.success(request, "Comprobante subido correctamente.")
            return redirect('usuarios:ver_pago', pk=pk)
        else:
            messages.error(request, "Por favor sube un archivo válido.")

    return render(request, 'usuarios/pagos/ver_pago.html', {'pago': pago})


@login_required
def subir_comprobante_pago(request, pk):
    pago = get_object_or_404(pagos, pk=pk)

    # Asegurar que el usuario autenticado sea el dueño del pago
    if pago.profile.user != request.user:
        messages.error(request, "No tienes permisos para modificar este pago.")
        return redirect('usuarios:lista_pagos')

    if request.method == 'POST':
        comprobante = request.FILES.get('comprobante_pago')
        numero = request.POST.get('numero_de_comprobante')

        if not comprobante:
            messages.error(request, "Debes adjuntar un comprobante.")
        else:
            if pago.comprobante_pago:
                messages.warning(request, "Ya has subido un comprobante.")
            else:
                pago.comprobante_pago = comprobante
                pago.numero_de_comprobante = numero
                pago.save()
                messages.success(request, "Comprobante subido exitosamente.")
                return redirect('usuarios:ver_pago', pk=pago.pk)

    return render(request, 'usuarios/pagos/subir_comprobante.html', {'pago': pago})




@login_required
def vista_certificados(request):
    # Obtener el perfil del usuario logueado
    profile = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        form = AutorizacionForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('usuarios:vista_certificados')
    else:
        form = AutorizacionForm(instance=profile)

    # ✅ Usar el perfil para filtrar los mensajes
    mensajes = Mensaje.objects.filter(receptor=profile).order_by('-fecha_envio')

    # Archivos adjuntos del perfil del usuario
    archivos = InformesTerapeuticos.objects.filter(profile=profile).order_by('-fecha_creado')

    return render(request, 'usuarios/certificados/certificados_total.html', {
        'form': form,
        'profile': profile,
        'mensajes': mensajes,
        'archivos': archivos
    })


from django.views.generic import TemplateView
from unfold.views import UnfoldModelAdminViewMixin

class DashboardPrincipalView(UnfoldModelAdminViewMixin, TemplateView):
    title = "Dashboard Principal"  # Esto aparece como título en la página
    permission_required = ()       # Asegúrate de configurar esto para tu seguridad
    template_name = "usuarios/dashboard_principal.html"







class TareaListView(ListView):
    model = tareas
    template_name = 'tareas/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        return tareas.objects.filter(
            profile__user=self.request.user,
            envio_tarea=True  # ⬅️ Solo tareas enviadas
        ).order_by('-fecha_envio')


class TareaDetailView(LoginRequiredMixin, DetailView):
    model = tareas
    template_name = 'usuarios/tareas/tarea.html'
    context_object_name = 'tarea'

    def get_object(self, queryset=None):
        # Garantizar que la tarea pertenece al usuario autenticado
        return get_object_or_404(tareas, pk=self.kwargs['pk'], profile__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = self.object.comentarios.all()
        context['form'] = TareaComentarioForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Define self.object para el template
        form = TareaComentarioForm(request.POST, request.FILES)
        
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = request.user
            comentario.tarea = self.object
            comentario.save()

            # Marcar tarea como realizada
            self.object.actividad_realizada = True  # O tarea.realizada, si ese es el campo correcto
            self.object.save()

            return redirect('usuarios:ver_tarea', pk=self.object.pk)

        # Si el formulario es inválido, volver a renderizar con errores
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)


class ActividadListView(LoginRequiredMixin, ListView):
    model = tareas
    template_name = 'tareas/actividad_list.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        # Solo mostrar actividades enviadas, del usuario actual
        return tareas.objects.filter(
            envio_tarea=True,
            profile__user=self.request.user
        ).order_by('-fecha_envio')


class ActividadDetailView(LoginRequiredMixin, DetailView):
    model = tareas
    template_name = 'tareas/actividad_detail.html'
    context_object_name = 'actividad'

    def get_object(self, queryset=None):
        # Solo permite ver actividades propias que han sido enviadas
        return get_object_or_404(
            tareas,
            pk=self.kwargs['pk'],
            profile__user=self.request.user,
            envio_tarea=True
        )

class TerapiaListView(ListView):
    model = tareas
    template_name = 'tareas/terapia_list.html'
    context_object_name = 'terapias'

    def get_queryset(self):
        return tareas.objects.filter(cita_terapeutica_asignada__isnull=False, profile__user=self.request.user).order_by('-cita_terapeutica_asignada')

class TerapiaDetailView(DetailView):
    model = tareas
    template_name = 'tareas/terapia_detail.html'
    context_object_name = 'terapia'



class CitasAsistidasListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'citas/citas_asistidas.html'
    context_object_name = 'citas'

    def get_queryset(self):
        return Cita.objects.filter(profile__user=self.request.user, confirmada=True)

class CitasNoAsistidasListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'citas/citas_no_asistidas.html'
    context_object_name = 'citas'

    def get_queryset(self):
        return Cita.objects.filter(profile__user=self.request.user, cancelada=True)

class CitasPendientesListView(LoginRequiredMixin, ListView):
    model = Cita
    template_name = 'citas/citas_pendientes.html'
    context_object_name = 'citas'

    def get_queryset(self):
        return Cita.objects.filter(profile__user=self.request.user, pendiente=True)

class CitaDetailView(LoginRequiredMixin, DetailView):
    model = Cita
    template_name = 'citas/cita_detalle.html'
    context_object_name = 'cita'

    def get_queryset(self):
        return Cita.objects.filter(profile__user=self.request.user)