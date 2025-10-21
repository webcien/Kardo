# Información de Versiones de KardoCore

KardoCore está disponible en dos versiones principales para soportar diferentes versiones de Python.

## Versiones Disponibles

### v0.1.0-alpha (Branch: main)
**Python 3.14+ - Versión de Desarrollo**

Esta es la versión de desarrollo que aprovecha las últimas características de Python 3.14, incluyendo:
- Evaluación diferida de anotaciones (PEP 649/749)
- `annotationlib` para manejo avanzado de anotaciones
- Union types nativos (`int | None`)
- Mejor rendimiento con características modernas

**Instalación:**
```bash
# Requiere Python 3.14+
pip install git+https://github.com/webcien/Kardo.git@main
```

**Uso recomendado:**
- Desarrollo de nuevas características
- Entornos con Python 3.14+
- Proyectos que requieren máximo rendimiento

---

### v0.0.9 (Branch: v0.0.9) ⭐ RECOMENDADO PARA PRODUCCIÓN
**Python 3.11+ - Versión Estable**

Esta es la versión estable compatible con Python 3.11, 3.12, 3.13 y 3.14+. Incluye todas las funcionalidades de v0.1.0 con fallbacks para compatibilidad.

**Instalación:**
```bash
# Compatible con Python 3.11+
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

**Uso recomendado:**
- Producción
- Entornos con Python 3.11-3.13
- Proyectos que requieren estabilidad

---

## Comparación de Características

| Característica | v0.1.0-alpha | v0.0.9 |
|----------------|--------------|---------|
| Python 3.11 | ❌ | ✅ |
| Python 3.12 | ❌ | ✅ |
| Python 3.13 | ❌ | ✅ |
| Python 3.14+ | ✅ | ✅ |
| Motor KardoTheme | ✅ | ✅ |
| PackageManager | ✅ | ✅ |
| Sistema ASGI | ✅ | ✅ |
| Validación de modelos | ✅ | ✅ |
| Sistema de eventos | ✅ | ✅ |
| CLI | ✅ | ✅ |
| Rendimiento | Óptimo | Muy bueno |
| Estabilidad | Beta | Estable |

---

## ¿Qué Versión Elegir?

### Usa v0.0.9 si:
- ✅ Estás en producción
- ✅ Usas Python 3.11, 3.12 o 3.13
- ✅ Necesitas estabilidad
- ✅ Quieres compatibilidad amplia

### Usa v0.1.0-alpha si:
- ✅ Estás en desarrollo
- ✅ Usas Python 3.14+
- ✅ Quieres las últimas características
- ✅ Necesitas máximo rendimiento

---

## Migración entre Versiones

### De v0.1.0 a v0.0.9
```bash
pip uninstall kardocore
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

**Cambios necesarios:** Ninguno en código de aplicación.

### De v0.0.9 a v0.1.0
```bash
# Primero actualiza Python a 3.14+
pip uninstall kardocore
pip install git+https://github.com/webcien/Kardo.git@main
```

**Cambios necesarios:** Ninguno en código de aplicación.

---

## Instalación Detallada

### Opción 1: Desde GitHub (Recomendado)

**Versión estable (v0.0.9):**
```bash
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

**Versión desarrollo (v0.1.0):**
```bash
pip install git+https://github.com/webcien/Kardo.git@main
```

### Opción 2: Desde código fuente

```bash
# Clonar repositorio
git clone https://github.com/webcien/Kardo.git
cd Kardo

# Para v0.0.9 (estable)
git checkout v0.0.9
pip install -e .

# O para v0.1.0 (desarrollo)
git checkout main
pip install -e .
```

### Opción 3: Con requirements.txt

**Para v0.0.9:**
```
git+https://github.com/webcien/Kardo.git@v0.0.9
```

**Para v0.1.0:**
```
git+https://github.com/webcien/Kardo.git@main
```

---

## Verificar Versión Instalada

```python
import kardocore
print(kardocore.__version__)
```

O desde la terminal:
```bash
kardo --version
```

---

## Soporte y Actualizaciones

- **v0.0.9**: Mantenimiento activo, corrección de bugs
- **v0.1.0-alpha**: Desarrollo activo, nuevas características

Ambas versiones reciben actualizaciones de seguridad.

---

## Roadmap

### v0.0.9 (Estable)
- ✅ Python 3.11+ compatible
- ✅ Todas las características core
- 🔄 Corrección de bugs
- 🔄 Mejoras de rendimiento
- 🔄 Documentación

### v0.1.0 (Desarrollo)
- ✅ Python 3.14+ optimizado
- 🔄 Nuevas características experimentales
- 🔄 Optimizaciones avanzadas
- 📅 Sistema de caché integrado
- 📅 Soporte para múltiples bases de datos
- 📅 API REST automática
- 📅 GraphQL support

### v1.0.0 (Futuro)
- 📅 Versión estable unificada
- 📅 Python 3.14+ como requisito mínimo
- 📅 Todas las características de v0.1.0
- 📅 Documentación completa
- 📅 Testing exhaustivo

---

## Preguntas Frecuentes

**P: ¿Puedo usar v0.0.9 con Python 3.14?**
R: Sí, v0.0.9 es compatible con Python 3.14+, pero no aprovecha las nuevas características.

**P: ¿Mi código funcionará en ambas versiones?**
R: Sí, el código de aplicación es 100% compatible entre versiones.

**P: ¿Cuál es más rápida?**
R: v0.1.0 es ligeramente más rápida en Python 3.14+ debido a optimizaciones del lenguaje.

**P: ¿Cuándo debería actualizar de v0.0.9 a v0.1.0?**
R: Cuando actualices a Python 3.14+ y quieras las últimas características.

**P: ¿v0.0.9 recibirá nuevas características?**
R: v0.0.9 recibirá correcciones de bugs y mejoras de rendimiento, pero las nuevas características se desarrollan en v0.1.0.

---

## Contacto y Soporte

- **Issues**: https://github.com/webcien/Kardo/issues
- **Documentación**: Ver README.md y README_v0.0.9.md
- **Changelog**: Ver CHANGELOG.md

---

## Licencia

Ambas versiones están bajo licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

