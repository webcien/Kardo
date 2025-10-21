# KardoCSS

**Framework CSS 100% Mobile-First, Modular y Optimizado**

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()

## Descripción

KardoCSS es un framework CSS utility-first, mobile-first y altamente optimizado, diseñado originalmente para KardoCore pero completamente independiente y utilizable en cualquier proyecto web.

### Características Principales

- **100% Mobile-First**: Diseñado desde cero para dispositivos móviles
- **Utility-First**: Clases utilitarias componibles y predecibles
- **Compilador Propio**: Sistema de compilación rápido y eficiente
- **Prefijo Único**: Todas las clases usan el prefijo `k-` para evitar conflictos
- **Responsive**: Sistema de breakpoints intuitivo y flexible
- **Optimizado**: CSS minificado y optimizado para producción
- **Extensible**: Fácil de personalizar y extender
- **Zero Dependencies**: Sin dependencias externas

### Filosofía

KardoCSS sigue los principios de diseño moderno:

- **Composición sobre herencia**
- **Utilidades sobre componentes predefinidos**
- **Mobile-first sobre desktop-first**
- **Rendimiento sobre conveniencia**
- **Simplicidad sobre complejidad**

## Instalación

```bash
# NPM (próximamente)
npm install -D kardocss

# O clonar el repositorio
git clone https://github.com/webcien/KardoCSS.git
cd kardocss
```

## Uso Rápido

### 1. HTML Básico

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KardoCSS Example</title>
    <link rel="stylesheet" href="kardocss.min.css">
</head>
<body class="k-bg-gray-100">
    <div class="k-container k-mx-auto k-p-4">
        <h1 class="k-text-3xl k-font-bold k-text-primary k-mb-4">
            ¡Hola, KardoCSS!
        </h1>
        <p class="k-text-lg k-text-gray-700 k-mb-6">
            Framework CSS mobile-first y utility-first.
        </p>
        <button class="k-btn k-btn-primary k-px-6 k-py-3 k-rounded-lg">
            Comenzar
        </button>
    </div>
</body>
</html>
```

### 2. Responsive Design

```html
<div class="k-grid k-grid-cols-1 k-md:grid-cols-2 k-lg:grid-cols-4 k-gap-4">
    <div class="k-bg-white k-p-4 k-rounded-lg k-shadow">
        Columna 1
    </div>
    <div class="k-bg-white k-p-4 k-rounded-lg k-shadow">
        Columna 2
    </div>
    <div class="k-bg-white k-p-4 k-rounded-lg k-shadow">
        Columna 3
    </div>
    <div class="k-bg-white k-p-4 k-rounded-lg k-shadow">
        Columna 4
    </div>
</div>
```

## Sistema de Utilidades

### Espaciado (Spacing)

```css
/* Padding */
k-p-{tamaño}    /* Padding en todos los lados */
k-px-{tamaño}   /* Padding horizontal */
k-py-{tamaño}   /* Padding vertical */
k-pt-{tamaño}   /* Padding top */
k-pr-{tamaño}   /* Padding right */
k-pb-{tamaño}   /* Padding bottom */
k-pl-{tamaño}   /* Padding left */

/* Margin */
k-m-{tamaño}    /* Margin en todos los lados */
k-mx-{tamaño}   /* Margin horizontal */
k-my-{tamaño}   /* Margin vertical */
k-mt-{tamaño}   /* Margin top */
k-mr-{tamaño}   /* Margin right */
k-mb-{tamaño}   /* Margin bottom */
k-ml-{tamaño}   /* Margin left */

/* Tamaños: 0, 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64 */
```

### Colores

```css
/* Backgrounds */
k-bg-primary
k-bg-secondary
k-bg-accent
k-bg-white
k-bg-black
k-bg-gray-{100-900}

/* Text */
k-text-primary
k-text-secondary
k-text-white
k-text-black
k-text-gray-{100-900}

/* Borders */
k-border-primary
k-border-secondary
k-border-gray-{100-900}
```

### Tipografía

```css
/* Tamaños */
k-text-xs      /* 0.75rem */
k-text-sm      /* 0.875rem */
k-text-base    /* 1rem */
k-text-lg      /* 1.125rem */
k-text-xl      /* 1.25rem */
k-text-2xl     /* 1.5rem */
k-text-3xl     /* 1.875rem */
k-text-4xl     /* 2.25rem */

/* Peso */
k-font-thin
k-font-light
k-font-normal
k-font-medium
k-font-semibold
k-font-bold
k-font-black

/* Alineación */
k-text-left
k-text-center
k-text-right
k-text-justify
```

### Layout

```css
/* Display */
k-block
k-inline-block
k-inline
k-flex
k-inline-flex
k-grid
k-inline-grid
k-hidden

/* Flexbox */
k-flex-row
k-flex-col
k-flex-wrap
k-items-start
k-items-center
k-items-end
k-justify-start
k-justify-center
k-justify-end
k-justify-between

/* Grid */
k-grid-cols-{1-12}
k-gap-{tamaño}
```

### Dimensiones

```css
/* Width */
k-w-full       /* 100% */
k-w-screen     /* 100vw */
k-w-auto
k-w-{fracción} /* 1/2, 1/3, 2/3, 1/4, 3/4, etc. */

/* Height */
k-h-full       /* 100% */
k-h-screen     /* 100vh */
k-h-auto
```

### Bordes y Sombras

```css
/* Border Radius */
k-rounded-none
k-rounded-sm
k-rounded
k-rounded-lg
k-rounded-full

/* Shadows */
k-shadow-none
k-shadow-sm
k-shadow
k-shadow-md
k-shadow-lg
k-shadow-xl
```

## Breakpoints Responsive

KardoCSS usa un sistema mobile-first de breakpoints:

```css
/* Mobile (default) */
k-p-4

/* Tablet (768px+) */
k-md:p-8

/* Desktop (1024px+) */
k-lg:p-12

/* Large Desktop (1280px+) */
k-xl:p-16
```

## Compilación

```bash
# Compilar CSS
python kardocss/cli/build.py --input src/styles.kcss --output dist/kardocss.css

# Compilar y minificar
python kardocss/cli/build.py --input src/styles.kcss --output dist/kardocss.min.css --minify
```

## Estructura del Proyecto

```
kardocss/
├── core/           # Núcleo del framework
├── compiler/       # Compilador de CSS
├── utilities/      # Definiciones de utilidades
├── themes/         # Temas predefinidos
├── cli/            # Herramientas CLI
├── tests/          # Pruebas
├── docs/           # Documentación
└── examples/       # Ejemplos de uso
```

## Personalización

Puedes personalizar KardoCSS mediante un archivo de configuración:

```python
# kardocss.config.py
config = {
    "colors": {
        "primary": "#3498db",
        "secondary": "#2ecc71",
        "accent": "#e74c3c",
    },
    "spacing": {
        "scale": [0, 4, 8, 12, 16, 24, 32, 48, 64],
    },
    "breakpoints": {
        "md": "768px",
        "lg": "1024px",
        "xl": "1280px",
    },
}
```

## Integración con KardoCore

KardoCSS está diseñado para integrarse perfectamente con KardoCore:

```python
# En KardoTheme
#for post in posts
  <article class="k-card k-p-6 k-mb-4 k-shadow-md k-rounded-lg">
    <h2 class="k-text-2xl k-font-bold k-mb-2">{post.title}</h2>
    <p class="k-text-gray-700">{post.excerpt}</p>
  </article>
#end
```

## Roadmap

- [x] Sistema de utilidades base
- [ ] Compilador completo
- [ ] CLI para generación
- [ ] Temas predefinidos
- [ ] Componentes opcionales
- [ ] Publicación en NPM
- [ ] Documentación completa

## Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## Autor

Juan Quezada

---

**Nota**: Este proyecto está en fase alpha de desarrollo. Puede usarse en proyectos personales pero no se recomienda para producción todavía.

