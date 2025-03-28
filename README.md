# TIENDA SENA 🛍️  

**Tienda Sena** es un ecommerce creado para los aprendices del SENA, permitiéndoles promocionar y vender sus proyectos o emprendimientos. La plataforma brinda un espacio seguro y accesible para la gestión de sus negocios digitales.  

## 🚀 Características  

- Creación de tiendas virtuales personalizadas  
- Publicación y gestión de productos  
- Procesos de pago seguros  
- Valoraciones y comentarios de clientes      

## 🛠️ Tecnologías Utilizadas  

- **Backend:** Django 5.1.1 (Python 3.12.2)  
- **Frontend:** HTML, CSS, JavaScript  
- **Autenticación:** Django Authentication  
- **Notificaciones:** Firebase   

## 📦 Instalación y Configuración  

### 1. Clonar el repositorio  
```bash
git clone https://github.com/Ausuga3/tienda_sena_django.git
cd tienda-sena  
```

### 2. Migraciones de base de datos  
```bash
python manage.py migrate  
```

### 3. Ejecutar el servidor  
Ubícate en la carpeta principal del proyecto, donde está el archivo `manage.py`, y ejecuta:  

En **Linux**:  
```bash
python3 manage.py runserver  
```
En **Windows**:  
```bash
python manage.py runserver  
```

## 📂 Estructura del Proyecto  

El proyecto cuenta con varias secciones y plantillas diseñadas para una experiencia de usuario intuitiva:  

- **Index** – Página principal  
- **Login** – Inicio de sesión  
- **Registrar** – Registro de nuevos usuarios  
- **Productos** – Listado de productos disponibles  

## 💻 Requerimientos del Sistema  

Para ejecutar esta plataforma web de manera óptima, tu PC debe cumplir con los siguientes requisitos:  

### 🖥️ Hardware  
- **Procesador:** Intel Core i3 o equivalente  
- **Memoria RAM:** 4 GB o más  
- **Almacenamiento:** 500 MB de espacio disponible (para archivos temporales y caché)  

### 🛠️ Software  
- **Navegador:** Última versión de Google Chrome, Mozilla Firefox o Microsoft Edge  
- **Sistema Operativo:** Windows 10, macOS 10.14+, Linux (Ubuntu 18.04 o superior)  
- **Conexión a Internet:** 10 Mbps o más para una experiencia fluida

**Desarrollado con ❤️ para impulsar el talento estudiantil del SENA.** 🚀  

---

# Guía de Trabajo con Ramas y Sincronización

### Antes de Comenzar a Hacer Cambios

### Mantener la rama main actualizada (antes de trabajar)

1. Cambiar a la rama `main`:
   ```bash
   git checkout main
   ```

2. Actualizar la rama `main`:
   ```bash
   git pull origin main
   ```

### Integrar los últimos cambios de main a tu rama de trabajo

3. Cambiar a tu rama de trabajo:
   ```bash
   git checkout dark
   # O el nombre de la rama en la que trabajes.
   ```

4. Obtener los últimos cambios de la rama `main` y fusionarlos con `merge`:
   ```bash
   git merge main
   # O usar rebase si prefieres:
   # git rebase main
  
  >[!NOTE]
  >La diferencia entre merge y rebase es que merge crea un nuevo commit de fusión, mientras que rebase aplica tus cambios sobre los cambios de la rama main, creando un historial más limpio.


5. Realizar cambios, añadir y confirmar:
   ```bash
   git add .
   git commit -m "Descripción de los cambios"
   git tag -a v1.1.0-alpha.1 -m "v1.1.0-alpha.1"
   ```

6. Subir los cambios a la rama remota:
   ```bash
   git push -u origin dark --tags
   # O el nombre de la rama en la que trabajes.
   ```
Recuerda resolver cualquier conflicto que pueda surgir durante el merge o rebase.
