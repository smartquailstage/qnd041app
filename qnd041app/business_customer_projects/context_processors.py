from .models import BusinessSystemProject

def all_business_projects(request):
    return {
        'all_projects': BusinessSystemProject.objects.all()
    }
