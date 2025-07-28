# Guía para Agregar Nuevas Tarjetas de Equipo

## Estructura de Tarjeta Estándar

Para mantener la consistencia visual y funcional, usa esta estructura cuando agregues nuevos miembros del equipo:

```html
<!-- Team Member [NÚMERO] -->
<div class="col-lg-4 col-md-6">
    <div class="team-card h-100">
        <!-- Contenedor de imagen con altura fija -->
        <div class="team-image-container">
            <img src="{% static 'assets/[NOMBRE_IMAGEN]' %}" alt="Foto de [NOMBRE_COMPLETO]" class="team-image">
        </div>
        <!-- Contenido de la tarjeta -->
        <div class="card-content p-4">
            <div>
                <span class="role-tag">[CARGO]</span>
                <h5 class="mb-3">[NOMBRE_COMPLETO]</h5>
                <p class="text-muted mb-4">[DESCRIPCIÓN_BREVE]</p>
            </div>
            <div class="member-social d-flex">
                <a href="#" class="social-link" target="_blank" rel="noopener noreferrer" aria-label="[RED_SOCIAL] de [NOMBRE]">
                    <i class="bi bi-[ICONO]"></i> [RED_SOCIAL]
                </a>
                <a href="#" class="social-link" target="_blank" rel="noopener noreferrer" aria-label="[RED_SOCIAL] de [NOMBRE]">
                    <i class="bi bi-[ICONO]"></i> [RED_SOCIAL]
                </a>
            </div>
        </div>
    </div>
</div>
```

## Especificaciones Técnicas

### Imágenes
- **Tamaño recomendado**: 400x400px mínimo
- **Formato**: JPG, PNG o WebP
- **Ratio**: 1:1 (cuadrada) para mejor ajuste
- **Ubicación**: `tienda_sena/static/assets/`

### Clases CSS Importantes
- `team-image-container`: Contenedor con altura fija (280px)
- `team-image`: Imagen con object-fit: cover para ajuste automático
- `card-content`: Contenedor flexible para el contenido de texto
- `h-100`: Asegura que todas las tarjetas tengan la misma altura

### Campos a Completar
- `[NÚMERO]`: Número secuencial del miembro
- `[NOMBRE_IMAGEN]`: Nombre del archivo de imagen
- `[NOMBRE_COMPLETO]`: Nombre completo del miembro
- `[CARGO]`: Posición o cargo en el equipo
- `[DESCRIPCIÓN_BREVE]`: Descripción de 1-2 líneas
- `[RED_SOCIAL]`: Nombre de la red social (LinkedIn, GitHub, etc.)
- `[ICONO]`: Clase del icono de Bootstrap Icons

### Iconos Disponibles
- **LinkedIn**: `bi-linkedin`
- **Twitter**: `bi-twitter`
- **Facebook**: `bi-facebook`
- **GitHub**: `bi-github`
- **Instagram**: `bi-instagram`
- **Dribbble**: `bi-dribbble`
- **YouTube**: `bi-youtube`
- **TikTok**: `bi-tiktok`
- **WhatsApp**: `bi-whatsapp`
- **Telegram**: `bi-telegram`

## Mejores Prácticas

1. **Accesibilidad**: Siempre incluir `alt` y `aria-label` descriptivos
2. **Consistencia**: Mantener el mismo formato de descripción
3. **Responsive**: Las tarjetas se adaptan automáticamente a diferentes pantallas
4. **Performance**: Optimizar imágenes antes de subirlas

## Ejemplo Completo

```html
<!-- Team Member 4 -->
<div class="col-lg-4 col-md-6">
    <div class="team-card h-100">
        <div class="team-image-container">
            <img src="{% static 'assets/maria_perfil.jpeg' %}" alt="Foto de María González" class="team-image">
        </div>
        <div class="card-content p-4">
            <div>
                <span class="role-tag">Diseñadora UX/UI</span>
                <h5 class="mb-3">María González</h5>
                <p class="text-muted mb-4">Especialista en crear interfaces intuitivas y experiencias de usuario excepcionales.</p>
            </div>
            <div class="member-social d-flex">
                <a href="#" class="social-link" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn de María">
                    <i class="bi bi-linkedin"></i> LinkedIn
                </a>
                <a href="#" class="social-link" target="_blank" rel="noopener noreferrer" aria-label="Behance de María">
                    <i class="bi bi-behance"></i> Behance
                </a>
            </div>
        </div>
    </div>
</div>
```

## Características del Sistema

✅ **Altura uniforme**: Todas las tarjetas tienen la misma altura (450px mínimo)
✅ **Imágenes consistentes**: Contenedor de 280px de altura con ajuste automático
✅ **Responsive**: Adaptación automática a móviles y tablets
✅ **Efectos hover**: Animaciones suaves al pasar el cursor
✅ **Accesibilidad**: Etiquetas descriptivas para lectores de pantalla
