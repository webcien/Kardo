KardoCore - Guía de Instalación y Configuración

**Versión**: 0.1.0-alpha**Fecha**: Octubre 2025

---

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)

1. [Métodos de Instalación](#m%C3%A9todos-de-instalaci%C3%B3n)

1. [Modos de Operación](#modos-de-operaci%C3%B3n)

1. [Configuración Inicial](#configuraci%C3%B3n-inicial)

1. [Instalación por Entorno](#instalaci%C3%B3n-por-entorno)

1. [Verificación de la InstalaciónC](#verificaci%C3%B3n-de-la-instalaci%C3%B3n)

1. [Solución de Problemas](#soluci%C3%B3n-de-problemas)

---

## Requisitos del Sistema

### Requisitos Mínimos

- **Python**: 3.14 o superior

- **Sistema Operativo**: Linux, macOS, o Windows

- **RAM**: 512 MB mínimo (2 GB recomendado)

- **Espacio en Disco**: 100 MB para instalación base

### Dependencias del Sistema

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.14 python3.14-venv python3-pip git

# macOS (con Homebrew)
brew install python@3.14 git

# Windows
# Descargar Python 3.14 desde python.org
```

---

## Métodos de Instalación

### Método 1: Instalación desde Código Fuente (Recomendado para Desarrollo)

```bash
# 1. Clonar el repositorio
git clone https://github.com/webcien/KardoCore.git
cd kardocore

# 2. Crear entorno virtual
python3.14 -m venv venv

# 3. Activar entorno virtual
# En Linux/macOS:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# 4. Instalar en modo desarrollo
pip install -e .

# 5. Instalar dependencias de desarrollo (opcional)
pip install -e ".[dev]"
```

### Método 2: Instalación desde PyPI (Próximamente)

```bash
# Cuando esté publicado en PyPI
pip install kardocore
```

### Método 3: Instalación con Docker (Próximamente)

```bash
# Usando Docker
docker pull kardocore/kardocore:latest
docker run -p 8000:8000 kardocore/kardocore
```

---

## Modos de Operación

KardoCore puede operar en diferentes modos según las necesidades del proyecto:

### 1. **Modo Headless CMS (Solo API)**

Expone solo endpoints de API REST/GraphQL sin frontend.

**Casos de uso:**

- Backend para aplicaciones móviles

- API para aplicaciones SPA (React, Vue, Angular)

- Microservicios

- Integraciones con sistemas externos

**Instalación:**

```bash
# 1. Instalar KardoCore (método 1 o 2)
pip install -e .

# 2. Crear archivo de configuración
cp .env.example .env

# 3. Editar .env
nano .env
```

**Configuración (.env):**

```bash
# Modo Headless
KARDO_MODE=headless
KARDO_DEBUG=false
KARDO_ENVIRONMENT=production

# Servidor
KARDO_HOST=0.0.0.0
KARDO_PORT=8000

# Seguridad
KARDO_SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
KARDO_ALLOWED_HOSTS=api.tudominio.com

# Base de datos
KARDO_DATABASE_URL=postgresql://user:pass@localhost/kardocore

# IA (opcional)
KARDO_AI_ENABLED=true
KARDO_AI_PROVIDER=openai
KARDO_AI_API_KEY=tu-api-key-de-openai

# Temas (no se usan en headless)
KARDO_THEME_FRONTEND=none
KARDO_THEME_ADMIN=default
```

**Ejecutar:**

```bash
# Desarrollo
uvicorn kardocore.main:app --reload --host 0.0.0.0 --port 8000

# Producción
uvicorn kardocore.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**Acceso:**

- API: `http://localhost:8000/api/`

- Admin: `http://localhost:8000/admin/`

- Docs: `http://localhost:8000/docs/`

---

### 2. **Modo CMS Completo (Backend + Frontend)**

Incluye backend, frontend público y panel de administración.

**Casos de uso:**

- Sitios web corporativos

- Blogs y publicaciones

- Portales de contenido

- Sitios de documentación

**Instalación:**

```bash
# 1. Instalar KardoCore
pip install -e .

# 2. Instalar KardoCSS (opcional pero recomendado)
cd ../kardocss
pip install -e .
cd ../kardocore

# 3. Crear estructura de temas
mkdir -p themes/frontend themes/admin

# 4. Copiar temas por defecto
cp -r examples/themes/frontend themes/
cp -r examples/themes/admin themes/

# 5. Compilar KardoCSS
cd ../kardocss
python -m kardocss.cli.build -o ../kardocore/themes/frontend/static/css/kardocss.min.css --minify
cd ../kardocore

# 6. Configurar
cp .env.example .env
nano .env
```

**Configuración (.env):**

```bash
# Modo CMS Completo
KARDO_MODE=full_cms
KARDO_DEBUG=false
KARDO_ENVIRONMENT=production

# Servidor
KARDO_HOST=0.0.0.0
KARDO_PORT=8000

# Seguridad
KARDO_SECRET_KEY=tu-clave-secreta-muy-larga-y-segura-aqui
KARDO_ALLOWED_HOSTS=www.tudominio.com,tudominio.com

# Base de datos
KARDO_DATABASE_URL=postgresql://user:pass@localhost/kardocore

# IA
KARDO_AI_ENABLED=true
KARDO_AI_PROVIDER=openai
KARDO_AI_API_KEY=tu-api-key-de-openai
KARDO_AI_MODEL=gpt-4

# Temas
KARDO_THEME_FRONTEND=frontend
KARDO_THEME_ADMIN=admin

# Caché
KARDO_CACHE_ENABLED=true
KARDO_CACHE_TTL=3600
```

**Estructura de Directorios:**

```
kardocore/
├── themes/
│   ├── frontend/              # Tema del sitio público
│   │   ├── templates/
│   │   │   ├── base.html
│   │   │   ├── index.html
│   │   │   ├── page.html
│   │   │   └── post.html
│   │   ├── static/
│   │   │   ├── css/
│   │   │   │   └── kardocss.min.css
│   │   │   ├── js/
│   │   │   └── images/
│   │   └── config/
│   │       └── theme.yaml
│   │
│   └── admin/                 # Tema del panel de administración
│       ├── templates/
│       │   ├── base.html
│       │   ├── dashboard.html
│       │   └── content/
│       ├── static/
│       │   ├── css/
│       │   └── js/
│       └── config/
│           └── theme.yaml
│
├── uploads/                   # Archivos subidos
├── media/                     # Media generada
└── kardocore.db              # Base de datos (SQLite)
```

**Ejecutar:**

```bash
# Desarrollo
uvicorn kardocore.main:app --reload --host 0.0.0.0 --port 8000

# Producción con Gunicorn + Uvicorn workers
gunicorn kardocore.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Acceso:**

- Frontend: `http://localhost:8000/`

- Admin: `http://localhost:8000/admin/`

- API: `http://localhost:8000/api/`

---

### 3. **Modo Híbrido (API + Frontend Estático)**

API backend con frontend pre-renderizado o SSG.

**Casos de uso:**

- Sitios con alta performance

- JAMstack

- Sitios con contenido mayormente estático

**Configuración (.env):**

```bash
KARDO_MODE=hybrid
KARDO_STATIC_GENERATION=true
KARDO_STATIC_OUTPUT_DIR=./dist
```

---

### 4. **Modo eCommerce**

CMS completo con funcionalidades de comercio electrónico.

**Configuración (.env):**

```bash
KARDO_MODE=ecommerce
KARDO_ECOMMERCE_ENABLED=true
KARDO_PAYMENT_PROVIDER=stripe
KARDO_STRIPE_API_KEY=tu-stripe-key
```

---

## Configuración Inicial

### 1. Crear Usuario Administrador

```bash
# Usando CLI de KardoCore
krd create-admin

# O mediante Python
python -c "from kardocore.cli import create_admin; create_admin()"
```

**Interactivo:**

```
Crear Usuario Administrador
===========================
Nombre: Juan Quezada
Email: admin@tudominio.com
Contraseña: ********
Confirmar contraseña: ********

✅ Usuario administrador creado exitosamente
```

### 2. Inicializar Base de Datos

```bash
# Crear tablas
krd db init

# Ejecutar migraciones
krd db migrate

# Seed de datos de ejemplo (opcional)
krd db seed
```

### 3. Configurar Temas

**Archivo: ****`themes/frontend/config/theme.yaml`**

```yaml
name: "Mi Tema Frontend"
version: "1.0.0"
author: "Tu Nombre"

settings:
  logo: "/static/images/logo.png"
  primary_color: "#3498db"
  secondary_color: "#2ecc71"
  
templates:
  index: "index.html"
  page: "page.html"
  post: "post.html"
  archive: "archive.html"

menus:
  main:
    - title: "Inicio"
      url: "/"
    - title: "Blog"
      url: "/blog"
    - title: "Contacto"
      url: "/contacto"
```

---

## Instalación por Entorno

### Desarrollo Local

```bash
# 1. Clonar repositorio
git clone https://github.com/webcien/KardoCore.git
cd kardocore

# 2. Entorno virtual
python3.14 -m venv venv
source venv/bin/activate

# 3. Instalar en modo desarrollo
pip install -e ".[dev]"

# 4. Configurar
cp .env.example .env
nano .env

# Configuración de desarrollo
KARDO_DEBUG=true
KARDO_ENVIRONMENT=development
KARDO_DATABASE_URL=sqlite:///kardocore_dev.db

# 5. Inicializar
krd db init
krd create-admin

# 6. Ejecutar
uvicorn kardocore.main:app --reload
```

**Acceso:** `http://localhost:8000`

---

### Staging/Testing

```bash
# 1. Clonar en servidor
git clone https://github.com/webcien/KardoCore.git
cd kardocore

# 2. Entorno virtual
python3.14 -m venv venv
source venv/bin/activate

# 3. Instalar
pip install -e .

# 4. Configurar
cp .env.example .env
nano .env

# Configuración de staging
KARDO_DEBUG=false
KARDO_ENVIRONMENT=staging
KARDO_DATABASE_URL=postgresql://user:pass@localhost/kardocore_staging
KARDO_ALLOWED_HOSTS=staging.tudominio.com

# 5. Inicializar
krd db migrate
krd create-admin

# 6. Ejecutar con systemd
sudo systemctl start kardocore
```

---

### Producción

#### Opción 1: Servidor VPS (Ubuntu/Debian)

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias
sudo apt install python3.14 python3.14-venv nginx postgresql redis-server -y

# 3. Crear usuario
sudo useradd -m -s /bin/bash kardocore
sudo su - kardocore

# 4. Clonar repositorio
git clone https://github.com/webcien/KardoCore.git
cd kardocore

# 5. Entorno virtual
python3.14 -m venv venv
source venv/bin/activate

# 6. Instalar
pip install -e .
pip install gunicorn

# 7. Configurar
cp .env.example .env
nano .env

# Configuración de producción
KARDO_DEBUG=false
KARDO_ENVIRONMENT=production
KARDO_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
KARDO_DATABASE_URL=postgresql://kardocore:password@localhost/kardocore_prod
KARDO_ALLOWED_HOSTS=www.tudominio.com,tudominio.com

# 8. Configurar PostgreSQL
sudo -u postgres psql
CREATE DATABASE kardocore_prod;
CREATE USER kardocore WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE kardocore_prod TO kardocore;
\q

# 9. Inicializar
krd db migrate
krd create-admin

# 10. Crear servicio systemd
exit  # Salir del usuario kardocore
sudo nano /etc/systemd/system/kardocore.service
```

**Archivo: ****`/etc/systemd/system/kardocore.service`**

```
[Unit]
Description=KardoCore Application
After=network.target postgresql.service

[Service]
Type=notify
User=kardocore
Group=kardocore
WorkingDirectory=/home/kardocore/kardocore
Environment="PATH=/home/kardocore/kardocore/venv/bin"
ExecStart=/home/kardocore/kardocore/venv/bin/gunicorn kardocore.main:app \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --access-logfile /var/log/kardocore/access.log \
    --error-logfile /var/log/kardocore/error.log

[Install]
WantedBy=multi-user.target
```

```bash
# 11. Crear directorio de logs
sudo mkdir -p /var/log/kardocore
sudo chown kardocore:kardocore /var/log/kardocore

# 12. Habilitar y iniciar servicio
sudo systemctl daemon-reload
sudo systemctl enable kardocore
sudo systemctl start kardocore
sudo systemctl status kardocore

# 13. Configurar Nginx
sudo nano /etc/nginx/sites-available/kardocore
```

**Archivo: ****`/etc/nginx/sites-available/kardocore`**

```
server {
    listen 80;
    server_name tudominio.com www.tudominio.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/kardocore/kardocore/themes/frontend/static/;
        expires 30d;
    }

    location /media/ {
        alias /home/kardocore/kardocore/media/;
        expires 30d;
    }
}
```

```bash
# 14. Habilitar sitio
sudo ln -s /etc/nginx/sites-available/kardocore /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# 15. Configurar SSL con Let's Encrypt
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d tudominio.com -d www.tudominio.com
```

---

#### Opción 2: Docker

**Archivo: ****`Dockerfile`**

```
FROM python:3.14-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear usuario no-root
RUN useradd -m -u 1000 kardocore && chown -R kardocore:kardocore /app
USER kardocore

EXPOSE 8000

CMD ["uvicorn", "kardocore.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Archivo: ****`docker-compose.yml`**

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: kardocore
      POSTGRES_USER: kardocore
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine

  app:
    build: .
    ports:
      - "8000:8000"
    environment:
      KARDO_DATABASE_URL: postgresql://kardocore:password@db/kardocore
      KARDO_SECRET_KEY: ${KARDO_SECRET_KEY}
      KARDO_DEBUG: false
    depends_on:
      - db
      - redis
    volumes:
      - ./themes:/app/themes
      - ./uploads:/app/uploads
      - ./media:/app/media

volumes:
  postgres_data:
```

```bash
# Ejecutar
docker-compose up -d

# Ver logs
docker-compose logs -f app

# Crear admin
docker-compose exec app krd create-admin
```

---

## Verificación de la Instalación

### 1. Verificar Servidor

```bash
# Verificar que el servidor está corriendo
curl http://localhost:8000/api/health

# Respuesta esperada:
# {"status": "healthy", "version": "0.1.0-alpha"}
```

### 2. Verificar Base de Datos

```bash
# Listar tablas
krd db tables

# Verificar conexión
krd db check
```

### 3. Verificar Temas

```bash
# Listar temas instalados
krd themes list

# Verificar tema activo
krd themes active
```

### 4. Acceder al Panel de Administración

1. Abrir navegador: `http://localhost:8000/admin/`

1. Iniciar sesión con credenciales de administrador

1. Verificar dashboard

### 5. Crear Contenido de Prueba

```bash
# Crear página de prueba
krd content create --type page --title "Mi Primera Página"

# Crear post de prueba
krd content create --type post --title "Mi Primer Post"
```

---

## Solución de Problemas

### Error: "Module not found: kardocore"

```bash
# Verificar instalación
pip list | grep kardocore

# Reinstalar
pip install -e .
```

### Error: "Database connection failed"

```bash
# Verificar configuración
echo $KARDO_DATABASE_URL

# Verificar que PostgreSQL está corriendo
sudo systemctl status postgresql

# Probar conexión
psql -h localhost -U kardocore -d kardocore_prod
```

### Error: "Permission denied" en archivos estáticos

```bash
# Corregir permisos
sudo chown -R kardocore:kardocore /home/kardocore/kardocore
chmod -R 755 themes/*/static
```

### Error: "Port 8000 already in use"

```bash
# Encontrar proceso
sudo lsof -i :8000

# Matar proceso
sudo kill -9 <PID>

# O usar otro puerto
uvicorn kardocore.main:app --port 8001
```

### Logs no se generan

```bash
# Verificar configuración de logging
cat .env | grep LOG

# Crear directorio de logs
mkdir -p /var/log/kardocore
sudo chown kardocore:kardocore /var/log/kardocore

# Ver logs en tiempo real
tail -f /var/log/kardocore/kardocore.log
```

---

## Comandos Útiles

```bash
# CLI de KardoCore
krd --help                    # Ayuda general
krd db init                   # Inicializar base de datos
krd db migrate                # Ejecutar migraciones
krd create-admin              # Crear administrador
krd themes list               # Listar temas
krd content create            # Crear contenido
krd plugins list              # Listar plugins
krd cache clear               # Limpiar caché
krd backup create             # Crear backup
krd backup restore <file>     # Restaurar backup
```

---

## Recursos Adicionales

- **Documentación**: [https://docs.kardocore.dev](https://docs.kardocore.dev) (próximamente)

- **GitHub**: [https://github.com/webcien/KardoCore](https://github.com/webcien/KardoCore)

- **Comunidad**: [https://community.kardocore.dev](https://community.kardocore.dev) (próximamente)

- **Issues**: [https://github.com/webcien/KardoCore/issues](https://github.com/webcien/KardoCore/issues)

---

**Última actualización**: Octubre 2025**Versión del documento**: 1.0

