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

## [v1.28.29-alpha.1] - 19-05-2025

### Added

- Añadir modelos y vistas para la gestión de usuarios, productos y órdenes, incluyendo mejoras en la interfaz y nuevas funcionalidades.

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
