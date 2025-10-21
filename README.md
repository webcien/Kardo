# Kardo

**Ecosistema de Desarrollo Web Moderno con Python y CSS**

---

## 📦 Monorepo

Este repositorio contiene el ecosistema completo de Kardo en fase inicial de desarrollo:

### 🐍 [KardoCore](./KardoCore)

Framework Python híbrido, modular e IA-ready para Headless CMS, CMS completos, APIs y aplicaciones empresariales.

**Características:**
- Arquitectura ASGI asíncrona
- Sistema de validación propio (sin Pydantic)
- Motor de plantillas KardoTheme
- Integración IA nativa
- Modularidad extrema
- Python 3.14+

**[Ver documentación →](./KardoCore/README.md)**

---

### 🎨 [KardoCSS](./KardoCSS)

Framework CSS 100% mobile-first, modular y optimizado. Utility-first con prefijo `k-`.

**Características:**
- 100% Mobile-First
- Utility-First
- Compilador propio
- Prefijo único `k-`
- Sin dependencias
- Responsive

**[Ver documentación →](./KardoCSS/README.md)**

---

## 🚀 Inicio Rápido

### Clonar el Repositorio

```bash
git clone https://github.com/webcien/Kardo.git
cd Kardo
```

### Instalar KardoCore

```bash
cd KardoCore
python3.14 -m venv venv
source venv/bin/activate
pip install -e .
```

### Instalar KardoCSS

```bash
cd ../KardoCSS
pip install -e .
```

### Crear un Proyecto

```bash
# Usar el instalador CLI de KardoCore
kardo new miproyecto --mode full
cd miproyecto
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📚 Documentación

- **[KardoCore README](./KardoCore/README.md)** - Documentación del framework Python
- **[KardoCore Quick Start](./KardoCore/QUICK-START.md)** - Guía de inicio rápido
- **[KardoCore Installation](./KardoCore/HOW-TO-INSTALL.md)** - Guía completa de instalación
- **[KardoCSS README](./KardoCSS/README.md)** - Documentación del framework CSS
- **[Project Summary](./PROJECT_SUMMARY.md)** - Resumen completo del proyecto

---

## 🏗️ Estructura del Proyecto

```
Kardo/
├── KardoCore/          # Framework Python
│   ├── kardocore/      # Código fuente
│   ├── examples/       # Ejemplos
│   ├── tests/          # Tests
│   └── docs/           # Documentación
│
├── KardoCSS/           # Framework CSS
│   ├── kardocss/       # Código fuente
│   ├── examples/       # Ejemplos
│   └── dist/           # CSS compilado
│
└── PROJECT_SUMMARY.md  # Resumen del proyecto
```

---

## 🎯 Filosofía

El ecosistema Kardo se basa en:

1. **Modularidad**: Componentes desacoplados y reutilizables
2. **Simplicidad**: API clara y predecible
3. **Performance**: Optimizado para velocidad
4. **Seguridad**: Validación estricta y sandboxing
5. **Flexibilidad**: Múltiples modos de operación
6. **IA-Ready**: Integración nativa de IA generativa

---

## 🛣️ Roadmap

### Fase Actual: Alpha (v0.1.0)

- [x] Core de KardoCore
- [x] Motor de plantillas KardoTheme
- [x] Sistema de validación propio
- [x] KardoCSS compilador base
- [x] CLI instalador
- [ ] Módulo KardoAI
- [ ] Panel KardoAdmin
- [ ] Tests unitarios
- [ ] Documentación completa

### Próximas Fases

- [ ] Beta (v0.2.0): Sistema de plugins
- [ ] RC (v0.9.0): Optimizaciones y estabilidad
- [ ] v1.0.0: Lanzamiento público

---

## 🤝 Contribuir

Este proyecto está en desarrollo activo. Las contribuciones serán bienvenidas una vez que se lance la versión alpha pública.

Ver guías de contribución:
- [KardoCore CONTRIBUTING.md](./KardoCore/CONTRIBUTING.md)
- [KardoCSS CONTRIBUTING.md](./KardoCSS/CONTRIBUTING.md)

---

## 📄 Licencia

Ambos proyectos están bajo **MIT License**.

- [KardoCore LICENSE](./KardoCore/LICENSE)
- [KardoCSS LICENSE](./KardoCSS/LICENSE)

---

## 👤 Autor

**Juan Quezada**

---

## 🌟 Estado del Proyecto

**Versión**: 0.1.0-alpha  
**Estado**: En desarrollo activo  
**Python**: 3.14+  
**Licencia**: MIT

---

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/webcien/Kardo/issues)
- **Documentación**: Ver carpetas de cada proyecto

---

**Nota**: Este proyecto está en fase alpha. No se recomienda su uso en producción todavía.

