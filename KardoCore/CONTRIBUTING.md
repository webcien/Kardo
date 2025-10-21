# Contribuir a KardoCore

¡Gracias por tu interés en contribuir a KardoCore! Este documento proporciona pautas para contribuir al proyecto.

## Código de Conducta

Al participar en este proyecto, te comprometes a mantener un ambiente respetuoso y colaborativo.

## Cómo Contribuir

### Reportar Bugs

Si encuentras un bug, por favor crea un issue con:

- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Versión de Python y KardoCore
- Sistema operativo

### Sugerir Mejoras

Las sugerencias de nuevas características son bienvenidas. Por favor:

- Verifica que no exista un issue similar
- Describe claramente la funcionalidad propuesta
- Explica por qué sería útil para el proyecto

### Pull Requests

1. **Fork el repositorio**
2. **Crea una rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commits con mensajes claros** siguiendo [Conventional Commits](https://www.conventionalcommits.org/)
4. **Escribe tests** para tu código
5. **Asegúrate de que los tests pasen** (`pytest`)
6. **Actualiza la documentación** si es necesario
7. **Push a tu fork** (`git push origin feature/AmazingFeature`)
8. **Abre un Pull Request**

### Estándares de Código

- **Python 3.14+** como versión mínima
- **PEP 8** para estilo de código
- **Type hints** en todas las funciones públicas
- **Docstrings** en formato Google/NumPy
- **Tests** con pytest para nuevas funcionalidades
- **Black** para formateo automático
- **Mypy** para verificación de tipos

### Estructura de Commits

```
tipo(alcance): descripción breve

Descripción más detallada si es necesario.

Fixes #123
```

Tipos válidos:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Formateo, sin cambios de código
- `refactor`: Refactorización de código
- `test`: Agregar o modificar tests
- `chore`: Tareas de mantenimiento

### Tests

```bash
# Ejecutar todos los tests
pytest

# Con coverage
pytest --cov=kardocore

# Tests específicos
pytest tests/test_models.py
```

### Documentación

- Actualiza el README.md si cambias funcionalidad pública
- Agrega docstrings a nuevas funciones/clases
- Actualiza ejemplos si es necesario

## Proceso de Revisión

1. Un mantenedor revisará tu PR
2. Se pueden solicitar cambios
3. Una vez aprobado, se hará merge

## Preguntas

Si tienes preguntas, abre un issue con la etiqueta `question`.

## Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la licencia MIT del proyecto.

