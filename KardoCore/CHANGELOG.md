# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.1.0-alpha] - 2025-10-21

### Agregado
- Versión inicial del framework KardoCore
- Sistema ASGI personalizado sin dependencias externas
- Motor de plantillas KardoTheme con sintaxis natural
- Sistema de validación de modelos propio (sin Pydantic)
- Sistema de eventos asíncronos
- PackageManager para gestión de plantillas
- CLI para instalación y gestión

### Requisitos
- Python >= 3.14
- Aprovecha características de Python 3.14 (PEP 649/749)
- `annotationlib` para anotaciones diferidas

## [0.0.9] - 2025-10-21

### Agregado
- Versión compatible con Python 3.11+
- Todas las características de v0.1.0-alpha
- Fallbacks para características de Python 3.14

### Cambiado
- Compatibilidad con Python >= 3.11 (en lugar de >= 3.14)
- Reemplazo de `annotationlib` con fallback a `typing.get_type_hints`
- Reemplazo de union types (`int | None`) con `Optional[int]`
- Reemplazo de `callable` con `Callable` de typing

### Corregido
- Importaciones compatibles con Python 3.11
- Sintaxis de type hints compatible con Python 3.11
- Sistema de anotaciones con fallback para versiones anteriores

### Requisitos
- Python >= 3.11
- Compatible con Python 3.11, 3.12, 3.13, 3.14+

### Notas de Migración
Si estás usando Python 3.14+, se recomienda usar la versión v0.1.0-alpha que aprovecha las nuevas características del lenguaje. Esta versión v0.0.9 es para compatibilidad con versiones anteriores de Python.

## [Unreleased]

### Planeado
- Sistema de caché integrado
- Soporte para múltiples bases de datos
- Sistema de migraciones
- Autenticación y autorización integrada
- API REST automática
- GraphQL support
- WebSocket support
- Testing utilities
- Documentación completa

