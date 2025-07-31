

def permission_callback(request):
    return request.user.has_perm("usuarios.change_model")


def permission_callback_prospecion(request):
    return request.user.has_perm("usuarios.change_Prospecion")



