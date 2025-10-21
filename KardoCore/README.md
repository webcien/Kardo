# KardoCore

**Framework Python Híbrido, Modular e IA-Ready**

[![Python](https://img.shields.io/badge/python-3.14+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)]()

## Descripción

KardoCore es un framework open source híbrido, modular y multisalidas desarrollado en Python, diseñado para la creación de Headless CMS, CMS completos, APIs, eCommerce y aplicaciones empresariales con integración nativa de IA generativa.

### Características Principales

- **Arquitectura ASGI Asíncrona**: Basado en el estándar ASGI para máximo rendimiento
- **Sistema de Validación Propio**: Inspirado en Pydantic pero desarrollado desde cero
- **Motor de Plantillas KardoTheme**: Sintaxis expresiva y segura para frontend y backend
- **Integración IA Nativa**: Sistema modular para conectar con OpenAI, Ollama, HuggingFace, etc.
- **Híbrido Multisalidas**: Opera como framework web tradicional, headless CMS o API server
- **Modularidad Extrema**: Sistema de plugins y extensiones completamente desacoplado
- **Seguridad por Diseño**: Validación estricta, sandboxing y aislamiento de componentes

### Filosofía

KardoCore es **headless por diseño** con IA integrada pero desacoplada del core. Construido con arquitectura modular ideal y escalable que es rápida, asíncrona, segura, inteligente y universal.

## Requisitos

- **Python 3.14+** (aprovecha características como PEP 649, 734, 750, 768, 784)
- Sistema operativo: Linux, macOS, Windows
- Servidor ASGI: Uvicorn, Hypercorn o Daphne

## Instalación Rápida

```bash
# Clonar el repositorio (cuando esté disponible)
git clone https://github.com/webcien/KardoCore.git
cd kardocore

# Crear entorno virtual
python3.14 -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate

# Instalar dependencias
pip install -e .

# Crear archivo de configuración
cp .env.example .env
# Editar .env con tu configuración

# Ejecutar servidor de desarrollo
uvicorn kardocore.main:app --reload
```

## Inicio Rápido

```python
from kardocore import KardoApp, JSONResponse

app = KardoApp(title="Mi Primera App", version="1.0.0")

@app.get("/")
async def index(request):
    return {"message": "¡Hola, KardoCore!"}

@app.post("/api/users")
async def create_user(request):
    data = await request.json()
    # Procesar datos
    return JSONResponse({"user": data}, status_code=201)

@app.on_event("on_startup")
async def startup():
    print("Aplicación iniciada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Estructura del Proyecto

```
kardocore/
├── core/                # Núcleo del framework
│   ├── api/            # API REST y GraphQL
│   ├── auth/           # Autenticación y autorización
│   ├── events/         # Sistema de eventos y hooks
│   ├── models/         # Sistema de validación propio
│   ├── plugins/        # Gestión de plugins
│   └── utils/          # Utilidades
├── theme/              # Motor de plantillas KardoTheme
├── ai/                 # Módulo KardoAI
│   ├── providers/      # Adaptadores de IA
│   └── modules/        # Módulos IA
├── admin/              # Panel de administración
├── cli/                # Herramientas CLI
├── config/             # Configuración
├── tests/              # Pruebas
└── docs/               # Documentación
```

## Componentes Principales

### 1. KardoCore (Núcleo)

El núcleo del framework proporciona:

- Servidor ASGI asíncrono
- Sistema de rutas tipadas
- Modelos de datos con validación automática
- Sistema de eventos y hooks
- Autenticación JWT + RBAC
- API REST y GraphQL

### 2. KardoTheme (Motor de Plantillas)

Motor de plantillas unificado para frontend y backend:

- Sintaxis expresiva y compacta
- Compilación a AST seguro
- Contextos separados (frontend/admin)
- Componentes reutilizables
- Sandboxing y escape automático

### 3. KardoAI (Integración IA)

Sistema modular para integración de IA:

- Adaptadores para múltiples proveedores
- Eventos automáticos
- Control de costos y tokens
- Plugins IA externos

### 4. KardoAdmin (Panel de Administración)

Interfaz de administración mobile-first:

- Renderizado con KardoTheme
- Editor WYSIWYG modular
- Gestión completa del sistema
- Extensible mediante plugins

## Características de Python 3.14 Utilizadas

KardoCore aprovecha las últimas características de Python 3.14:

- **PEP 649/749**: Evaluación diferida de anotaciones para mejor rendimiento
- **PEP 734**: Múltiples intérpretes para aislamiento de plugins
- **PEP 750**: Template strings para sanitización segura
- **PEP 768**: Interfaz de depuración segura para producción
- **PEP 784**: Compresión Zstandard para mejor rendimiento

## Configuración

KardoCore usa un sistema de configuración tipado con soporte para variables de entorno:

```python
from kardocore import KardoSettings, String, Integer

class AppConfig(KardoSettings):
    debug: bool = FieldInfo(default=False)
    database_url: str = String(required=True)
    secret_key: str = String(min_length=32, required=True)
    port: int = Integer(default=8000)
    
    class Config:
        env_file = ".env"
        env_prefix = "KARDO_"

config = AppConfig()
```

## Sistema de Eventos

```python
from kardocore import event, Events

@event(Events.ON_CONTENT_CREATED)
async def on_content_created(content):
    print(f"Nuevo contenido creado: {content.title}")
    # Generar resumen con IA
    # Optimizar SEO
    # Enviar notificaciones
```

## Roadmap

- [x] Fase 1: Core y Seguridad
- [ ] Fase 2: KardoTheme
- [ ] Fase 3: KardoAI
- [ ] Fase 4: Panel Administrativo
- [ ] Fase 5: Extensiones y Plugins
- [ ] Fase 6: Lanzamiento Alpha

## Contribuir

Este proyecto está en desarrollo activo. Las contribuciones son bienvenidas una vez que se lance la versión alpha pública.

## Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## Autor

Juan Quezada

## Agradecimientos

Inspirado en proyectos como FastAPI, Starlette, Jinja2 y Pydantic, pero desarrollado completamente desde cero bajo licencia MIT.

---

**Nota**: Este proyecto está en fase alpha de desarrollo. No se recomienda su uso en producción todavía.

