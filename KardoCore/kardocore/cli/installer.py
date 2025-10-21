#!/usr/bin/env python3
"""
KardoCore CLI Installer

Instalador simplificado que permite crear proyectos KardoCore
con un solo comando según el modo deseado.
"""

import os
import sys
import shutil
import secrets
from pathlib import Path
from typing import Optional
import argparse


class Colors:
    """Colores ANSI para terminal."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class KardoInstaller:
    """Instalador principal de KardoCore."""
    
    MODES = {
        'core': 'Solo núcleo ASGI + API (Headless)',
        'admin': 'Core + Panel de Administración',
        'full': 'CMS Completo (Core + Admin + Frontend)',
        'frontend': 'Solo Frontend (Plantillas + KardoCSS)'
    }
    
    def __init__(self, project_name: str, mode: str, directory: Optional[str] = None):
        """
        Inicializa el instalador.
        
        Args:
            project_name: Nombre del proyecto
            mode: Modo de instalación
            directory: Directorio de instalación (opcional)
        """
        self.project_name = project_name
        self.mode = mode
        self.base_dir = Path(directory) if directory else Path.cwd() / project_name
        
    def install(self):
        """Ejecuta la instalación completa."""
        self._print_header()
        self._validate_mode()
        self._create_directory()
        
        if self.mode == 'core':
            self._install_core_only()
        elif self.mode == 'admin':
            self._install_core_admin()
        elif self.mode == 'full':
            self._install_full()
        elif self.mode == 'frontend':
            self._install_frontend_only()
        
        self._create_env_file()
        self._create_requirements()
        self._create_readme()
        self._print_success()
    
    def _print_header(self):
        """Imprime el encabezado del instalador."""
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}  🚀 KardoCore Installer{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}\n")
        print(f"{Colors.GREEN}Proyecto:{Colors.END} {self.project_name}")
        print(f"{Colors.GREEN}Modo:{Colors.END} {self.MODES[self.mode]}")
        print(f"{Colors.GREEN}Directorio:{Colors.END} {self.base_dir}\n")
    
    def _validate_mode(self):
        """Valida que el modo sea válido."""
        if self.mode not in self.MODES:
            print(f"{Colors.RED}❌ Error: Modo '{self.mode}' no válido{Colors.END}")
            print(f"\nModos disponibles:")
            for mode, desc in self.MODES.items():
                print(f"  • {mode}: {desc}")
            sys.exit(1)
    
    def _create_directory(self):
        """Crea el directorio del proyecto."""
        if self.base_dir.exists():
            print(f"{Colors.YELLOW}⚠️  El directorio ya existe. ¿Sobrescribir? (y/N): {Colors.END}", end='')
            response = input().lower()
            if response != 'y':
                print(f"{Colors.RED}❌ Instalación cancelada{Colors.END}")
                sys.exit(0)
            shutil.rmtree(self.base_dir)
        
        self.base_dir.mkdir(parents=True)
        print(f"{Colors.GREEN}✓{Colors.END} Directorio creado")
    
    def _install_core_only(self):
        """Instala solo el núcleo."""
        print(f"\n{Colors.BLUE}📦 Instalando Core Only...{Colors.END}")
        
        # Estructura de directorios
        (self.base_dir / 'core').mkdir()
        (self.base_dir / 'core' / 'routes').mkdir()
        (self.base_dir / 'core' / 'models').mkdir()
        (self.base_dir / 'core' / 'events').mkdir()
        
        # Archivo principal
        self._create_file('core/app.py', self._template_core_app())
        self._create_file('core/__init__.py', '')
        self._create_file('core/routes/__init__.py', '')
        self._create_file('core/models/__init__.py', '')
        self._create_file('core/events/__init__.py', '')
        
        # Configuración
        self._create_file('core/settings.py', self._template_settings())
        
        # Main
        self._create_file('main.py', self._template_main_core())
        
        print(f"{Colors.GREEN}✓{Colors.END} Core instalado")
    
    def _install_core_admin(self):
        """Instala Core + Admin."""
        print(f"\n{Colors.BLUE}📦 Instalando Core + Admin...{Colors.END}")
        
        # Instalar core primero
        self._install_core_only()
        
        # Admin
        (self.base_dir / 'admin').mkdir()
        (self.base_dir / 'admin' / 'templates').mkdir()
        (self.base_dir / 'admin' / 'static').mkdir()
        (self.base_dir / 'admin' / 'static' / 'css').mkdir()
        (self.base_dir / 'admin' / 'static' / 'js').mkdir()
        
        # Templates de admin
        self._create_file('admin/templates/base.html', self._template_admin_base())
        self._create_file('admin/templates/dashboard.html', self._template_admin_dashboard())
        self._create_file('admin/templates/login.html', self._template_admin_login())
        
        # Admin routes
        self._create_file('admin/__init__.py', '')
        self._create_file('admin/routes.py', self._template_admin_routes())
        
        print(f"{Colors.GREEN}✓{Colors.END} Admin instalado")
    
    def _install_full(self):
        """Instala CMS completo."""
        print(f"\n{Colors.BLUE}📦 Instalando CMS Completo...{Colors.END}")
        
        # Instalar core + admin primero
        self._install_core_admin()
        
        # Frontend themes
        (self.base_dir / 'themes').mkdir()
        (self.base_dir / 'themes' / 'frontend').mkdir()
        (self.base_dir / 'themes' / 'frontend' / 'default').mkdir()
        (self.base_dir / 'themes' / 'frontend' / 'default' / 'templates').mkdir()
        (self.base_dir / 'themes' / 'frontend' / 'default' / 'static').mkdir()
        (self.base_dir / 'themes' / 'frontend' / 'default' / 'static' / 'css').mkdir()
        (self.base_dir / 'themes' / 'frontend' / 'default' / 'static' / 'js').mkdir()
        
        # Templates frontend
        self._create_file('themes/frontend/default/templates/base.html', 
                         self._template_frontend_base())
        self._create_file('themes/frontend/default/templates/index.html', 
                         self._template_frontend_index())
        self._create_file('themes/frontend/default/templates/page.html', 
                         self._template_frontend_page())
        self._create_file('themes/frontend/default/templates/post.html', 
                         self._template_frontend_post())
        
        # Theme config
        self._create_file('themes/frontend/default/theme.json', self._template_theme_config())
        
        # Plugins
        (self.base_dir / 'plugins').mkdir()
        
        # AI
        (self.base_dir / 'ai').mkdir()
        (self.base_dir / 'ai' / 'providers').mkdir()
        self._create_file('ai/__init__.py', '')
        self._create_file('ai/providers/__init__.py', '')
        
        # Uploads y media
        (self.base_dir / 'uploads').mkdir()
        (self.base_dir / 'media').mkdir()
        
        print(f"{Colors.GREEN}✓{Colors.END} CMS Completo instalado")
    
    def _install_frontend_only(self):
        """Instala solo frontend."""
        print(f"\n{Colors.BLUE}📦 Instalando Frontend Only...{Colors.END}")
        
        # Themes
        (self.base_dir / 'themes').mkdir()
        (self.base_dir / 'themes' / 'minimal').mkdir()
        (self.base_dir / 'themes' / 'minimal' / 'templates').mkdir()
        (self.base_dir / 'themes' / 'minimal' / 'static').mkdir()
        (self.base_dir / 'themes' / 'minimal' / 'static' / 'css').mkdir()
        
        # Templates
        self._create_file('themes/minimal/templates/index.html', 
                         self._template_frontend_index())
        self._create_file('themes/minimal/templates/page.html', 
                         self._template_frontend_page())
        
        # Theme config
        self._create_file('themes/minimal/theme.json', self._template_theme_config())
        
        # Build script
        self._create_file('build.py', self._template_build_script())
        
        print(f"{Colors.GREEN}✓{Colors.END} Frontend instalado")
    
    def _create_env_file(self):
        """Crea el archivo .env."""
        print(f"\n{Colors.BLUE}🔐 Generando configuración...{Colors.END}")
        
        secret_key = secrets.token_urlsafe(32)
        
        env_content = f"""# KardoCore Configuration
# Generado automáticamente por el instalador

# General
KARDO_DEBUG=true
KARDO_ENVIRONMENT=development
KARDO_MODE={self.mode}

# Servidor
KARDO_HOST=127.0.0.1
KARDO_PORT=8000

# Seguridad
KARDO_SECRET_KEY={secret_key}
KARDO_ALLOWED_HOSTS=*

# Base de datos
KARDO_DATABASE_URL=sqlite:///{self.project_name}.db

# IA (opcional)
KARDO_AI_ENABLED=false
KARDO_AI_PROVIDER=openai
KARDO_AI_API_KEY=

# Temas
KARDO_THEME_FRONTEND=default
KARDO_THEME_ADMIN=default

# Caché
KARDO_CACHE_ENABLED=true
KARDO_CACHE_TTL=3600

# Logging
KARDO_LOG_LEVEL=INFO
KARDO_LOG_FILE={self.project_name}.log
"""
        
        self._create_file('.env', env_content)
        self._create_file('.env.example', env_content)
        print(f"{Colors.GREEN}✓{Colors.END} Configuración generada")
    
    def _create_requirements(self):
        """Crea requirements.txt."""
        requirements = """# KardoCore Dependencies
uvicorn>=0.30.0
python-dotenv>=1.0.0
"""
        
        if self.mode in ['admin', 'full']:
            requirements += """
# Admin dependencies
jinja2>=3.1.0
"""
        
        if self.mode == 'full':
            requirements += """
# Full CMS dependencies
aiofiles>=23.0.0
"""
        
        self._create_file('requirements.txt', requirements)
    
    def _create_readme(self):
        """Crea README.md."""
        readme = f"""# {self.project_name}

Proyecto KardoCore - Modo: {self.MODES[self.mode]}

## Instalación

```bash
# Crear entorno virtual
python3.14 -m venv venv
source venv/bin/activate  # En Windows: venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt
```

## Configuración

Edita el archivo `.env` con tu configuración.

## Ejecutar

```bash
# Desarrollo
uvicorn main:app --reload

# Producción
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Acceso

"""
        
        if self.mode in ['core', 'admin', 'full']:
            readme += """- API: http://localhost:8000/api/
- Docs: http://localhost:8000/docs/
"""
        
        if self.mode in ['admin', 'full']:
            readme += """- Admin: http://localhost:8000/admin/
"""
        
        if self.mode == 'full':
            readme += """- Frontend: http://localhost:8000/
"""
        
        readme += f"""
## Documentación

- [KardoCore Docs](https://docs.kardocore.dev)
- [GitHub](https://github.com/webcien/KardoCore)

---

Generado con KardoCore Installer v0.1.0-alpha
"""
        
        self._create_file('README.md', readme)
    
    def _create_file(self, path: str, content: str):
        """Crea un archivo con contenido."""
        file_path = self.base_dir / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding='utf-8')
    
    def _print_success(self):
        """Imprime mensaje de éxito."""
        print(f"\n{Colors.GREEN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.GREEN}  ✨ Instalación completada exitosamente{Colors.END}")
        print(f"{Colors.GREEN}{'='*60}{Colors.END}\n")
        
        print(f"{Colors.CYAN}Próximos pasos:{Colors.END}\n")
        print(f"  1. cd {self.project_name}")
        print(f"  2. python3.14 -m venv venv")
        print(f"  3. source venv/bin/activate")
        print(f"  4. pip install -r requirements.txt")
        
        if self.mode in ['core', 'admin', 'full']:
            print(f"  5. uvicorn main:app --reload")
        elif self.mode == 'frontend':
            print(f"  5. python build.py")
        
        print(f"\n{Colors.YELLOW}📚 Documentación:{Colors.END} https://docs.kardocore.dev")
        print(f"{Colors.YELLOW}💬 Comunidad:{Colors.END} https://community.kardocore.dev\n")
    
    # Templates
    
    def _template_core_app(self):
        """Template para core/app.py."""
        return '''"""
Aplicación principal de KardoCore
"""

from kardocore import KardoApp, JSONResponse

app = KardoApp(title="''' + self.project_name + '''", version="1.0.0")


@app.get("/")
async def index(request):
    """Endpoint raíz."""
    return {
        "message": "¡Bienvenido a KardoCore!",
        "project": "''' + self.project_name + '''",
        "mode": "''' + self.mode + '''"
    }


@app.get("/api/health")
async def health(request):
    """Health check."""
    return {"status": "healthy", "version": "1.0.0"}


@app.on_event("on_startup")
async def startup():
    """Ejecutado al iniciar."""
    print("🚀 Aplicación iniciada")


@app.on_event("on_shutdown")
async def shutdown():
    """Ejecutado al cerrar."""
    print("👋 Aplicación detenida")
'''
    
    def _template_settings(self):
        """Template para settings.py."""
        return '''"""
Configuración del proyecto
"""

import os
from pathlib import Path

# Directorios
BASE_DIR = Path(__file__).parent.parent
THEMES_DIR = BASE_DIR / "themes"
UPLOADS_DIR = BASE_DIR / "uploads"
MEDIA_DIR = BASE_DIR / "media"

# Configuración desde .env
DEBUG = os.getenv("KARDO_DEBUG", "false").lower() == "true"
SECRET_KEY = os.getenv("KARDO_SECRET_KEY", "change-this-in-production")
DATABASE_URL = os.getenv("KARDO_DATABASE_URL", "sqlite:///''' + self.project_name + '''.db")

# Servidor
HOST = os.getenv("KARDO_HOST", "127.0.0.1")
PORT = int(os.getenv("KARDO_PORT", 8000))
'''
    
    def _template_main_core(self):
        """Template para main.py."""
        return '''"""
Punto de entrada principal
"""

from core.app import app

if __name__ == "__main__":
    import uvicorn
    from core.settings import HOST, PORT, DEBUG
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=DEBUG
    )
'''
    
    def _template_admin_base(self):
        """Template para admin base.html."""
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page.title} - Admin</title>
    <link rel="stylesheet" href="/admin/static/css/admin.css">
</head>
<body>
    <nav>
        <h1>KardoAdmin</h1>
        <ul>
            <li><a href="/admin/">Dashboard</a></li>
            <li><a href="/admin/content/">Contenido</a></li>
            <li><a href="/admin/users/">Usuarios</a></li>
        </ul>
    </nav>
    
    <main>
        #block content
        #end
    </main>
</body>
</html>
'''
    
    def _template_admin_dashboard(self):
        """Template para admin dashboard.html."""
        return '''#extends "base.html"

#block content
<h1>Dashboard</h1>
<p>Bienvenido al panel de administración de ''' + self.project_name + '''</p>

<div class="stats">
    <div class="stat">
        <h3>Páginas</h3>
        <p>{stats.pages}</p>
    </div>
    <div class="stat">
        <h3>Posts</h3>
        <p>{stats.posts}</p>
    </div>
    <div class="stat">
        <h3>Usuarios</h3>
        <p>{stats.users}</p>
    </div>
</div>
#end
'''
    
    def _template_admin_login(self):
        """Template para admin login.html."""
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Admin</title>
</head>
<body>
    <div class="login-container">
        <h1>KardoAdmin</h1>
        <form method="post">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
    </div>
</body>
</html>
'''
    
    def _template_admin_routes(self):
        """Template para admin routes.py."""
        return '''"""
Rutas del panel de administración
"""

from kardocore import HTMLResponse
from kardocore.theme import KardoTheme

theme = KardoTheme(template_dir="admin/templates")


async def dashboard(request):
    """Dashboard principal."""
    html = theme.render("dashboard.html", {
        "page": {"title": "Dashboard"},
        "stats": {
            "pages": 10,
            "posts": 25,
            "users": 5
        }
    })
    return HTMLResponse(html)


async def login(request):
    """Login."""
    html = theme.render("login.html", {})
    return HTMLResponse(html)
'''
    
    def _template_frontend_base(self):
        """Template para frontend base.html."""
        return '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page.title} - ''' + self.project_name + '''</title>
    <link rel="stylesheet" href="/static/css/kardocss.min.css">
</head>
<body class="k-bg-gray-100">
    <header class="k-bg-primary k-text-white k-p-4">
        <div class="k-container k-mx-auto">
            <h1 class="k-text-2xl k-font-bold">{site.name}</h1>
        </div>
    </header>
    
    <main class="k-container k-mx-auto k-p-4">
        #block content
        #end
    </main>
    
    <footer class="k-bg-gray-800 k-text-white k-p-4 k-mt-8">
        <div class="k-container k-mx-auto k-text-center">
            <p>&copy; 2025 ''' + self.project_name + '''. Powered by KardoCore.</p>
        </div>
    </footer>
</body>
</html>
'''
    
    def _template_frontend_index(self):
        """Template para frontend index.html."""
        return '''#extends "base.html"

#block content
<h1 class="k-text-4xl k-font-bold k-mb-4">{page.title}</h1>
<p class="k-text-lg k-text-gray-700 k-mb-8">{page.description}</p>

<div class="k-grid k-grid-cols-1 k-md:grid-cols-2 k-lg:grid-cols-3 k-gap-6">
    #for post in posts
        <article class="k-bg-white k-p-6 k-rounded-lg k-shadow-md">
            <h2 class="k-text-xl k-font-semibold k-mb-2">{post.title}</h2>
            <p class="k-text-gray-600">{post.excerpt}</p>
            <a href="/posts/{post.id}" class="k-text-primary">Leer más →</a>
        </article>
    #end
</div>
#end
'''
    
    def _template_frontend_page(self):
        """Template para frontend page.html."""
        return '''#extends "base.html"

#block content
<article>
    <h1 class="k-text-4xl k-font-bold k-mb-4">{page.title}</h1>
    <div class="k-prose">
        {page.content}
    </div>
</article>
#end
'''
    
    def _template_frontend_post(self):
        """Template para frontend post.html."""
        return '''#extends "base.html"

#block content
<article>
    <h1 class="k-text-4xl k-font-bold k-mb-2">{post.title}</h1>
    <p class="k-text-gray-600 k-mb-6">Por {post.author} - {post.date}</p>
    <div class="k-prose">
        {post.content}
    </div>
</article>
#end
'''
    
    def _template_theme_config(self):
        """Template para theme.json."""
        return '''{
  "name": "Default Theme",
  "version": "1.0.0",
  "author": "KardoCore",
  "description": "Tema por defecto de KardoCore",
  "settings": {
    "primary_color": "#3498db",
    "secondary_color": "#2ecc71"
  }
}
'''
    
    def _template_build_script(self):
        """Template para build.py (frontend only)."""
        return '''#!/usr/bin/env python3
"""
Script de compilación para frontend
"""

from pathlib import Path
from kardocore.theme import KardoTheme

def build():
    """Compila las plantillas a HTML estático."""
    theme = KardoTheme(template_dir="themes/minimal/templates")
    output_dir = Path("dist")
    output_dir.mkdir(exist_ok=True)
    
    # Compilar index
    html = theme.render("index.html", {
        "site": {"name": "''' + self.project_name + '''"},
        "page": {
            "title": "Inicio",
            "description": "Bienvenido a mi sitio"
        },
        "posts": []
    })
    
    (output_dir / "index.html").write_text(html, encoding="utf-8")
    print("✓ index.html compilado")

if __name__ == "__main__":
    build()
'''


def main():
    """Punto de entrada del CLI."""
    parser = argparse.ArgumentParser(
        description="KardoCore Installer - Crea proyectos KardoCore con un solo comando",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modos disponibles:
  core      - Solo núcleo ASGI + API (Headless)
  admin     - Core + Panel de Administración
  full      - CMS Completo (Core + Admin + Frontend)
  frontend  - Solo Frontend (Plantillas + KardoCSS)

Ejemplos:
  kardo new myproject --mode core
  kardo new myblog --mode full
  kardo new mytheme --mode frontend
        """
    )
    
    parser.add_argument(
        'action',
        choices=['new', 'init'],
        help='Acción a realizar'
    )
    
    parser.add_argument(
        'name',
        help='Nombre del proyecto'
    )
    
    parser.add_argument(
        '-m', '--mode',
        required=True,
        choices=['core', 'admin', 'full', 'frontend'],
        help='Modo de instalación'
    )
    
    parser.add_argument(
        '-d', '--directory',
        help='Directorio de instalación (opcional)'
    )
    
    args = parser.parse_args()
    
    try:
        installer = KardoInstaller(args.name, args.mode, args.directory)
        installer.install()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}⚠️  Instalación cancelada por el usuario{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}❌ Error durante la instalación: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main()

