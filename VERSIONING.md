## Versionamiento del Proyecto

Este proyecto sigue las reglas de [**Semantic Versioning (SemVer)**](https://semver.org/) para gestionar el control de versiones. Esto asegura que las actualizaciones y cambios sean fáciles de comprender y seguir por el equipo de desarrollo y los usuarios.

### Convenciones de Versionado

- **MAJOR**: Cambios incompatibles con versiones anteriores (breaking changes).
- **MINOR**: Nuevas características que son compatibles con versiones anteriores.
- **PATCH**: Correcciones de errores o mejoras menores que no afectan la compatibilidad.

## Reglas para la numeración

1. Comienza en `1.0.0` cuando se lance la primera versión pública estable.
2. Incrementa:
   - **MAJOR** cuando introduces cambios incompatibles con versiones anteriores.
   - **MINOR** cuando añades nuevas funcionalidades compatibles con versiones anteriores.
   - **PATCH** cuando arreglas errores o realizas mejoras internas.
3. Utiliza etiquetas de **pre-lanzamiento** para versiones en desarrollo, como:
   - `alpha`: Versión en desarrollo inicial, puede ser inestable. Ejemplo: `1.2.0-alpha`.
   - `beta`: Versión más estable, pero puede contener errores. Ejemplo: `1.2.0-beta`.
   - `rc` (release candidate): Candidata a ser estable si no se encuentran errores. Ejemplo: `1.2.0-rc`.

### Cómo usar etiquetas de pre-lanzamiento

1. Añade una etiqueta de pre-lanzamiento al final de la versión, separada por un guion (`-`).
2. Puedes combinar etiquetas con números secuenciales para identificar iteraciones, por ejemplo:
   - `1.2.0-alpha.1`
   - `1.2.0-beta.2`
   - `1.2.0-rc.3`

3. Actualiza las etiquetas según el progreso del desarrollo:
   - **Alpha** → **Beta** → **RC** → Versión estable (`MAJOR.MINOR.PATCH`).

## Ejemplos

- `1.0.0`: Primera versión pública.
- `1.1.0`: Se añade una nueva funcionalidad compatible.
- `1.1.1`: Corrección de un error menor.
- `2.0.0-alpha.1`: Primera iteración de pre-lanzamiento para la versión 2.0.
- `2.0.0-rc.1`: Versión candidata a ser estable para la 2.0.

> [!IMPORTANT]
> ## Registro de versiones
> Este archivo **NO** incluye un historial de cambios. Para un registro detallado, consulta el archivo [CHANGELOG.md].
