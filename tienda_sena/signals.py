from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from allauth.socialaccount.signals import pre_social_login, social_account_added
from .models import Usuario
from django.contrib import messages

def combinar_carritos_helper(request):
    """Helper function para combinar carritos - importada desde views"""
    from .views import combinar_carritos
    combinar_carritos(request)

@receiver(pre_social_login)
def social_login_handler(sender, request, sociallogin, **kwargs):
    """
    Signal que se ejecuta antes del login social.
    Maneja la creación de usuarios en el modelo personalizado.
    """
    # Obtener datos del usuario de Google
    email = sociallogin.account.extra_data.get('email')
    name = sociallogin.account.extra_data.get('name', '')
    
    if email:
        try:
            # Buscar si ya existe un usuario con este email
            usuario = Usuario.objects.get(correo=email)
            
            # Si existe, actualizar la sesión personalizada
            request.session["pista"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.nombre_apellido
            }
            
            # Combinar carritos si es necesario
            combinar_carritos_helper(request)
            
        except Usuario.DoesNotExist:
            # Si no existe, crear un nuevo usuario
            usuario = Usuario.objects.create(
                nombre_apellido=name or email.split('@')[0],
                correo=email,
                password="",  # Los usuarios de Google no necesitan contraseña local
                rol=2,  # Cliente por defecto
                documento="000000"  # Documento por defecto
            )
            
            # Crear la sesión personalizada para el nuevo usuario
            request.session["pista"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.nombre_apellido
            }
            
            # Combinar carritos si es necesario
            combinar_carritos_helper(request)
            
            messages.success(request, f"¡Bienvenido {usuario.nombre_apellido}! Tu cuenta ha sido creada exitosamente.")


@receiver(social_account_added)
def social_account_added_handler(sender, request, sociallogin, **kwargs):
    """
    Signal que se ejecuta después de agregar una cuenta social.
    """
    messages.success(request, f"¡Bienvenido de vuelta {sociallogin.account.extra_data.get('name', 'Usuario')}!")


@receiver(user_logged_in)
def user_logged_in_handler(sender, user, request, **kwargs):
    """
    Signal que se ejecuta cuando un usuario hace login.
    Se asegura de que la sesión personalizada esté configurada.
    """
    # Solo manejar si no hay sesión "pista" ya establecida
    if not request.session.get("pista"):
        try:
            # Buscar el usuario en nuestro modelo personalizado
            usuario = Usuario.objects.get(correo=user.email)
            
            request.session["pista"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.nombre_apellido
            }
            
        except Usuario.DoesNotExist:
            # Si no existe en nuestro modelo, crear uno
            usuario = Usuario.objects.create(
                nombre_apellido=user.get_full_name() or user.username or user.email.split('@')[0],
                correo=user.email,
                password="",
                rol=2,  # Cliente por defecto
                documento="000000"
            )
            
            request.session["pista"] = {
                "id": usuario.id,
                "rol": usuario.rol,
                "nombre": usuario.nombre_apellido
            }
