# TIENDA SENA 🛍️  

**Tienda Sena** es una plataforma de ecommerce desarrollada específicamente para los aprendices del SENA, donde pueden promocionar y vender sus proyectos, emprendimientos y productos. La plataforma ofrece un espacio seguro, moderno y accesible para la gestión de negocios digitales estudiantiles.

## 🚀 Características Principales  

### Para Estudiantes/Vendedores:
- 🏪 **Creación de tiendas virtuales personalizadas**
- 📦 **Gestión completa de productos** (agregar, editar, eliminar)
- 🖼️ **Optimización automática de imágenes** con múltiples formatos
- 📊 **Panel de control** para gestionar ventas y productos
- 📋 **Sistema de solicitudes** para convertirse en vendedor

### Para Compradores:
- 🛒 **Carrito de compras inteligente** con persistencia
- ⭐ **Sistema de valoraciones y reseñas**
- 🔍 **Búsqueda avanzada** por categorías y filtros
- 💬 **Comentarios y calificaciones** de productos
- 👤 **Perfiles de usuario personalizables**

### Para Administradores:
- 🛡️ **Panel de administración completo**
- 👥 **Gestión de usuarios** y roles
- ✅ **Aprobación de vendedores**

## 🛠️ Tecnologías Utilizadas  

- **Backend:** Django 5.1.1 (Python 3.10+)
- **Base de datos:** SQLite3 (desarrollo) / PostgreSQL/MySQL (producción)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap Icons
- **Autenticación:** Django Allauth 65.9.0
- **Gestión de imágenes:** Cloudinary + Pillow 10.0.0+
- **Emails:** Django Email System (SMTP Gmail)
- **Testing:** Pytest + Pytest-Django
- **API:** Django REST Framework   

## 📦 Instalación y Configuración  

### Prerrequisitos
- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git
- Node.js 16.0+ (para Bootstrap Icons)

### 1. Clonar el repositorio  
```bash
git clone https://github.com/CristianS2Dev/Django_tienda_sena.git
cd Django_tienda_sena
```

### 2. Crear y activar entorno virtual (Recomendado)
**En Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias  
```bash
pip install -r requirements.txt
```

**Dependencias principales incluidas:**
- Django 5.1.1
- Django Allauth 65.9.0 (autenticación)
- Pillow 10.0.0+ (procesamiento de imágenes)
- Django REST Framework (API)
- Cloudinary (gestión de imágenes en la nube)
- Pytest 8.1.1 + Pytest-Django 4.11.1 (testing)

### 4. Configurar variables de entorno (Recomendado)
Crea un archivo `.env` en la raíz del proyecto basándote en `env.example`:
```env
# Configuración de Django
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True

# Configuración de email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password-de-aplicacion

# Configuración de Cloudinary (opcional para producción)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### 5. Realizar migraciones de base de datos  
```bash
python manage.py makemigrations
python manage.py migrate  
```

### 6. Crear superusuario (Opcional)
```bash
python manage.py createsuperuser
```

### 7. Instalar dependencias de frontend
```bash
npm install  # Para Bootstrap Icons
```

### 8. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver  
```

La aplicación estará disponible en: `http://127.0.0.1:8000/`

## ⚙️ Comandos de Gestión Útiles

### Limpieza de Carritos Huérfanos
Elimina carritos de compra sin usuario y con más de 7 días de antigüedad:
```bash
python manage.py limpiar_carritos_huerfanos
```

### Migración a Cloudinary
Migra imágenes locales al servicio de Cloudinary:
```bash
python manage.py migrar_a_cloudinary
```

### Actualización de Notificaciones
Actualiza el sistema de notificaciones:
```bash
python manage.py actualizar_notificaciones
```

### Reset de Productos
Reinicia la base de datos de productos (solo desarrollo):
```bash
python manage.py reset_productos
```

### Comandos de Administración
```bash
# Crear superusuario
python manage.py createsuperuser

# Limpiar sesiones expiradas
python manage.py clearsessions

# Recopilar archivos estáticos para producción
python manage.py collectstatic

# Ejecutar tests
python -m pytest
```

## 🏗️ Estructura del Proyecto  

```
Django_tienda_sena/
├── tienda/                     # Configuración principal del proyecto
│   ├── settings.py            # Configuraciones de Django
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuración WSGI
├── tienda_sena/               # Aplicación principal
│   ├── models.py              # Modelos: Usuario, Producto, Carrito, Orden, etc.
│   ├── views.py               # Vistas principales
│   ├── cloudinary_views.py    # Vistas para gestión de Cloudinary
│   ├── cloudinary_utils.py    # Utilidades para Cloudinary
│   ├── image_utils.py         # Utilidades para procesamiento de imágenes
│   ├── session_utils.py       # Gestión de sesiones
│   ├── email_settings.py      # Configuraciones de email
│   ├── urls.py                # URLs de la aplicación
│   ├── serializador.py        # Serializadores para API REST
│   ├── signals.py             # Señales de Django
│   ├── context_processors.py  # Procesadores de contexto
│   ├── utils.py               # Utilidades generales
│   ├── templates/             # Templates HTML
│   │   ├── index.html         # Página principal
│   │   ├── login.html         # Inicio de sesión
│   │   ├── registrarse.html   # Registro de usuarios
│   │   ├── productos/         # Templates de productos
│   │   ├── usuarios/          # Templates de usuarios
│   │   └── administrador/     # Panel de administración
│   ├── static/                # Archivos estáticos (CSS, JS, imágenes)
│   ├── management/            # Comandos personalizados de Django
│   │   └── commands/          # Comandos específicos
│   │       ├── limpiar_carritos_huerfanos.py
│   │       ├── migrar_a_cloudinary.py
│   │       ├── actualizar_notificaciones.py
│   │       └── reset_productos.py
│   ├── migrations/            # Migraciones de base de datos
│   ├── templatetags/          # Tags personalizados de templates
│   └── tests/                 # Tests unitarios
├── media/                     # Archivos subidos por usuarios
│   ├── productos/             # Imágenes de productos
│   │   ├── originales/        # Imágenes originales
│   │   ├── optimizadas/       # Imágenes optimizadas
│   │   └── miniaturas/        # Miniaturas de productos
│   ├── usuarios/              # Imágenes de usuarios
│   │   ├── perfiles/          # Fotos de perfil optimizadas
│   │   └── originales/        # Fotos de perfil originales
│   └── certificado/           # Certificados de productos
├── requirements.txt           # Dependencias de Python
├── package.json              # Dependencias de Node.js (Bootstrap Icons)
├── env.example               # Ejemplo de variables de entorno
├── backup_cron.py            # Script de respaldo automático
├── log_bk.txt               # Logs de respaldo
├── CHANGUELOG.md            # Registro de cambios
├── VERSIONING.md            # Control de versiones
└── manage.py                 # Script de gestión de Django
```

## 👥 Roles de Usuario

### 🛡️ Administrador
- Gestión completa de usuarios
- Aprobación/rechazo de solicitudes de vendedores
- Acceso al panel de administración de Django
- Supervisión general de la plataforma

### 🛍️ Vendedor
- Gestión de productos propios
- Subida y optimización de imágenes
- Panel de control de ventas
- Gestión de inventario

### 👤 Cliente
- Navegación y compra de productos
- Gestión de carrito de compras
- Sistema de reseñas y calificaciones
- Perfil personalizable

## 🌐 Funcionalidades Destacadas

### Autenticación Social
- **Registro tradicional:** Con verificación por email
- **Recuperación de contraseña:** Sistema de códigos de verificación
- **Allauth Integration:** Sistema robusto de autenticación

### Gestión de Productos
- **Categorías dinámicas:** Sistema flexible de categorización
- **Filtros avanzados:** Por precio, categoría, vendedor, colores
- **Gestión de imágenes:** Cloudinary + optimización local
- **Múltiples imágenes:** Soporte para galerías de productos con miniaturas
- **Sistema de stock:** Control de inventario en tiempo real

### Carrito de Compras
- **Persistencia:** Mantiene productos entre sesiones
- **Actualizaciones en tiempo real:** JavaScript asíncrono
- **Cálculos automáticos:** Subtotales, impuestos, totales
- **Limpieza automática:** Eliminación de carritos huérfanos después de 7 días
- **Gestión de stock:** Verificación automática de disponibilidad  

## 💻 Requerimientos del Sistema  

### 🖥️ Para Desarrollo
- **Python:** 3.10 o superior
- **Node.js:** 16.0 o superior (para Bootstrap Icons)
- **Sistema Operativo:** Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memoria RAM:** 4 GB mínimo, 8 GB recomendado
- **Almacenamiento:** 2 GB de espacio disponible

### 🌐 Para Usuarios Finales
- **Navegador:** Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Conexión a Internet:** 5 Mbps para navegación fluida
- **JavaScript:** Habilitado (requerido para funcionalidades interactivas)
- **Cookies:** Habilitadas (para sesiones y carrito de compras)

### � Para Producción
- **Servidor:** Ubuntu 20.04+ o similar
- **Memoria RAM:** 8 GB mínimo
- **Base de datos:** PostgreSQL 12+ o MySQL 8.0+
- **Servidor web:** Nginx + Gunicorn (recomendado)
- **SSL:** Certificado válido para HTTPS

## 🔧 Configuración para Producción

### Variables de Entorno Requeridas
```env
# Django
SECRET_KEY=clave_secreta_muy_segura
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com

# Base de datos
DATABASE_URL=postgresql://usuario:password@localhost/tienda_sena

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion

# Cloudinary (opcional)
CLOUDINARY_CLOUD_NAME=tu-cloud-name
CLOUDINARY_API_KEY=tu-api-key
CLOUDINARY_API_SECRET=tu-api-secret
```

### Comandos de Despliegue
```bash
# Instalar dependencias
pip install -r requirements.txt
npm install

# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear migraciones y aplicarlas
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (primera vez)
python manage.py createsuperuser

# Ejecutar tests (opcional)
python -m pytest
```

## 🐛 Solución de Problemas Comunes

### Error de Pillow
```bash
# Si hay problemas con Pillow en Windows
pip uninstall Pillow
pip install Pillow>=10.0.0

```

### Error de archivos estáticos
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --clear
```

### Error de Cloudinary
```bash
# Verificar configuración de Cloudinary
python manage.py shell
>>> import cloudinary
>>> cloudinary.config()
```

### Problemas con Google OAuth
1. Verificar que las credenciales en `.env` sean correctas
2. Asegurar que la URL de callback esté configurada en Google Console
3. Verificar que `SITE_ID = 1` esté configurado en settings.py

## 📚 API y Endpoints

### Principales URLs de la aplicación:
- `/` - Página principal
- `/login/` - Iniciar sesión
- `/registrarse/` - Registro de usuarios
- `/productos/` - Listado de productos
- `/productos/<id>/` - Detalle de producto
- `/panel_admin/` - Panel de administración
- `/usuarios/` - Gestión de usuarios (admin)
- `/carrito/` - Gestión del carrito de compras
- `/api/` - Endpoints de API REST
- `/cloudinary/` - Gestión de imágenes Cloudinary

### Modelos Principales:
- **Usuario:** Gestión de usuarios con roles (Admin, Cliente, Vendedor)
- **Producto:** Catálogo de productos con categorías y stock
- **ImagenProducto:** Gestión de múltiples imágenes por producto
- **Carrito/ElementoCarrito:** Sistema de carrito de compras
- **Orden/OrdenItem:** Gestión de pedidos y ventas
- **CalificacionProducto:** Sistema de reseñas y valoraciones
- **Notificacion:** Sistema de notificaciones a usuarios
- **SolicitudVendedor:** Proceso de aprobación para vendedores

**Desarrollado con ❤️ para impulsar el talento estudiantil del SENA.** 🚀  

## 🧪 Testing

El proyecto incluye un conjunto de tests unitarios utilizando Pytest:

```bash
# Ejecutar todos los tests
python -m pytest

# Ejecutar tests con verbose
python -m pytest -v

# Ejecutar tests específicos
python -m pytest tienda_sena/tests/

# Generar reporte de cobertura
python -m pytest --cov=tienda_sena
```

## 🔧 Funcionalidades Avanzadas

### Sistema de Respaldo Automático
- **Script de respaldo:** `backup_cron.py` para automatizar respaldos de la base de datos
- **Logs de respaldo:** Registro detallado en `log_bk.txt`
- **Programación automática:** Compatible con cron jobs para respaldos periódicos

### Gestión de Imágenes Inteligente
- **Cloudinary Integration:** Almacenamiento en la nube para imágenes
- **Optimización automática:** Múltiples formatos (original, optimizada, miniatura)
- **Migración de imágenes:** Comando para migrar de almacenamiento local a Cloudinary

### Sistema de Notificaciones
- **Notificaciones en tiempo real:** Sistema completo de notificaciones para usuarios
- **Gestión de estado:** Notificaciones leídas/no leídas
- **Filtrado por usuario:** Notificaciones personalizadas según el rol

### Procesadores de Contexto
- **Categorías globales:** Disponibles en todos los templates
- **Colores dinámicos:** Sistema de colores para categorías
- **Notificaciones globales:** Acceso a notificaciones desde cualquier vista

---

# Guía de Trabajo con Git para Equipos

### Antes de Comenzar a Hacer Cambios

## 1. Antes de Empezar a Trabajar

### Mantener la rama `main` actualizada

```bash
# Cambiar a la rama main
git checkout main

# Traer los últimos cambios del servidor
git pull origin main
```

### Crear o actualizar tu rama de trabajo

```bash
# Cambiar a tu rama de trabajo
git checkout dark  # O el nombre de tu rama

# Fusionar los cambios recientes de main
git merge main     # O usa git rebase main si prefieres un historial más limpio
```

---

## 2. Trabajando y Subiendo Cambios

### Hacer cambios y subirlos

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin dark  # O el nombre de tu rama
```

---

## 3. ¿Qué Hacer Si Otra Persona Ya Subió Cambios?

Si alguien más modificó el mismo archivo y ya subió los cambios:

1. **Guarda tus cambios localmente**

   ```bash
   git add .
   git commit -m "Mis cambios locales"
   ```

2. **Trae los últimos cambios del servidor sin fusionarlos directamente**

   ```bash
   git fetch origin
   ```

3. **Integra los cambios recientes**

   - **Opción 1 (merge, más sencillo):**
     ```bash
     git merge origin/dark  # Si tu rama es "dark"
     ```
   - **Opción 2 (rebase, mantiene un historial más limpio):**
     ```bash
     git rebase origin/dark
     ```
>[!NOTE]
>La diferencia entre merge y rebase es que merge crea un nuevo commit de fusión, mientras que rebase aplica tus cambios sobre los cambios de la rama main, creando un historial más limpio.

4. **Resolver conflictos (si los hay)**

   - Si Git marca un conflicto, abre el archivo y edita las partes conflictivas.
   - Luego, marca el archivo como resuelto y continúa el proceso:
     ```bash
     git add archivo_conflictivo
     git rebase --continue  # Solo si usaste rebase
     ```

5. **Subir los cambios corregidos**

   ```bash
   git push origin dark
   ```
   - Si usaste `rebase`, podrías necesitar `git push --force`.

---


