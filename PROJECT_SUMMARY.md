# Proyecto Kardo - Resumen de Desarrollo

**Fecha de creación**: Octubre 2025  
**Versión**: 0.1.0-alpha  
**Autor**: Juan Quezada  
**Licencia**: MIT

## Descripción General

El Proyecto Kardo es un ecosistema de desarrollo web moderno que consta de dos frameworks independientes pero diseñados para trabajar juntos:

1. **KardoCore**: Framework Python híbrido, modular e IA-ready
2. **KardoCSS**: Framework CSS 100% mobile-first y utility-first

Ambos proyectos están desarrollados desde cero, sin dependencias externas pesadas, bajo licencia MIT y listos para ser publicados en GitHub como proyectos open source independientes.

---

## KardoCore

### Descripción

Framework Python basado en ASGI para la creación de Headless CMS, CMS completos, APIs, eCommerce y aplicaciones empresariales con integración nativa de IA generativa.

### Características Implementadas

#### ✅ Núcleo del Framework

- **Servidor ASGI Asíncrono** (`kardocore/core/app.py`)
  - Manejo de peticiones HTTP
  - Sistema de rutas tipadas
  - Respuestas JSON y HTML
  - Middleware extensible

- **Sistema de Validación Propio** (`kardocore/core/models/`)
  - Inspirado en Pydantic pero desarrollado desde cero
  - Validación de tipos automática
  - Conversión de tipos
  - Helpers para campos comunes (String, Integer, Email, DateTime)
  - Serialización a dict/JSON

- **Sistema de Eventos Asíncronos** (`kardocore/core/events.py`)
  - EventManager con aislamiento de errores
  - Decorador `@event` para registro fácil
  - Historial de eventos para auditoría
  - Eventos predefinidos del sistema

- **Sistema de Configuración** (`kardocore/core/config.py`)
  - KardoSettings con validación tipada
  - Soporte para variables de entorno (.env)
  - Prioridad: ENV > .env > defaults
  - Configuración por entorno (dev, staging, prod)

#### ✅ Motor de Plantillas KardoTheme

- **Tokenizador** (`kardocore/theme/tokenizer.py`)
  - Sintaxis expresiva con prefijo `#`
  - Bloques de control: `#for`, `#if`, `#elif`, `#else`, `#end`
  - Expresiones dinámicas: `{variable}`
  - Comentarios: `{# ... #}`
  - Validación de bloques balanceados

- **Renderizador** (`kardocore/theme/renderer.py`)
  - Escape automático (anti-XSS)
  - Sandboxing de seguridad
  - Contexto seguro para evaluación
  - Soporte para bucles y condicionales anidados

- **Motor Principal** (`kardocore/theme/engine.py`)
  - Caché de plantillas compiladas
  - Renderizado desde archivos o strings
  - Precompilación de plantillas
  - Detección automática de cambios

### Tecnologías Utilizadas

- **Python 3.14+** con características modernas:
  - PEP 649/749: Evaluación diferida de anotaciones
  - PEP 734: Múltiples intérpretes para aislamiento
  - PEP 750: Template strings seguros
  - PEP 768: Interfaz de depuración
  - PEP 784: Compresión Zstandard

- **ASGI** para servidor asíncrono
- **Uvicorn** como servidor de desarrollo

### Estructura del Proyecto

```
KardoCore/
├── kardocore/
│   ├── core/           # Núcleo del framework
│   │   ├── app.py      # Aplicación ASGI
│   │   ├── models/     # Sistema de validación
│   │   ├── events.py   # Sistema de eventos
│   │   └── config.py   # Configuración
│   ├── theme/          # Motor de plantillas
│   │   ├── tokenizer.py
│   │   ├── renderer.py
│   │   └── engine.py
│   ├── ai/             # Módulo IA (pendiente)
│   ├── admin/          # Panel admin (pendiente)
│   └── cli/            # Herramientas CLI (pendiente)
├── examples/
│   ├── simple_app.py
│   ├── theme_example.py
│   └── templates/
├── tests/              # Tests (pendiente)
├── docs/               # Documentación (pendiente)
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── setup.py
└── .env.example
```

### Ejemplos de Uso

#### Aplicación Básica

```python
from kardocore import KardoApp, JSONResponse

app = KardoApp(title="Mi App", version="1.0.0")

@app.get("/")
async def index(request):
    return {"message": "¡Hola, KardoCore!"}

@app.on_event("on_startup")
async def startup():
    print("Aplicación iniciada")
```

#### Motor de Plantillas

```python
from kardocore.theme import KardoTheme

theme = KardoTheme(template_dir="templates")
html = theme.render("page.html", {
    "title": "Mi Página",
    "posts": posts
})
```

### Roadmap

- [x] Fase 1: Core y Seguridad
- [x] Fase 2: KardoTheme (Motor de Plantillas)
- [ ] Fase 3: KardoAI (Integración IA)
- [ ] Fase 4: Panel Administrativo
- [ ] Fase 5: Extensiones y Plugins
- [ ] Fase 6: Tests y Documentación
- [ ] Fase 7: Lanzamiento Alpha

---

## KardoCSS

### Descripción

Framework CSS utility-first y mobile-first diseñado originalmente para KardoCore pero completamente independiente y utilizable en cualquier proyecto web.

### Características Implementadas

#### ✅ Sistema de Configuración

- **KardoCSSConfig** (`kardocss/core/config.py`)
  - Configuración completa de tokens de diseño
  - Colores, espaciados, tipografía, breakpoints
  - Personalización mediante archivos Python
  - Merge profundo de configuraciones

#### ✅ Compilador

- **KardoCSSCompiler** (`kardocss/compiler/compiler.py`)
  - Generación de CSS completo
  - Minificación automática
  - Purging de CSS no utilizado (pendiente implementación completa)
  - Optimización de tamaño

#### ✅ Generadores de Utilidades

- **Spacing** (`kardocss/utilities/spacing.py`)
  - Margin y padding en todas las direcciones
  - Escala de espaciado configurable
  - Conversión automática px a rem

- **Colors** (`kardocss/utilities/colors.py`)
  - Background, text y border colors
  - Escalas de grises
  - Colores semánticos (primary, secondary, etc.)

- **Typography** (`kardocss/utilities/typography.py`)
  - Tamaños de fuente
  - Pesos de fuente
  - Alineación de texto

- **Layout** (`kardocss/utilities/layout.py`)
  - Display (block, flex, grid, etc.)
  - Flexbox utilities
  - Grid utilities

- **Borders** (`kardocss/utilities/borders.py`)
  - Border radius
  - Sombras (shadows)

- **Sizing** (`kardocss/utilities/sizing.py`)
  - Width y height
  - Container

#### ✅ CLI

- **Build Tool** (`kardocss/cli/build.py`)
  - Compilación desde línea de comandos
  - Soporte para configuración personalizada
  - Minificación opcional
  - Output detallado

### Tecnologías Utilizadas

- **Python 3.10+** para el compilador
- **CSS3** estándar
- **Sin dependencias externas**

### Estructura del Proyecto

```
KardoCSS/
├── kardocss/
│   ├── core/
│   │   └── config.py       # Configuración
│   ├── compiler/
│   │   └── compiler.py     # Compilador principal
│   ├── utilities/          # Generadores de utilidades
│   │   ├── spacing.py
│   │   ├── colors.py
│   │   ├── typography.py
│   │   ├── layout.py
│   │   ├── borders.py
│   │   └── sizing.py
│   └── cli/
│       └── build.py        # CLI
├── examples/
│   └── index.html
├── dist/
│   ├── kardocss.css        # CSS compilado (16.94 KB)
│   └── kardocss.min.css    # CSS minificado (13.37 KB)
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── setup.py
└── test_compile.py
```

### Ejemplos de Uso

#### HTML con KardoCSS

```html
<div class="k-container k-mx-auto k-p-4">
  <h1 class="k-text-3xl k-font-bold k-text-primary k-mb-4">
    ¡Hola, KardoCSS!
  </h1>
  <div class="k-grid k-grid-cols-1 k-md:grid-cols-2 k-gap-4">
    <div class="k-bg-white k-p-6 k-rounded-lg k-shadow-md">
      Tarjeta 1
    </div>
    <div class="k-bg-white k-p-6 k-rounded-lg k-shadow-md">
      Tarjeta 2
    </div>
  </div>
</div>
```

#### Compilación

```bash
# Compilar CSS
python -m kardocss.cli.build -o dist/kardocss.css

# Compilar y minificar
python -m kardocss.cli.build -o dist/kardocss.min.css --minify
```

### Roadmap

- [x] Sistema de configuración
- [x] Compilador base
- [x] Utilidades fundamentales
- [x] CLI básico
- [ ] Variantes responsive completas
- [ ] Purging de CSS no utilizado
- [ ] Componentes opcionales
- [ ] Publicación en NPM/PyPI
- [ ] Documentación completa

---

## Integración KardoCore + KardoCSS

### Uso Conjunto

```html
<!-- Plantilla KardoTheme con clases KardoCSS -->
<!DOCTYPE html>
<html>
<head>
    <title>{page.title}</title>
    <link rel="stylesheet" href="/static/css/kardocss.min.css">
</head>
<body class="k-bg-gray-100">
    <div class="k-container k-mx-auto k-p-4">
        <h1 class="k-text-4xl k-font-bold k-text-primary">
            {page.title}
        </h1>
        
        #for post in posts
            <article class="k-bg-white k-p-6 k-rounded-lg k-shadow-md k-mb-4">
                <h2 class="k-text-2xl k-font-semibold">{post.title}</h2>
                <p class="k-text-gray-700">{post.excerpt}</p>
            </article>
        #end
    </div>
</body>
</html>
```

---

## Estado Actual del Desarrollo

### ✅ Completado

1. **KardoCore**
   - ✅ Servidor ASGI básico
   - ✅ Sistema de validación propio
   - ✅ Sistema de eventos
   - ✅ Configuración con .env
   - ✅ Motor de plantillas KardoTheme completo
   - ✅ Ejemplos funcionales
   - ✅ Documentación README
   - ✅ Licencia MIT
   - ✅ CONTRIBUTING.md

2. **KardoCSS**
   - ✅ Sistema de configuración
   - ✅ Compilador funcional
   - ✅ Generadores de utilidades
   - ✅ CLI básico
   - ✅ Minificación
   - ✅ Ejemplos HTML
   - ✅ Documentación README
   - ✅ Licencia MIT
   - ✅ CONTRIBUTING.md

### 🚧 Pendiente

1. **KardoCore**
   - ⏳ Módulo KardoAI (integración IA)
   - ⏳ Panel KardoAdmin
   - ⏳ Sistema de autenticación completo
   - ⏳ API REST/GraphQL
   - ⏳ Sistema de plugins
   - ⏳ Tests unitarios
   - ⏳ Documentación completa

2. **KardoCSS**
   - ⏳ Variantes responsive completas
   - ⏳ Purging avanzado
   - ⏳ Componentes opcionales
   - ⏳ Tests
   - ⏳ Documentación de utilidades

---

## Próximos Pasos

### Corto Plazo (1-2 semanas)

1. Completar tests unitarios básicos
2. Implementar módulo KardoAI básico
3. Crear documentación de API
4. Preparar para publicación en GitHub

### Mediano Plazo (1-2 meses)

1. Desarrollar panel KardoAdmin
2. Implementar sistema de plugins
3. Completar variantes responsive de KardoCSS
4. Crear sitio de documentación

### Largo Plazo (3-6 meses)

1. Lanzamiento alpha público
2. Comunidad y contribuciones
3. Publicación en PyPI (KardoCore) y NPM (KardoCSS)
4. Versión 1.0 estable

---

## Notas Técnicas

### Decisiones de Diseño

1. **Sin Pydantic**: Se desarrolló un micro-sistema de validación propio para mantener control total y evitar dependencias pesadas.

2. **Prefijo k-**: KardoCSS usa el prefijo `k-` en todas las clases para evitar conflictos con otros frameworks.

3. **Mobile-First**: Ambos frameworks priorizan dispositivos móviles en su diseño.

4. **Modularidad**: Arquitectura completamente modular y desacoplada.

5. **Seguridad**: Escape automático, sandboxing y validación estricta en todos los niveles.

### Compatibilidad

- **Python**: 3.14+ (KardoCore), 3.10+ (KardoCSS)
- **Navegadores**: Todos los navegadores modernos
- **Servidores ASGI**: Uvicorn, Hypercorn, Daphne

---

## Licencia

Ambos proyectos están licenciados bajo **MIT License**, permitiendo uso comercial y modificación libre.

---

## Contacto y Contribuciones

- **Autor**: Juan Quezada
- **GitHub**: (pendiente de publicación)
- **Contribuciones**: Ver CONTRIBUTING.md en cada proyecto

---

**Última actualización**: Octubre 2025  
**Versión del documento**: 1.0

