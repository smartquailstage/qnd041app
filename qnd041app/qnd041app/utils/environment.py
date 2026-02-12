# project/utils/environment.py

def environment_callback(request):
    import os
    env = os.getenv('DJANGO_ENV', 'SmartBusinessAnalytics® ')

    if env == 'production':
        return ["SmartQuail.S.A.S", "success"]
    elif env == 'staging':
        return ["SmartQuail.S.A.S", "warning"]
    elif env == 'demo':
        return ["SmartQuail.S.A.S", "info"]
    elif env == 'suspention':
        return ["SmartQuail.S.A.S", "danger"]
    
    else:
        return ["SmartQuail.S.A.S", "info"]



