# project/utils/environment.py

def environment_callback(request):
    import os
    env = os.getenv('DJANGO_ENV', 'SmartBusinessAnalytics® ')

    if env == 'production':
        return ["SmartBusinessAnalytics® (I+D)+A", "success"]
    elif env == 'staging':
        return ["SmartBusinessAnalytics® (I+D)+A ", "warning"]
    elif env == 'demo':
        return ["SmartBusinessAnalytics® (I+D)+A", "info"]
    elif env == 'suspention':
        return ["SmartBusinessAnalytics® (I+D)+A", "danger"]
    
    else:
        return ["SmartBusinessAnalytics® (I+D)+A", "info"]



