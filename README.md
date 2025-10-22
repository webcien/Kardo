# KardoCore

**Modern Python Framework for CMS, Headless CMS, APIs and Enterprise Applications**

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-0.0.9-orange.svg)](https://github.com/webcien/Kardo/releases/tag/v0.0.9)

---

## 🌟 Overview

**KardoCore** is a hybrid, modular, and AI-ready Python framework designed for building modern web applications, CMS platforms, headless CMS, REST APIs, and enterprise solutions.

### Key Features

- ⚡ **Asynchronous ASGI Architecture** - Built for high performance
- 🎨 **Native Template Engine (KardoTheme)** - Natural syntax with `#` prefix
- 📦 **Package Manager** - Install and manage themes easily
- 🔒 **Built-in Validation System** - No external dependencies
- 🤖 **AI-Ready** - Native integration for AI features
- 🧩 **Extreme Modularity** - Use only what you need
- 🌍 **Multi-language Support** - i18n ready

---

## 📋 Version Information

KardoCore is available in **two versions** to support different Python environments:

### 🎯 v0.0.9 (Stable) - **RECOMMENDED FOR PRODUCTION**
- **Python**: >= 3.11
- **Status**: Stable and production-ready
- **Branch**: `v0.0.9`
- **Compatible with**: Python 3.11, 3.12, 3.13, 3.14+

### 🚀 v0.1.0-alpha (Development)
- **Python**: >= 3.14
- **Status**: Active development
- **Branch**: `main`
- **Features**: Uses Python 3.14 modern features (PEP 649/749)

**📖 [See detailed version comparison →](VERSION_INFO.md)**

---

## 🚀 Quick Start

### Installation

**For production (Python 3.11+):**
```bash
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

**For development (Python 3.14+):**
```bash
pip install git+https://github.com/webcien/Kardo.git@main
```

### Hello World

```python
from kardocore import KardoApp

app = KardoApp()

@app.route("/")
async def index(request):
    return {"message": "Hello from KardoCore!"}

if __name__ == "__main__":
    app.run()
```

Run your app:
```bash
python app.py
```

Visit: http://localhost:8000

---

## 🎨 Template Engine (KardoTheme)

KardoCore includes a powerful native template engine with natural syntax.

### Template Example

**templates/index.html:**
```html
<!DOCTYPE html>
<html lang="en">
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
        <p>No items available</p>
    #end
    
    #include "partials/footer.html"
</body>
</html>
```

### Using Templates

```python
from kardocore.theme import KardoTheme

theme = KardoTheme(template_dir="templates")

context = {
    "title": "My Store",
    "items": [
        {"name": "Product 1", "price": 29.99},
        {"name": "Product 2", "price": 39.99}
    ]
}

html = theme.render("index.html", context)
print(html)
```

### Template Syntax

| Syntax | Description | Example |
|--------|-------------|---------|
| `{variable}` | Variable interpolation | `{user.name}` |
| `#if condition` | Conditional | `#if user.is_admin` |
| `#else` | Else clause | `#else` |
| `#end` | End block | `#end` |
| `#for item in items` | Loop | `#for post in posts` |
| `#include "file"` | Include template | `#include "header.html"` |
| `{# comment #}` | Comment | `{# TODO: fix this #}` |

---

## 📦 Package Manager

Install and manage themes from the official registry.

### CLI Commands

```bash
# Install a theme
kardo theme install wellness-clinic

# List installed themes
kardo theme list

# Search themes
kardo theme search health

# View theme info
kardo theme info wellness-clinic

# Uninstall theme
kardo theme uninstall wellness-clinic
```

### Programmatic Usage

```python
from kardocore.packages import PackageManager

pm = PackageManager()

# Install theme
pm.install_theme("wellness-clinic")

# List themes
themes = pm.list_themes()

# Search themes
results = pm.search_themes(query="health", category="salud-bienestar")
```

---

## 🏗️ Project Structure

```
my_project/
├── app.py              # Main application
├── templates/          # KardoTheme templates
│   ├── layout.html
│   ├── index.html
│   └── partials/
│       ├── header.html
│       └── footer.html
├── static/             # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── models/             # Data models
├── routes/             # Route handlers
└── requirements.txt
```

---

## 📚 Documentation

- **[Installation Guide](HOW-TO-INSTALL.md)** - Detailed installation instructions
- **[Quick Start Guide](QUICK-START.md)** - Get started in 5 minutes
- **[Version Info](VERSION_INFO.md)** - Compare v0.0.9 and v0.1.0
- **[Changelog](CHANGELOG.md)** - Version history
- **[Contributing](CONTRIBUTING.md)** - How to contribute

### Language-Specific Documentation

- 🇺🇸 **English**: README.md (this file)
- 🇪🇸 **Español**: [README.es.md](README.es.md)

---

## 🌐 Ecosystem

KardoCore is part of the **Kardo Ecosystem**:

### [KardoCSS](https://github.com/webcien/KardoCSS)
Mobile-first CSS framework with utilities and components
- 67KB full / 50KB minified
- 20+ components
- 100+ utilities
- Touch-optimized

### [KardoTemplates](https://github.com/webcien/KardoTemplates)
Professional template collection for KardoCore
- 60 templates (50 frontend + 10 backend)
- 15 frontend categories
- 2 backend categories
- Mobile-first responsive

---

## 🎯 Use Cases

- ✅ **CMS Platforms** - Full-featured content management systems
- ✅ **Headless CMS** - API-first content platforms
- ✅ **REST APIs** - Fast and scalable APIs
- ✅ **Web Applications** - Modern web apps
- ✅ **Enterprise Solutions** - Business applications
- ✅ **E-commerce** - Online stores
- ✅ **Blogs & Portfolios** - Personal websites

---

## 🔧 Requirements

### For v0.0.9 (Stable)
- Python >= 3.11
- uvicorn >= 0.30.0

### For v0.1.0-alpha (Development)
- Python >= 3.14
- uvicorn >= 0.30.0

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Clone repository
git clone https://github.com/webcien/Kardo.git
cd Kardo

# For stable version
git checkout v0.0.9

# For development version
git checkout main

# Install in development mode
pip install -e .

# Run tests
pytest
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Inspired by modern Python frameworks
- Built with performance and developer experience in mind
- Community-driven development

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/webcien/Kardo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/webcien/Kardo/discussions)
- **Documentation**: [Full Documentation](https://github.com/webcien/Kardo/wiki)

---

## 🗺️ Roadmap

### v0.0.9 (Current - Stable)
- ✅ Python 3.11+ compatibility
- ✅ Core features complete
- 🔄 Bug fixes and improvements
- 🔄 Documentation

### v0.1.0-alpha (Current - Development)
- ✅ Python 3.14+ optimizations
- 🔄 Experimental features
- 📅 Integrated caching system
- 📅 Multi-database support
- 📅 Automatic REST API
- 📅 GraphQL support

### v1.0.0 (Future)
- 📅 Stable unified version
- 📅 Python 3.14+ as minimum requirement
- 📅 Complete documentation
- 📅 Comprehensive testing
- 📅 Production-ready

---

## ⭐ Star History

If you find KardoCore useful, please consider giving it a star on GitHub!

---

**Made with ❤️ by the Kardo Team**

