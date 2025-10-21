# KardoCore v0.0.9 - Versión Compatible Python 3.11+

Esta es la versión **v0.0.9** de KardoCore, compatible con **Python 3.11 o superior**.

## Diferencias con v0.1.0

La versión **v0.1.0-alpha** (branch `master`) está diseñada para **Python 3.14+** y aprovecha las nuevas características del lenguaje como evaluación diferida de anotaciones (PEP 649/749) y `annotationlib`.

Esta versión **v0.0.9** (branch `v0.0.9`) mantiene todas las funcionalidades pero con compatibilidad para **Python 3.11, 3.12, 3.13 y 3.14+**.

## Cambios de Compatibilidad

### 1. Sistema de Anotaciones

**v0.1.0 (Python 3.14+):**
```python
from annotationlib import get_annotations, Format
```

**v0.0.9 (Python 3.11+):**
```python
try:
    from annotationlib import get_annotations, Format
except ImportError:
    def get_annotations(obj, *, eval_str=False, format=None):
        return get_type_hints(obj) if eval_str else getattr(obj, '__annotations__', {})
    Format = None
```

### 2. Type Hints

**v0.1.0 (Python 3.14+):**
```python
def function(param: int | None = None) -> str | None:
    validator: callable | None = None
```

**v0.0.9 (Python 3.11+):**
```python
from typing import Optional, Union, Callable

def function(param: Optional[int] = None) -> Optional[str]:
    validator: Optional[Callable] = None
```

## Instalación

### Desde GitHub (branch v0.0.9)

```bash
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

### Desde código fuente

```bash
git clone https://github.com/webcien/Kardo.git
cd Kardo
git checkout v0.0.9
pip install -e .
```

## Requisitos

- Python >= 3.11
- uvicorn >= 0.30.0

## Uso

El uso es idéntico a la versión v0.1.0. Consulta el [README principal](README.md) para documentación completa.

```python
from kardocore import KardoApp

app = KardoApp()

@app.route("/")
async def index(request):
    return {"message": "Hello from KardoCore v0.0.9!"}

if __name__ == "__main__":
    app.run()
```

## Motor de Plantillas KardoTheme

```python
from kardocore.theme import KardoTheme

theme = KardoTheme(template_dir="templates")

context = {
    "title": "Mi Sitio",
    "items": ["Item 1", "Item 2", "Item 3"]
}

html = theme.render("index.html", context)
```

### Sintaxis de KardoTheme

```html
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    
    #if items
        <ul>
        #for item in items
            <li>{item}</li>
        #end
        </ul>
    #else
        <p>No hay items</p>
    #end
    
    #include "partials/footer.html"
</body>
</html>
```

## PackageManager

```python
from kardocore.packages import PackageManager

pm = PackageManager()

# Instalar tema desde registry
pm.install_theme("wellness-clinic")

# Listar temas instalados
themes = pm.list_themes()

# Buscar temas
results = pm.search_themes(query="salud")
```

## CLI

```bash
# Instalar un tema
kardo theme install wellness-clinic

# Listar temas instalados
kardo theme list

# Buscar temas
kardo theme search salud

# Ver información de un tema
kardo theme info wellness-clinic
```

## Migración desde v0.1.0

Si tienes código escrito para v0.1.0 (Python 3.14+) y necesitas ejecutarlo en Python 3.11-3.13:

1. Cambia a la versión v0.0.9:
   ```bash
   pip uninstall kardocore
   pip install git+https://github.com/webcien/Kardo.git@v0.0.9
   ```

2. Tu código de aplicación **no necesita cambios**, solo la versión de KardoCore instalada.

3. Si estás desarrollando extensiones o plugins que usan internals de KardoCore, revisa los cambios en type hints.

## Migración hacia v0.1.0

Si actualizas a Python 3.14+ y quieres aprovechar las nuevas características:

1. Actualiza a Python 3.14+
2. Cambia a la versión v0.1.0:
   ```bash
   pip uninstall kardocore
   pip install git+https://github.com/webcien/Kardo.git@master
   ```

3. Tu código de aplicación seguirá funcionando sin cambios.

## Soporte

- **v0.0.9**: Mantenimiento y corrección de bugs para Python 3.11+
- **v0.1.0**: Desarrollo activo con nuevas características para Python 3.14+

## Licencia

MIT License - Ver [LICENSE](LICENSE) para más detalles.

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md) para guías de contribución.

## Changelog

Ver [CHANGELOG.md](CHANGELOG.md) para historial completo de cambios.

