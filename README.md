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

### 2. Instalar dependencias  
Asegúrate de tener un entorno virtual configurado y activo. Luego, instala las dependencias necesarias:  

```bash
pip install -r requirements.txt
```

Si las dependencias **Pillow** no están en el archivo `requirements.txt`, instálalas manualmente:  

```bash
pip install pillow
```

### 3. Migraciones de base de datos  
```bash
python manage.py migrate  
```

### 4. Ejecutar el servidor  
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


