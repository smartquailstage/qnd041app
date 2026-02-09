# project/utils/environment.py

def environment_callback(request):
    import os
    env = os.getenv('DJANGO_ENV', 'SmartBusinessAnalytics® ')

    if env == 'production':
        return ["Version:qnd.0.4.1.0.1", "success"]
    elif env == 'staging':
        return ["Version: qnd.0.4.1.0.1", "warning"]
    elif env == 'demo':
        return ["Version: qnd.0.4.1.0.1", "info"]
    elif env == 'suspention':
        return ["Version: qnd.0.4.1.0.1", "danger"]
    
    else:
        return ["Version:qnd.0.4.1.app", "info"]



