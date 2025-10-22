# KardoCore

**Framework Python Moderno para CMS, Headless CMS, APIs y Aplicaciones Empresariales**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Licencia](https://img.shields.io/badge/Licencia-MIT-green.svg)](LICENSE)
[![Versión](https://img.shields.io/badge/Versi%C3%B3n-0.0.9-orange.svg)](https://github.com/webcien/Kardo/releases/tag/v0.0.9)

---

## 🌟 Descripción General

**KardoCore** es un framework Python híbrido, modular y preparado para IA, diseñado para construir aplicaciones web modernas, plataformas CMS, headless CMS, APIs REST y soluciones empresariales.

### Características Principales

- ⚡ **Arquitectura ASGI Asíncrona** - Construido para alto rendimiento
- 🎨 **Motor de Plantillas Nativo (KardoTheme)** - Sintaxis natural con prefijo `#`
- 📦 **Gestor de Paquetes** - Instala y gestiona temas fácilmente
- 🔒 **Sistema de Validación Integrado** - Sin dependencias externas
- 🤖 **Preparado para IA** - Integración nativa para características de IA
- 🧩 **Modularidad Extrema** - Usa solo lo que necesitas
- 🌍 **Soporte Multi-idioma** - Listo para i18n

---

## 📋 Información de Versiones

KardoCore está disponible en **dos versiones** para soportar diferentes entornos Python:

### 🎯 v0.0.9 (Estable) - **RECOMENDADO PARA PRODUCCIÓN**
- **Python**: >= 3.11
- **Estado**: Estable y listo para producción
- **Branch**: `v0.0.9`
- **Compatible con**: Python 3.11, 3.12, 3.13, 3.14+

### 🚀 v0.1.0-alpha (Desarrollo)
- **Python**: >= 3.14
- **Estado**: Desarrollo activo
- **Branch**: `main`
- **Características**: Usa características modernas de Python 3.14 (PEP 649/749)

**📖 [Ver comparación detallada de versiones →](VERSION_INFO.md)**

---

## 🚀 Inicio Rápido

### Instalación

**Para producción (Python 3.11+):**
```bash
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

**Para desarrollo (Python 3.14+):**
```bash
pip install git+https://github.com/webcien/Kardo.git@main
```

### Hola Mundo

```python
from kardocore import KardoApp

app = KardoApp()

@app.route("/")
async def index(request):
    return {"message": "¡Hola desde KardoCore!"}

if __name__ == "__main__":
    app.run()
```

Ejecuta tu aplicación:
```bash
python app.py
```

Visita: http://localhost:8000

---

## 🎨 Motor de Plantillas (KardoTheme)

KardoCore incluye un potente motor de plantillas nativo con sintaxis natural.

### Ejemplo de Plantilla

**templates/index.html:**
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    
    #if items
        <ul>
        #for item in items
            <li>{item.name} - ${item.price}</li>
        #end
        </ul>
    #else
        <p>No hay artículos disponibles</p>
    #end
    
    #include "partials/footer.html"
</body>
</html>
```

### Usando Plantillas

```python
from kardocore.theme import KardoTheme

theme = KardoTheme(template_dir="templates")

context = {
    "title": "Mi Tienda",
    "items": [
        {"name": "Producto 1", "price": 29.99},
        {"name": "Producto 2", "price": 39.99}
    ]
}

html = theme.render("index.html", context)
print(html)
```

### Sintaxis de Plantillas

| Sintaxis | Descripción | Ejemplo |
|----------|-------------|---------|
| `{variable}` | Interpolación de variables | `{user.name}` |
| `#if condition` | Condicional | `#if user.is_admin` |
| `#else` | Cláusula else | `#else` |
| `#end` | Fin de bloque | `#end` |
| `#for item in items` | Bucle | `#for post in posts` |
| `#include "file"` | Incluir plantilla | `#include "header.html"` |
| `{# comment #}` | Comentario | `{# TODO: arreglar esto #}` |

---

## 📦 Gestor de Paquetes

Instala y gestiona temas desde el registro oficial.

### Comandos CLI

```bash
# Instalar un tema
kardo theme install wellness-clinic

# Listar temas instalados
kardo theme list

# Buscar temas
kardo theme search salud

# Ver información del tema
kardo theme info wellness-clinic

# Desinstalar tema
kardo theme uninstall wellness-clinic
```

### Uso Programático

```python
from kardocore.packages import PackageManager

pm = PackageManager()

# Instalar tema
pm.install_theme("wellness-clinic")

# Listar temas
themes = pm.list_themes()

# Buscar temas
results = pm.search_themes(query="salud", category="salud-bienestar")
```

---

## 🏗️ Estructura del Proyecto

```
mi_proyecto/
├── app.py              # Aplicación principal
├── templates/          # Plantillas KardoTheme
│   ├── layout.html
│   ├── index.html
│   └── partials/
│       ├── header.html
│       └── footer.html
├── static/             # Archivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── models/             # Modelos de datos
├── routes/             # Manejadores de rutas
└── requirements.txt
```

---

## 📚 Documentación

- **[Guía de Instalación](HOW-TO-INSTALL.md)** - Instrucciones detalladas de instalación
- **[Guía de Inicio Rápido](QUICK-START.md)** - Comienza en 5 minutos
- **[Información de Versiones](VERSION_INFO.md)** - Compara v0.0.9 y v0.1.0
- **[Registro de Cambios](CHANGELOG.md)** - Historial de versiones
- **[Contribuir](CONTRIBUTING.md)** - Cómo contribuir

### Documentación por Idioma

- 🇺🇸 **English**: [README.md](README.md)
- 🇪🇸 **Español**: README.es.md (este archivo)

---

## 🌐 Ecosistema

KardoCore es parte del **Ecosistema Kardo**:

### [KardoCSS](https://github.com/webcien/KardoCSS)
Framework CSS mobile-first con utilidades y componentes
- 67KB completo / 50KB minificado
- 20+ componentes
- 100+ utilidades
- Optimizado para touch

### [KardoTemplates](https://github.com/webcien/KardoTemplates)
Colección de plantillas profesionales para KardoCore
- 60 plantillas (50 frontend + 10 backend)
- 15 categorías frontend
- 2 categorías backend
- Responsive mobile-first

---

## 🎯 Casos de Uso

- ✅ **Plataformas CMS** - Sistemas de gestión de contenidos completos
- ✅ **Headless CMS** - Plataformas de contenido API-first
- ✅ **APIs REST** - APIs rápidas y escalables
- ✅ **Aplicaciones Web** - Aplicaciones web modernas
- ✅ **Soluciones Empresariales** - Aplicaciones de negocio
- ✅ **E-commerce** - Tiendas online
- ✅ **Blogs y Portafolios** - Sitios web personales

---

## 🔧 Requisitos

### Para v0.0.9 (Estable)
- Python >= 3.11
- uvicorn >= 0.30.0

### Para v0.1.0-alpha (Desarrollo)
- Python >= 3.14
- uvicorn >= 0.30.0

---

## 🤝 Contribuir

¡Damos la bienvenida a contribuciones! Por favor consulta [CONTRIBUTING.md](CONTRIBUTING.md) para las pautas.

### Configuración de Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/webcien/Kardo.git
cd Kardo

# Para versión estable
git checkout v0.0.9

# Para versión de desarrollo
git checkout main

# Instalar en modo desarrollo
pip install -e .

# Ejecutar tests
pytest
```

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Inspirado por frameworks Python modernos
- Construido pensando en rendimiento y experiencia del desarrollador
- Desarrollo impulsado por la comunidad

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/webcien/Kardo/issues)
- **Discusiones**: [GitHub Discussions](https://github.com/webcien/Kardo/discussions)
- **Documentación**: [Documentación Completa](https://github.com/webcien/Kardo/wiki)

---

## 🗺️ Hoja de Ruta

### v0.0.9 (Actual - Estable)
- ✅ Compatibilidad con Python 3.11+
- ✅ Características core completas
- 🔄 Correcciones de bugs y mejoras
- 🔄 Documentación

### v0.1.0-alpha (Actual - Desarrollo)
- ✅ Optimizaciones para Python 3.14+
- 🔄 Características experimentales
- 📅 Sistema de caché integrado
- 📅 Soporte multi-base de datos
- 📅 API REST automática
- 📅 Soporte GraphQL

### v1.0.0 (Futuro)
- 📅 Versión estable unificada
- 📅 Python 3.14+ como requisito mínimo
- 📅 Documentación completa
- 📅 Testing exhaustivo
- 📅 Listo para producción

---

## ⭐ Historial de Estrellas

Si encuentras útil KardoCore, ¡por favor considera darle una estrella en GitHub!

---

**Hecho con ❤️ por el Equipo Kardo**

