from django.contrib import messages
from django.shortcuts import redirect

def session_rol_permission(*roles):
    def decorador(func):
        def decorada(request, *args, **kwargs):
            autenticado = request.session.get("pista", False)
            if autenticado:
                if len(roles) == 0 or (autenticado["rol"] in roles):
                    print(f"Sesion y Rol OK: {autenticado['rol']}")
                    return func(request, *args, **kwargs)
                else:
                    messages.info(request, "Usted no esta autorizado")
                    return redirect("index")
            else:
                messages.warning(request, "Usted no ha iniciado sesion")    
                return redirect("login")
        return decorada
    return decorador


from django.core.mail import EmailMessage

def send_email_with_attachment(subject, body, to_emails, attachments=None, from_email=None):
    """
    Envía un correo electrónico con posibilidad de archivos adjuntos.
    """

    email = EmailMessage(
        subject,
        body,
        from_email,
        to_emails
    )

    if attachments:
        for filename, content, mimetype in attachments:
            email.attach(filename, content, mimetype)

    try:
        email.send()
        return True
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
        return False
	