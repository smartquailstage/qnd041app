from .models import BusinessSystemProject

def business_projects_context(request):
    # Si no está autenticado, devolver vacío
    if not request.user.is_authenticated:
        return {
            'all_projects': [],
            'projects_in_progress': [],
        }

    # Todos los proyectos del usuario
    user_projects = BusinessSystemProject.objects.filter(user=request.user)

    # Completados
    completed_projects = user_projects.filter(progress=100)

    # En progreso
    in_progress = user_projects.exclude(progress=100)

    return {
        'all_projects': completed_projects,
        'projects_in_progress': in_progress,
    }
