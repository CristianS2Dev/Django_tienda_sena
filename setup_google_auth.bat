@echo off
echo Instalando Django Allauth...
pip install django-allauth

echo.
echo Aplicando migraciones...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo Django Allauth instalado correctamente!
echo ========================================
echo.
echo SIGUIENTE PASO: Configurar Google OAuth2
echo.
echo 1. Ve a: https://console.developers.google.com/
echo 2. Crea un nuevo proyecto o selecciona uno existente
echo 3. Habilita la API de Google+
echo 4. Ve a "Credenciales" y crea credenciales OAuth 2.0
echo 5. Agrega estas URIs de redireccion:
echo    - http://127.0.0.1:8000/accounts/google/login/callback/
echo    - http://localhost:8000/accounts/google/login/callback/
echo 6. Copia el Client ID y Client Secret
echo 7. Ejecuta: python manage.py runserver
echo 8. Ve a: http://127.0.0.1:8000/admin/
echo 9. En "Social Applications" agrega tu aplicacion de Google
echo.
pause
