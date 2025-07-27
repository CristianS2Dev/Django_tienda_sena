def get_user_session_info(request):
    """
    Obtiene información segura de la sesión del usuario.
    Retorna un diccionario con la información del usuario o None si no está logueado.
    """
    pista = request.session.get("pista", None)
    if pista and isinstance(pista, dict):
        user_id = pista.get('id')
        if user_id is not None and str(user_id).strip() != '':
            return {
                'id': user_id,
                'rol': pista.get('rol'),
                'nombre': pista.get('nombre', ''),
                'email': pista.get('email', ''),
                'is_authenticated': True
            }
    return {'is_authenticated': False}


def has_valid_user_session(request):
    """
    Verifica si el usuario tiene una sesión válida con ID.
    """
    user_info = get_user_session_info(request)
    return user_info['is_authenticated']
