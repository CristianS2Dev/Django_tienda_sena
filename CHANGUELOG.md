> [!TIP]
> ### Cómo llenar el *CHANGELOG*
> El CHANGELOG.md debe registrar los cambios realizados en el proyecto de forma clara y estructurada. Usa este formato para mantener el orden:
> ## [Versión] - Fecha
> ### Added
> - Descripción de nuevas funcionalidades o recursos añadidos.
> ### Fixed
> - Descripción de errores solucionados.
> ### Changed
> - Descripción de cambios en funcionalidades existentes.
> ### Removed
> - Descripción de funcionalidades o recursos eliminados.
> ### Note
> - Notas adicionales sobre los cambios realizados.
---

### CHANGELOG
---

## [v1.39.37-alpha.1] - 11-07-2025

### Added
- Nueva migración para el campo de categoría de productos
- Validaciones mejoradas para productos en las vistas

### Changed
- Modificado el enlace del botón de login para mejor funcionalidad
- Actualizada la estructura de la base de datos para productos

### Removed
- Eliminado archivo `.env.example` para simplificar la configuración
- Limpieza de respaldos antiguos de la base de datos

### Fixed
- Corregidas validaciones de productos en el sistema
- Mejorada la gestión de categorías de productos

### Note
- Esta versión incluye cambios en la estructura de base de datos que requieren migración
- Se recomienda hacer backup antes de aplicar las migraciones

---
## [v1.37.35-alpha.1] - 10-07-2025

### Added

- Se implementan validaciones robustas en la función `actualizar_perfil` para mejorar la seguridad y experiencia del usuario:
  - Validación de campos obligatorios (nombre y apellido no pueden estar vacíos)
  - Validación de espacios en blanco usando `.strip()` para limpiar datos de entrada
  - Validación que previene números en nombres y apellidos usando expresiones regulares
  - Validación opcional pero estricta para documento de identidad (solo números, 7-15 dígitos)
  - Validación opcional pero estricta para número de contacto (solo números, 7-15 dígitos)
- Se mantiene la funcionalidad existente de procesamiento de imágenes de perfil con optimización

### Changed

- Se mejora la función `actualizar_perfil` con validaciones consistentes siguiendo el mismo patrón de otras funciones del sistema
- Se optimiza el manejo de datos de entrada eliminando espacios innecesarios antes del procesamiento

### Fixed

- Se previenen errores de entrada de datos inválidos en la actualización de perfil de usuario
- Se mejora la retroalimentación al usuario con mensajes de error específicos y claros
- Se corrige el manejo de campos opcionales para permitir valores vacíos válidos

### Security

- Se fortalece la validación de entrada para prevenir inyección de datos maliciosos
- Se implementa sanitización de datos de entrada eliminando espacios en blanco
- Se añade validación de formato para campos numéricos (documento y contacto)

### Note

- Las validaciones siguen el mismo estilo y patrón implementado en otras funciones como `login` y `registrarse`
- Los campos documento y contacto son opcionales pero si se proporcionan deben cumplir con el formato establecido

---
## [v1.36.34-alpha.1] - 10-07-2025

### Added
- **Sistema de Respaldo Automatizado (Backup)**:
  - Nuevo script `backup_cron.py` para automatización de copias de seguridad
  - Funcionalidad de compresión de base de datos a formato ZIP
  - Envío automático de backups por correo electrónico
  - Configuración de cron jobs para respaldos programados
  - Log de actividades de backup en `log_bk.txt`
- **Comandos de Gestión Django**:
  - Comando `reset_productos.py` para reinicializar productos con datos realistas
  - Comando `optimizar_categorias.py` para optimización del sistema de categorías
  - Estructura mejorada de comandos de gestión en `management/commands/`
- **Optimización de Imágenes de Productos**:
  - Sistema automatizado de optimización de imágenes existentes
  - Conversión masiva a formato WebP para mejor rendimiento
  - Reorganización de carpetas de imágenes (`optimizadas/`, `originales/`, `miniaturas/`)
  - Limpieza automática de imágenes duplicadas y huérfanas

### Changed
- **Estructura de Base de Datos**:
  - Migración 0021 para implementación de nuevo sistema de categorías
  - Migración 0022 para revertir cambios de categorías cuando sea necesario
  - Optimización de consultas y relaciones en modelos
- **Sistema de Gestión de Archivos Media**:
  - Reorganización completa de la carpeta `media/productos/`
  - Implementación de estructura jerárquica para imágenes
  - Mejoras en el sistema de limpieza de archivos no utilizados
- **Context Processors**:
  - Optimización del procesador de contexto para categorías
  - Mejoras en el rendimiento de consultas de notificaciones de usuario
  - Reducción de carga en plantillas mediante procesamiento optimizado

### Fixed
- **Limpieza de Archivos de Desarrollo**:
  - Eliminación de archivos temporales y de prueba (`.coverage`, `t copy.py`)
  - Limpieza de imágenes duplicadas y versiones obsoletas
  - Corrección de rutas de archivos en configuraciones
- **Optimización de Rendimiento**:
  - Resolución de problemas de memoria con imágenes grandes
  - Mejoras en la carga de productos con múltiples imágenes
  - Optimización de consultas de base de datos para listados

### Security
- **Gestión de Respaldos**:
  - Implementación segura de envío de archivos por correo
  - Validación de rutas y permisos en scripts de backup
  - Configuración segura de cron jobs para tareas automatizadas

### Performance
- **Optimización de Imágenes**:
  - Conversión automática a WebP para reducir tamaño de archivos hasta 80%
  - Sistema de miniaturas optimizado para carga rápida
  - Lazy loading mejorado para imágenes de productos
- **Base de Datos**:
  - Optimización de consultas relacionadas con productos e imágenes
  - Indexación mejorada para búsquedas de categorías
  - Reducción significativa en tiempo de carga de listados

### Infrastructure
- **Automatización**:
  - Sistema completo de backup automatizado con cron
  - Scripts de mantenimiento para limpieza periódica
  - Logs detallados para monitoreo de operaciones automáticas

### Note
- **Backup Importante**: El sistema ahora incluye respaldos automáticos diarios
- **Optimización Masiva**: Se recomienda ejecutar `reset_productos.py` para beneficiarse de las optimizaciones
- **Rendimiento Mejorado**: Mejoras significativas en velocidad de carga de imágenes y productos

---
## [v1.35.33-alpha.1] - 06-07-2025

### Added
- **Sistema de Recuperación de Contraseña Completo**:
  - Nueva vista `ajax_validar_codigo` para validar códigos de verificación de 6 dígitos
  - Nueva vista `ajax_restablecer_password` para cambiar la contraseña después de la validación
  - Proceso de recuperación de contraseña en 3 pasos: envío de código, validación y restablecimiento
  - Interfaz de usuario mejorada con indicadores de progreso y formularios paso a paso
  - Validación en tiempo real de requisitos de contraseña (mayúsculas, minúsculas, números, caracteres especiales)
  - Funcionalidad de reenvío de código de verificación
  - Indicadores de carga (spinners) en todos los botones durante las operaciones

### Changed
- **Template `olvidar_contraseña.html`**:
  - Actualizado completamente para soportar flujo de 3 pasos
  - Mejorada la experiencia de usuario con campos de código de verificación individuales
  - Añadidos toggles para mostrar/ocultar contraseñas
  - Implementada navegación automática entre campos de código
  - Mejorados los textos a español y la usabilidad general
- **Rutas URL**:
  - Agregadas nuevas rutas: `ajax/validar-codigo/` y `ajax/restablecer-password/`
  - Configuración completa del flujo de recuperación de contraseña
- **Estilos CSS**:
  - Añadidos estilos para campos de verificación con estados visual (llenado, enfoque)
  - Implementados estilos de carga con animaciones CSS
  - Mejorada la experiencia visual de los botones con estados de carga

### Fixed
- **Importaciones y Dependencias**:
  - Agregada importación de `make_password` desde `django.contrib.auth.hashers`
  - Corregidas todas las dependencias necesarias para el funcionamiento completo
- **Validaciones de Seguridad**:
  - Implementada validación completa de contraseñas utilizando la función existente `validar_contraseña`
  - Añadida limpieza del código de verificación después del restablecimiento exitoso
  - Mejorada la seguridad con validaciones tanto en frontend como backend

### Security
- **Proceso de Verificación**:
  - Códigos de verificación de 6 dígitos almacenados de forma segura
  - Validación de códigos en el servidor antes de permitir cambio de contraseña
  - Limpieza automática de códigos de verificación después del uso
  - Validación de todos los campos requeridos antes del procesamiento

### Performance
- **Experiencia de Usuario**:
  - Interfaz asíncrona con feedback inmediato al usuario
  - Indicadores de carga para mejorar la percepción de velocidad
  - Navegación automática entre campos para mayor fluidez

### Note
- **Funcionalidad Completa**: El sistema de recuperación de contraseña ahora está completamente funcional con validación de código
- **Mejores Prácticas**: Implementado siguiendo las mejores prácticas de seguridad y UX
- **Responsive**: La interfaz es completamente responsive y accesible

---
## [v1.34.32-alpha.1] - 06-07-2025

### Added
- **Autenticación Social con Django Allauth**:
  - Integración completa de django-allauth para autenticación con Google
  - Botón de "Continuar con Google" en la página de login con diseño mejorado
  - Configuración automática de OAuth2 para Google
  - Archivo `signals.py` para manejar el login de usuarios y creación de cuentas sociales
  - Script de configuración automatizada `setup_google_auth.bat` para instalación fácil
  - Archivos `.env` y `.env.example` para configuración de credenciales OAuth2
- **Mejoras en la Página de Inicio**:
  - Categorías dinámicas en `index.html` que muestran productos reales
  - Enlaces directos a productos por categoría desde la página principal
  - Contador de productos por categoría actualizado dinámicamente

### Changed
- **Configuración de Django**:
  - Actualizado `settings.py` con configuraciones completas de allauth
  - Agregados backends de autenticación para múltiples métodos de login
  - Configurado SITE_ID y middleware requeridos por allauth
  - Actualizada configuración de templates para incluir context processors de allauth
- **URLs y Enrutamiento**:
  - Modificado `urls.py` para incluir rutas de allauth (`/accounts/`)
  - Integradas URLs de autenticación social en el sistema de enrutamiento
- **Templates y UI**:
  - Mejorado `login.html` con botón de Google y estilos actualizados
  - Añadidos iconos de Bootstrap para mejor experiencia visual
  - Integradas las etiquetas de socialaccount en los templates

### Fixed
- **Flujo de Autenticación Mejorado**:
  - Corregido el flujo de login para soportar múltiples métodos de autenticación
  - Mejorado el manejo de errores en el proceso de login social
  - Optimizada la experiencia de usuario en el proceso de registro/login

### Security
- **OAuth2 y Seguridad**:
  - Implementada autenticación OAuth2 con Google siguiendo mejores prácticas
  - Configuración segura de variables de entorno para credenciales
  - Validaciones adicionales para cuentas de redes sociales

### Performance
- **Carga Dinámica de Contenido**:
  - Optimizada la carga de categorías en la página principal
  - Mejorado el rendimiento de consultas para mostrar productos por categoría

### Note
- **Configuración Requerida**: Se debe configurar `GOOGLE_OAUTH2_CLIENT_ID` y `GOOGLE_OAUTH2_CLIENT_SECRET` en el archivo `.env`
- **Script de Instalación**: Usar `setup_google_auth.bat` para configuración automática del entorno
- **Dependencias**: Se requiere instalar django-allauth según `requirements.txt`

---
## [v1.33.31-alpha.1] - 06-07-2025

### Added
- **Autenticación Social con Google OAuth2**:
  - Integración completa de django-allauth para autenticación social
  - Botón de "Continuar con Google" en la página de login
  - Configuración automática de cuentas de usuario desde Google
  - Manejo de señales para usuarios de redes sociales
- **Campo de Estado de Usuario**:
  - Nuevo campo `activo` en el modelo Usuario para control de cuentas
  - Migración 0020 para agregar el campo activo
- **Mejoras en la Página de Inicio**:
  - Categorías dinámicas que muestran cantidad real de productos
  - Enlaces directos a productos por categoría
  - Interfaz mejorada para explorar categorías
- **Configuración de Entorno**:
  - Archivos .env y .env.example para variables de entorno
  - Script automatizado de configuración (setup_google_auth.bat)
  - Configuración de zona horaria a América/Bogotá

### Changed
- **Configuración de Django**:
  - Actualizada configuración de INSTALLED_APPS para incluir allauth
  - Configurados authentication backends para múltiples métodos de login
  - Mejorada configuración de templates y middleware
  - Actualizada configuración de idioma a español
- **URLs y Routing**:
  - Agregadas rutas de allauth para autenticación social
  - Configurado manejo de archivos media en desarrollo
- **Templates y UI**:
  - Mejorado diseño del login con botón de Google
  - Actualizados estilos CSS y JavaScript
  - Mejoras en responsive design y usabilidad

### Fixed
- **Merge Conflicts Resueltos**:
  - Combinados cambios de autenticación social con mejoras de UI
  - Resueltos conflictos en base de datos manteniendo datos locales
  - Solucionados conflictos de dependencias en migraciones

### Security
- **Autenticación Mejorada**:
  - Implementado OAuth2 con Google para mayor seguridad
  - Configuración PKCE habilitada para mayor protección
  - Validaciones adicionales para cuentas de redes sociales

### Note
- **Configuración Requerida**: Es necesario configurar las credenciales de Google OAuth2 en el archivo .env
- **Migraciones**: Se requiere ejecutar `python manage.py migrate` para aplicar la nueva migración de usuario activo

---

## [v1.32.30-alpha.1] - 06-07-2025

### Added
- Se agregan botones de "Agregar Productos" en múltiples ubicaciones para mejorar la experiencia del usuario:
  - Botón en la lista de productos (`listar_productos.html`) 
  - Botón en el template base de productos (`_productos.html`)
  - Botón condicional según el rol del usuario (vendedores y administradores)
- Se implementa la funcionalidad `mostrar_boton_agregar` en las vistas para controlar la visibilidad de botones
- Se mejora la gestión de imágenes de productos con nuevas funcionalidades:
  - Vista `gestionar_imagenes_producto` para administración avanzada de imágenes
  - Función para establecer imagen principal
  - Función para eliminar imágenes individuales
- Se agrega optimización automática de imágenes (conversión a WebP, redimensionamiento, generación de miniaturas)
- Se implementan validaciones mejoradas para el formulario de productos:
  - Validación de cantidad máxima de imágenes (5 por producto)
  - Validación de formato y tamaño de archivos
  - Validación de precios y descuentos
- Se añade sistema de breadcrumbs para mejor navegación
- Se mejora la interfaz del carrito de compras con botones de cantidad y eliminación

### Changed

- Se refactoriza la estructura de templates para mejor organización del código
- Se mejora el diseño responsive de las tarjetas de productos
- Se actualiza el panel de administrador con nuevas estadísticas y métricas
- Se optimiza la carga de imágenes con lazy loading y formatos WebP
- Se mejora la experiencia de usuario en el proceso de agregar/editar productos

### Fixed

- Se corrigen errores en la validación de formularios de productos
- Se arreglan problemas de redirección después de agregar/editar productos
- Se solucionan errores de sintaxis en templates
- Se corrigen problemas de permisos de usuario para diferentes roles
- Se arreglan errores en la actualización de perfil de usuario
- Se solucionan problemas de responsive design en dispositivos móviles
- Se corrigen errores en la gestión del carrito de compras
- Se arreglan problemas de optimización de imágenes que causaban errores de memoria

### Security

- Se mejoran las validaciones de entrada para prevenir inyección de código
- Se añaden decoradores de autenticación y autorización más robustos
- Se implementa validación de tipos de archivo para imágenes

### Performance

- Se optimiza automáticamente el tamaño de imágenes subidas (conversión a WebP)
- Se implementa compresión de imágenes para reducir el uso de ancho de banda
- Se mejora la carga de productos con paginación optimizada

---

## [v1.31.30-alpha.1] - 06-07-2025

### Added

- Se agregan botones para agregar productos

### Fixed

- Se arreglan errores de productos
- Se arreglan errores de actualizar perfil

---

## [v1.30.29-alpha.1] - 09-05-2025


### Changed

- Se crea el modelo de Calificaciones
- Se crea la vista de Calificaciones

---

## [v1.29.29-alpha.1] - 19-05-2025


### Changed

- Se actualizan los docstrings de los modelos para mayor claridad.
- Se mejora la configuración de Django y las URLs para incluir la documentación de admin.

---

## [v1.28.29-alpha.1] - 19-05-2025

### Added

- Añadir modelos y vistas para la gestión de usuarios, productos y órdenes, incluyendo mejoras en la interfaz y nuevas funcionalidades.

---


## [v1.27.28-alpha.2] - 19/05/2025

### Added

- Se agrega la vista de recuperar contraseña
- Se integra para la vista el enviar correo para recuperar contraseña

---

## [v1.26.28-alpha.2] - 26-04-2025

### Added

- Se crea el modelo `SolicitudVendedor` para gestionar solicitudes de certificación de vendedores.
- Se agregan vistas y templates para que los usuarios puedan solicitar certificación y los administradores puedan gestionarlas.
- Se agregan breadcrumbs para mejorar la navegación en las nuevas vistas.

### Removed

- Se elimina el campo `certificado` del modelo `Usuario`.

### Changed

- Se actualizan las migraciones para reflejar los cambios en los modelos.

---

## [v1.26.27-alpha.1] - 25-04-2025

### Added

- Validación en el modelo Producto para asegurar que los descuentos no excedan el 100% y que los precios finales no sean negativos.
- Nuevo filtro personalizado para agrupar productos en el carrusel.
- Se mejora la interfaz de usuario en los formularios de login y registro agregando la opción de mostrar/ocultar contraseña.

### Changed

- Refactorización del template `_productos.html` para mejorar el layout.
- Se agrega el nuevo template `_productos_carrusel.html` para una mejor visualización de productos.
- Mejoras en los templates `index.html` y `listar_productos.html` para una mejor experiencia de usuario.
- Actualización de CSS para mejorar el estilo y la responsividad de las tarjetas y carruseles de productos.

### Fixed

- Mejor manejo de errores y retroalimentación al usuario en las vistas de registro e inicio de sesión.

---

## [v1.25.26-alpha.1] - 24-04-2025

### Fixed

- Se corrige los permisos de las vistas del administrador para que sean accesibles solo por el usuario correspondiente.

## [v1.25.25-alpha.1] - 24-04-2025

### Changed

- Refactorización de la actualización de perfil de usuario para incluir la gestión de dirección principal.
- Mejora en el manejo y visualización de categorías de productos en las vistas y filtros.

---

## [v1.25.24-alpha.1] - 24-04-2025

### Added

- Se agregan modelos para la gestión de direcciones de usuario, incluyendo operaciones CRUD.
- Se añade funcionalidad para establecer dirección principal.
- Se crea comando para limpiar carritos de compra huérfanos con más de 7 días.
- Se mejora el template del perfil de usuario para mostrar y gestionar direcciones.
- Se agregan breadcrumbs para mejor navegación en la gestión de direcciones.
- Se actualiza el panel de administración para gestionar los nuevos modelos de direcciones y órdenes.

### Changed

- Se actualizan las vistas para soportar la gestión de direcciones.

### Fixed

- Se añade validación para los campos de dirección.

---


## [v1.24.23-alpha.1] - 21-04-2025

### Added

- Se agregan los modelos `Orden` y `OrdenItem` para la gestión de pedidos.

### Changed

- Se actualiza la vista `pagar_carrito` para crear órdenes y sus ítems al realizar el pago.
- Se mejora el template del carrito para mostrar un mensaje cuando está vacío.


---


## [v1.24.22-alpha.1] - 4-21-2025

### Changed

- Se agrega certificado al models

---

## [v1.23.22-alpha.1] - 4-21-2025

### Changed

- Refactorización de la funcionalidad de listado y filtrado de productos; actualización de templates y estilos para mejorar la experiencia de usuario

---

## [v1.21.21-alpha.1] - 4-11-2025

### Added

- Se agrega funcionalidad para cambiar contraseña



### Changed

- Se cambia validacion de contraseña y se convierte en una funcion

---
## [v1.20.21-alpha.1] - 4-11-2025

### Changed

- Se corrige la vista de sobre nosotros el responsive.

## [v1.20.20-alpha.1] - 4-10-2025

### Added

- Se agrega funcionalidad para el buscador de productos
- Se crea la vista del buscador de productos


### Changed

- Se centra el buscador
- Se mejora el diseño del buscador

---

### [v1.19.19-alpha.1] - 4-10-2025

### Added

- Se agrega vista del sobre nosotros

---

### [v1.19.18-alpha.1] - 4-10-2025

### Added

- Se agrega template de actualizar datos.
- Se agrega funcion para actualizar datos.


### Fixed

- Se mejora navbar para cerrar secion directamente.

---

### [v1.18.18-alpha.1] - 4-08-2025

### Fixed
- Se corrigen errores de sintaxis 

### Note

- Corregir errores con las ramas

---

### [v1.18.17-alpha.1] - 4-08-2025

### Added

- Se agrega validaciones para el carrito de compras
- Se agrega validacion para la incriptacion de la contraseña

### Fixed

- Se corrigen errores de sintaxis
- Se corrigen errores con el carrito de compras


---

### [v1.17.19-alpha.1] - 4-08-2025

### Added

- Se agrega validaciones para la imagen de los productos
- Se agrega validacion para escanear la imagen de los productos 

### Fixed

- Se corrigen errores de sintaxis

---

### [v1.16.18-alpha.1] - 4-08-2025

### Added

- Se agregan validaciones para el correo y eliminacion de usuarios



### [v1.15.18-alpha.1] - 4-08-2025

### Added

- Se agrega la vista `carrito` para el usuario
- Se agregan validaciones para el registro de productos

### Fixed

- Se corrigen errores de sintaxis
- Se corrigen errores para el registro de productos


---

## [v1.14.17-alpha.1] - 4-06-2025

### Fixed

- Se corrigen errores de sintaxis
- Se corrige la vista index

---


## [v1.13.16-alpha.1] - 4-06-2025

### Fixed

- Se corrigen errores de sintaxis
- Se corrige la vista index

---

## [v1.13.15-alpha.1] - 4-06-2025

### Fixed

- Se corrigen errores de sintaxis
- Se corrige la vista de los productos
- Se corrige la vista index

---

## [v1.13.14-alpha.1] - 4-04-2025


### Fixed

- Se corrigen errores de sintaxis
- Se corrige la vista de los productos

---

## [v1.13.13-alpha.1] - 3-04-2025

### Fixxed

- Se complementa la vista Tienda

---

## [v1.12.13-alpha.1] - 1-04-2025

### Fixed

- Se corrigen errores


## [v1.12.11-alpha.1] - 1-04-2025

### Fixed

- Se modifican los requisitos de registro
- Se muestra el Rol en los datos de la cuenta

---

## [v1.12.10-alpha.1] - 1-04-2025

### Added

- Se agrega la vista `detalle_producto_admin`  

---

### [v1.11.9-alpha.1] - 1-04-2025


### Fixed

- Se corrigen errores con el models.

### Add

- Se agregan modales al perfil del usuario

### [v1.10.8-alpha.1] - 30-03-2025

### Note

- Arreglar las fotos de los productos


### Fixed

- Se corrigen errores con el sidebar


---

## [v1.9.7-alpha.1] - 30-03-2025

### Fixed

- Se corrigen errores con el perfil y el sidebar

---

## [v1.9.6-alpha.1] - 30-03-2025

### Added

- Se agrega el archivo `.gitignore` para ignorar archivos innecesarios

### Changed

- Se mejora el banner de la vista de productos

### Fixed

- Se corrigen errores con los productos

### Notes

- Falta mejorar el diseño de la vista de editar y agregar productos
---

### [v1.9.5-alpha.1] - 30-03-2025

### Added

- Se agrego la vista Perfil

---

### [v1.8.5-alpha.1] - 30-03-2025

### Chaanged

- Se cammbio la vista de agregar productos

### Fixed

- Se corrigen errores con los productos y categorias
- Se corrigen errores con el precio y oferta de los productos

---

### [v1.8.4-alpha.1] - 30-03-2025

### Added

- Se agrega panel administrador
- Se sidebar admin y usuarios

### Fixed

- Se cambian de lugar hipervinculos
- Se mejora la lista de usuarios y productos

### Notes

- Tanto el panel administrador como las vistas de usuarios y productos faltan por hacer responsives.
---

### [v1.7.3-alpha.1] - 30-03-2025

### Added

- Se agrega funcionalidad para las categorias de los productos

### Fixed

- Se corrigen errores con los productos, categorias y el modelo

---

## [v1.6.2-alpha.1] - 29-03-2025

### Fixed

- Se corrigen errores con los productos

---

# [v1.6.1-alpha.1] - 28-03-2025

### Added

- Se agrega el CRUD de Usuarios

### Fixed

- Se re diseño el navbar
- Se corrige el models.Usuario

---

## [v1.5.1-alpha.1] - 28-03-2025

### Added

- Se agrega el CRUD de los productos

### Fixed

- Se corrigen errores de sintaxis

---

## [v1.4.0-alpha.1] - 28-03-2025

### Added

- se agrega archivo `utils.py`
- se agrega carpeta `media`
- se configura setting
- se agregan vistas
- Se agregan botones al Base `Registrar, Iniciar Session`

---

## [v1.3.0-alpha.1] - 28-03-2025

### Added
- se agrega archivo js

### Changed
- Se completa el landin page con bootstrap y css

---

## [v1.2.0-alpha.1] - 28-03-2025

### Added

- Se agrega html del index
- se agrega css del index, login, registrarse


### Note

- Falta bootstrap en section 2 y 4

---
## [v1.1.0-alpha.1] - 27-03-2025

### Added

- Se agrega el login y el registro de usuarios
- Se crea el modelo de usuario

### Note

- No esta funcional el botsrap en el login y el registro

---

## [v1.0.0-alpha.1] - 27-03-2025

### Added
- se agrega carpeta static
- se agrega bootstrap al proyecto
- se agrega la base con el footer y el navbar
- se inicia el landin page

### Notes
- el navbar y el footer solo son prototipos
 ----
