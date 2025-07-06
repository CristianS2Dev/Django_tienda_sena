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

- **Backend:** Django 5.1.2 (Python 3.12+)
- **Base de datos:** SQLite3 (desarrollo) / PostgreSQL/MySQL (producción)
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap Icons
- **Autenticación:** Django Allauth (incluye Google OAuth)
- **Procesamiento de imágenes:** Pillow/Pillow-SIMD
- **Emails:** Django Email System
- **Formularios:** Django Crispy Forms   

## 📦 Instalación y Configuración  

### Prerrequisitos
- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git

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
- Django 5.1.2
- Pillow (procesamiento de imágenes)
- Django Allauth (autenticación social)
- Django Crispy Forms
- Django Humanize
- Whitenoise (archivos estáticos)

### 4. Configurar variables de entorno (Opcional)
Crea un archivo `.env` en la raíz del proyecto para configuraciones sensibles:
```env
SECRET_KEY=tu_clave_secreta_aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
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

### Optimización de Imágenes
El sistema optimiza automáticamente las imágenes subidas, pero puedes ejecutar optimizaciones manuales:
```bash
python manage.py optimizar_imagenes
```

### Comandos de Administración
```bash
# Crear superusuario
python manage.py createsuperuser

# Limpiar sesiones expiradas
python manage.py clearsessions

# Recopilar archivos estáticos para producción
python manage.py collectstatic
```

## 🏗️ Estructura del Proyecto  

```
Django_tienda_sena/
├── tienda/                     # Configuración principal del proyecto
│   ├── settings.py            # Configuraciones de Django
│   ├── urls.py                # URLs principales
│   └── wsgi.py                # Configuración WSGI
├── tienda_sena/               # Aplicación principal
│   ├── models.py              # Modelos de base de datos
│   ├── views.py               # Vistas principales
│   ├── urls.py                # URLs de la aplicación
│   ├── templates/             # Templates HTML
│   │   ├── index.html         # Página principal
│   │   ├── login.html         # Inicio de sesión
│   │   ├── registrarse.html   # Registro de usuarios
│   │   ├── productos/         # Templates de productos
│   │   ├── usuarios/          # Templates de usuarios
│   │   └── administrador/     # Panel de administración
│   ├── static/                # Archivos estáticos (CSS, JS, imágenes)
│   ├── management/            # Comandos personalizados de Django
│   └── migrations/            # Migraciones de base de datos
├── media/                     # Archivos subidos por usuarios
│   ├── productos/             # Imágenes de productos
│   └── usuarios/              # Imágenes de perfiles
├── requirements.txt           # Dependencias de Python
├── package.json              # Dependencias de Node.js
└── manage.py                  # Script de gestión de Django
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
- **Google OAuth:** Inicio de sesión con cuenta de Google
- **Registro tradicional:** Con verificación por email
- **Recuperación de contraseña:** Sistema de códigos de verificación

### Gestión de Productos
- **Categorías dinámicas:** Sistema flexible de categorización
- **Filtros avanzados:** Por precio, categoría, vendedor
- **Optimización de imágenes:** Conversión automática a WebP
- **Múltiples imágenes:** Soporte para galerías de productos

### Carrito de Compras
- **Persistencia:** Mantiene productos entre sesiones
- **Actualizaciones en tiempo real:** JavaScript asíncrono
- **Cálculos automáticos:** Subtotales, impuestos, totales
- **Limpieza automática:** Eliminación de carritos antiguos  

## 💻 Requerimientos del Sistema  

### 🖥️ Para Desarrollo
- **Python:** 3.12 o superior
- **Node.js:** 16.0 o superior (para dependencias frontend)
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
SECRET_KEY=clave_secreta_muy_segura
DEBUG=False
ALLOWED_HOSTS=tudominio.com,www.tudominio.com
DATABASE_URL=postgresql://usuario:password@localhost/tienda_sena
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_email@gmail.com
EMAIL_HOST_PASSWORD=tu_password_de_aplicacion
```

### Comandos de Despliegue
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --noinput

# Crear migraciones y aplicarlas
python manage.py makemigrations
python manage.py migrate

# Crear superusuario (primera vez)
python manage.py createsuperuser
```

## 🐛 Solución de Problemas Comunes

### Error de Pillow
```bash
# Si hay problemas con Pillow en Windows
pip uninstall Pillow
pip install Pillow

# Para mejor rendimiento (opcional)
pip install Pillow-SIMD
```

### Error de migraciones
```bash
# Resetear migraciones (solo en desarrollo)
python manage.py migrate tienda_sena zero
python manage.py makemigrations tienda_sena
python manage.py migrate
```

### Error de archivos estáticos
```bash
# Recopilar archivos estáticos
python manage.py collectstatic --clear
```

## 📚 API y Endpoints

### Principales URLs de la aplicación:
- `/` - Página principal
- `/login/` - Iniciar sesión
- `/registrarse/` - Registro de usuarios
- `/productos/` - Listado de productos
- `/panel_admin/` - Panel de administración
- `/usuarios/` - Gestión de usuarios (admin)
- `/carrito/` - Gestión del carrito de compras

**Desarrollado con ❤️ para impulsar el talento estudiantil del SENA.** 🚀  

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


