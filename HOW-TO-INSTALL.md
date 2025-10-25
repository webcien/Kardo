# KardoCore Installation Guide

Complete installation guide for all KardoCore modes and configurations.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Mode 1: Core Only (Headless/API)](#mode-1-core-only-headlessapi)
4. [Mode 2: Core + Admin](#mode-2-core--admin)
5. [Mode 3: Full CMS (Core + Admin + Theme)](#mode-3-full-cms-core--admin--theme)
6. [Mode 4: Theme Only](#mode-4-theme-only)
7. [CLI Installation](#cli-installation)
8. [npm Installation](#npm-installation)
9. [Configuration](#configuration)
10. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **Python**: 3.11 or higher
- **pip**: 21.0 or higher
- **RAM**: 512MB minimum
- **Disk Space**: 100MB minimum

### Recommended Requirements
- **Python**: 3.12 or higher
- **pip**: 23.0 or higher
- **RAM**: 2GB or more
- **Disk Space**: 500MB or more

### Optional Requirements
- **Node.js**: 18.0+ (for npm packages)
- **npm**: 9.0+ (for frontend assets)
- **PostgreSQL**: 14+ (for production databases)
- **Redis**: 7.0+ (for caching)

---

## Installation Methods

KardoCore can be installed via:
1. **PyPI** (Recommended for production)
2. **GitHub** (For latest features)
3. **CLI** (Recommended for quick project setup)
4. **npm** (For frontend assets)

---

## Mode 1: Core Only (Headless/API)

Perfect for REST APIs, microservices, and headless CMS backends.

### Installation

**From PyPI:**
```bash
pip install kardocore
```

**From GitHub (stable):**
```bash
pip install git+https://github.com/webcien/Kardo.git@v0.0.9
```

**From GitHub (development):**
```bash
pip install git+https://github.com/webcien/Kardo.git@main
```

**Using CLI (Recommended):**
```bash
# Install KardoCore first
pip install kardocore

# Initialize project with CLI
kardo init my-api --mode=core
cd my-api
```

### Quick Start

1. Create a new project:
```bash
mkdir my-api
cd my-api
```

2. Create `app.py`:
```python
from kardocore import KardoApp

app = KardoApp()

@app.route("/")
async def index(request):
    return {"message": "Hello from KardoCore!"}

@app.route("/api/users")
async def get_users(request):
    return {
        "users": [
            {"id": 1, "name": "John Doe"},
            {"id": 2, "name": "Jane Smith"}
        ]
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

3. Run the application:
```bash
python app.py
```

4. Test the API:
```bash
curl http://localhost:8000/
curl http://localhost:8000/api/users
```

### Production Deployment

```bash
# Install production server
pip install uvicorn[standard]

# Run with uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Mode 2: Core + Admin

Adds an admin panel for content management and user administration.

### Installation

**From PyPI:**
```bash
pip install kardocore[admin]
```

**From GitHub (stable):**
```bash
pip install "kardocore[admin] @ git+https://github.com/webcien/Kardo.git@v0.0.9"
```

**Using CLI (Recommended):**
```bash
# Install KardoCore with admin
pip install kardocore[admin]

# Initialize project with CLI
kardo init my-cms-admin --mode=admin
cd my-cms-admin

# Create admin user
kardo user create --username=admin --email=admin@example.com --role=admin
```

### Quick Start

1. Create a new project:
```bash
mkdir my-cms-admin
cd my-cms-admin
```

2. Create `app.py`:
```python
from kardocore import KardoApp
from kardocore.admin import KardoAdmin

app = KardoApp()

# Initialize admin panel
admin = KardoAdmin(
    app,
    title="My CMS Admin",
    base_url="/admin"
)

# Define a model
class Post:
    title: str
    content: str
    published: bool = False
    author: str

# Register model in admin
@admin.register
class PostAdmin:
    model = Post
    list_display = ["title", "author", "published"]
    search_fields = ["title", "content"]
    list_filter = ["published"]

@app.route("/")
async def index(request):
    return {"message": "Visit /admin for admin panel"}

if __name__ == "__main__":
    app.run()
```

3. Run the application:
```bash
python app.py
```

4. Access admin panel:
```
http://localhost:8000/admin
```

### Admin Configuration

Create `admin_config.py`:
```python
ADMIN_CONFIG = {
    "title": "My CMS Admin",
    "site_header": "My CMS Administration",
    "index_title": "Dashboard",
    
    # Authentication
    "auth_enabled": True,
    "login_url": "/admin/login",
    "logout_url": "/admin/logout",
    
    # UI
    "theme": "default",  # default, dark, light
    "logo": "/static/logo.png",
    "favicon": "/static/favicon.ico",
    
    # Features
    "search_enabled": True,
    "filters_enabled": True,
    "export_enabled": True,
    "bulk_actions": True,
    
    # Pagination
    "items_per_page": 25,
    
    # Security
    "csrf_protection": True,
    "session_timeout": 3600,
}
```

---

## Mode 3: Full CMS (Core + Admin + Theme)

Complete CMS solution with backend, admin panel, and frontend templates.

### Installation

**From PyPI:**
```bash
pip install kardocore[full]
```

**From GitHub (stable):**
```bash
pip install "kardocore[full] @ git+https://github.com/webcien/Kardo.git@v0.0.9"
```

**Using CLI (Recommended):**
```bash
# Install KardoCore full
pip install kardocore[full]

# Initialize complete CMS project with CLI
kardo init my-full-cms --mode=full --name="My CMS"
cd my-full-cms

# Install a theme
kardo theme install wellness-clinic

# Create admin user
kardo user create --username=admin --email=admin@example.com --role=admin

# Run migrations
kardo migrate up

# Start development server
kardo serve
```

### Quick Start

1. Create a new project:
```bash
mkdir my-full-cms
cd my-full-cms
```

2. Initialize project structure:
```bash
kardo init --mode=full --name="My CMS"
```

This creates:
```
my-full-cms/
├── app.py
├── config.py
├── models/
│   ├── __init__.py
│   └── post.py
├── routes/
│   ├── __init__.py
│   └── web.py
├── templates/
│   ├── layout.html
│   ├── index.html
│   └── partials/
│       ├── header.html
│       └── footer.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── admin/
    └── config.py
```

3. Install a theme:
```bash
kardo theme install wellness-clinic
```

4. Create `app.py`:
```python
from kardocore import KardoApp
from kardocore.admin import KardoAdmin
from kardocore.theme import KardoTheme

app = KardoApp()
admin = KardoAdmin(app)
theme = KardoTheme(template_dir="templates")

# Models
class Post:
    title: str
    content: str
    published: bool = False

@admin.register
class PostAdmin:
    model = Post

# Frontend routes
@app.route("/")
async def index(request):
    posts = Post.objects.filter(published=True)
    return theme.render("index.html", {
        "title": "My CMS",
        "posts": posts
    })

@app.route("/post/{slug}")
async def post_detail(request, slug):
    post = Post.objects.get(slug=slug)
    return theme.render("post.html", {
        "post": post
    })

if __name__ == "__main__":
    app.run()
```

5. Run the application:
```bash
python app.py
```

6. Access:
- **Frontend**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin

### Using Pre-built Templates

```bash
# List available templates
kardo theme list --available

# Install a template
kardo theme install wellness-clinic

# Activate template
kardo theme activate wellness-clinic

# Customize template
kardo theme customize wellness-clinic
```

---

## Mode 4: Theme Only

Use only the template engine for static sites or frontend projects.

### Installation

**From PyPI:**
```bash
pip install kardotheme
```

**From GitHub:**
```bash
pip install git+https://github.com/webcien/Kardo.git@v0.0.9#subdirectory=kardotheme
```

**Using CLI (Recommended):**
```bash
# Install kardotheme
pip install kardotheme

# Initialize theme-only project
kardo init my-static-site --mode=theme
cd my-static-site

# List available themes
kardo theme list --available

# Install a theme
kardo theme install wellness-clinic

# Build static site
kardo build
```

### Quick Start

1. Create a new project:
```bash
mkdir my-static-site
cd my-static-site
```

2. Create `build.py`:
```python
from kardotheme import KardoTheme
from pathlib import Path

theme = KardoTheme(template_dir="templates")

# Data
pages = [
    {
        "slug": "index",
        "title": "Home",
        "content": "Welcome to my site"
    },
    {
        "slug": "about",
        "title": "About",
        "content": "About us page"
    }
]

# Build pages
output_dir = Path("dist")
output_dir.mkdir(exist_ok=True)

for page in pages:
    html = theme.render("page.html", page)
    
    output_file = output_dir / f"{page['slug']}.html"
    output_file.write_text(html)
    
    print(f"✅ Built: {output_file}")

print(f"\n🎉 Site built successfully in {output_dir}/")
```

3. Create `templates/page.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <div>{content}</div>
</body>
</html>
```

4. Build the site:
```bash
python build.py
```

5. Serve locally:
```bash
python -m http.server --directory dist 8000
```

---

## CLI Installation

The KardoCore CLI provides commands for project initialization, theme management, user administration, and more.

### Installing the CLI

The CLI is automatically installed when you install KardoCore:

```bash
pip install kardocore
```

Verify installation:
```bash
kardo --version
```

### Available CLI Commands

#### 1. `kardo init` - Initialize New Project

```bash
# Core only (API/Headless)
kardo init my-api --mode=core

# Core + Admin
kardo init my-cms --mode=admin

# Full CMS (Core + Admin + Theme)
kardo init my-site --mode=full --name="My Site"

# Theme only (Static site)
kardo init my-static --mode=theme
```

**Options:**
- `--mode` - Installation mode: `core`, `admin`, `full`, `theme`
- `--name` - Project display name
- `--template` - Use a specific template
- `--database` - Database type: `sqlite`, `postgresql`, `mysql`

#### 2. `kardo serve` - Start Development Server

```bash
# Start server (default: localhost:8000)
kardo serve

# Custom host and port
kardo serve --host=0.0.0.0 --port=3000

# With auto-reload
kardo serve --reload
```

**Options:**
- `--host` - Server host (default: `127.0.0.1`)
- `--port` - Server port (default: `8000`)
- `--reload` - Enable auto-reload on file changes

#### 3. `kardo theme` - Manage Themes

```bash
# List available themes
kardo theme list --available

# List installed themes
kardo theme list

# Install a theme
kardo theme install wellness-clinic

# Activate a theme
kardo theme activate wellness-clinic

# Search themes
kardo theme search medical

# Customize theme
kardo theme customize wellness-clinic
```

**Options:**
- `list` - List themes
- `install <name>` - Install theme from repository
- `activate <name>` - Set theme as active
- `search <query>` - Search available themes
- `customize <name>` - Open theme for customization

#### 4. `kardo user` - Manage Users

```bash
# Create new user
kardo user create --username=john --email=john@example.com --role=author

# Create admin user
kardo user create --username=admin --email=admin@example.com --role=admin

# List users
kardo user list

# Change user role
kardo user role john --role=admin

# Delete user
kardo user delete john
```

**Options:**
- `create` - Create new user
- `list` - List all users
- `role <username>` - Change user role
- `delete <username>` - Delete user
- `--username` - Username
- `--email` - Email address
- `--role` - User role: `admin`, `author`, `user`, `guest`

#### 5. `kardo migrate` - Database Migrations

```bash
# Run all pending migrations
kardo migrate up

# Rollback last migration
kardo migrate down

# Show migration status
kardo migrate status

# Create new migration
kardo migrate create add_categories_table
```

**Options:**
- `up` - Run pending migrations
- `down` - Rollback last migration
- `status` - Show migration status
- `create <name>` - Create new migration file

#### 6. `kardo build` - Build for Production

```bash
# Build project
kardo build

# Build with specific output directory
kardo build --output=dist

# Build and minify
kardo build --minify
```

**Options:**
- `--output` - Output directory (default: `dist`)
- `--minify` - Minify assets
- `--optimize` - Optimize images and assets

### Complete CLI Workflow Example

```bash
# 1. Install KardoCore
pip install kardocore[full]

# 2. Initialize project
kardo init my-blog --mode=full --name="My Blog"
cd my-blog

# 3. Install theme
kardo theme install wellness-clinic

# 4. Create admin user
kardo user create --username=admin --email=admin@example.com --role=admin

# 5. Run migrations
kardo migrate up

# 6. Start development server
kardo serve --reload

# 7. Build for production
kardo build --minify
```

### CLI Help

Get help for any command:

```bash
# General help
kardo --help

# Command-specific help
kardo init --help
kardo theme --help
kardo user --help
kardo migrate --help
```

---

## npm Installation

Install frontend assets and build tools via npm.

### KardoCSS

```bash
# Install KardoCSS
npm install @kardo/css

# Or use CDN
# <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@kardo/css@latest/dist/kardo.min.css">
```

### KardoTheme Compiler

```bash
# Install theme compiler
npm install @kardo/theme-compiler

# Compile templates
npx kardo-compile templates/ --output dist/
```

### Complete Frontend Setup

```bash
# Initialize npm project
npm init -y

# Install dependencies
npm install @kardo/css @kardo/theme-compiler

# Install dev dependencies
npm install --save-dev webpack webpack-cli sass postcss autoprefixer

# Add scripts to package.json
```

**package.json:**
```json
{
  "name": "my-kardo-project",
  "version": "1.0.0",
  "scripts": {
    "build": "webpack --mode production",
    "dev": "webpack --mode development --watch",
    "compile-templates": "kardo-compile templates/ --output dist/"
  },
  "dependencies": {
    "@kardo/css": "^0.1.0",
    "@kardo/theme-compiler": "^0.1.0"
  },
  "devDependencies": {
    "webpack": "^5.88.0",
    "webpack-cli": "^5.1.0"
  }
}
```

---

## Configuration

### Environment Variables

Create `.env`:
```bash
# Application
KARDO_ENV=production
KARDO_DEBUG=false
KARDO_SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=secure-password

# KardoAI (optional)
KARDOAI_PROVIDER=openai
KARDOAI_API_KEY=your-api-key
```

### Configuration File

Create `config.py`:
```python
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# Application
DEBUG = os.getenv("KARDO_DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("KARDO_SECRET_KEY", "change-me-in-production")

# Database
DATABASE = {
    "url": os.getenv("DATABASE_URL", "sqlite:///kardo.db"),
    "pool_size": 10,
    "max_overflow": 20,
}

# Templates
TEMPLATES = {
    "dir": BASE_DIR / "templates",
    "auto_reload": DEBUG,
    "cache_enabled": not DEBUG,
}

# Static files
STATIC = {
    "dir": BASE_DIR / "static",
    "url": "/static",
}

# Admin
ADMIN = {
    "enabled": True,
    "base_url": "/admin",
    "title": "My CMS Admin",
}

# KardoAI
KARDOAI = {
    "enabled": True,
    "provider": os.getenv("KARDOAI_PROVIDER", "openai"),
    "api_key": os.getenv("KARDOAI_API_KEY"),
}
```

---

## Troubleshooting

### Common Issues

#### 1. Import Error

```bash
ModuleNotFoundError: No module named 'kardocore'
```

**Solution:**
```bash
pip install --upgrade kardocore
```

#### 2. Python Version

```bash
ERROR: Package requires Python >=3.11
```

**Solution:**
```bash
# Check Python version
python --version

# Upgrade Python or use pyenv
pyenv install 3.12
pyenv global 3.12
```

#### 3. Permission Error

```bash
PermissionError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

pip install kardocore
```

#### 4. Port Already in Use

```bash
OSError: [Errno 48] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python app.py --port 8001
```

### Getting Help

- **Documentation**: https://kardo.dev/docs
- **GitHub Issues**: https://github.com/webcien/Kardo/issues
- **Discord**: https://discord.gg/kardo
- **Email**: support@kardo.dev

---

## Next Steps

After installation:

1. **Read the Quick Start Guide**: [QUICK-START.md](QUICK-START.md)
2. **Explore Examples**: Check the `examples/` directory
3. **Install Templates**: Browse [KardoTemplates](https://github.com/webcien/KardoTemplates)
4. **Join Community**: [Discord](https://discord.gg/kardo)
5. **Read Documentation**: [Full Docs](https://kardo.dev/docs)

---

**Happy coding with KardoCore! 🚀**

