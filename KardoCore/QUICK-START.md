# KardoCore - Inicio Rápido

**La forma más simple de crear proyectos con KardoCore**

---

## 🚀 Instalación en 3 Pasos

### 1. Instalar KardoCore

```bash
pip install kardocore
```

### 2. Crear tu Proyecto

```bash
kardo new miproyecto --mode <modo>
```

### 3. Ejecutar

```bash
cd miproyecto
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

¡Listo! Tu proyecto está corriendo en `http://localhost:8000`

---

## 📦 Modos Disponibles

### 1. **Core Only** (Headless API)

```bash
kardo new myapi --mode core
```

**Incluye:**
- ✅ Servidor ASGI asíncrono
- ✅ Sistema de rutas REST
- ✅ Sistema de eventos
- ✅ Configuración con .env
- ✅ Base de datos configurable

**Ideal para:**
- APIs headless
- Microservicios
- Backend para apps móviles
- Integraciones serverless

**Acceso:**
- API: `http://localhost:8000/api/`
- Docs: `http://localhost:8000/docs/`

---

### 2. **Core + Admin**

```bash
kardo new mycms --mode admin
```

**Incluye:**
- ✅ Todo lo de "Core Only"
- ✅ Panel de administración completo
- ✅ Motor de plantillas KardoTheme (contexto admin)
- ✅ Autenticación y roles
- ✅ Gestión de usuarios

**Ideal para:**
- CMS headless con panel de administración
- Sistemas internos
- Dashboards administrativos

**Acceso:**
- API: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`
- Docs: `http://localhost:8000/docs/`

---

### 3. **Full CMS** (Completo)

```bash
kardo new mysite --mode full
```

**Incluye:**
- ✅ Todo lo de "Core + Admin"
- ✅ Frontend público con KardoTheme
- ✅ Sistema de temas
- ✅ Integración con KardoCSS
- ✅ Sistema de plugins
- ✅ Módulo KardoAI
- ✅ Gestión de medios

**Ideal para:**
- Sitios web completos
- Blogs y portales
- CMS tradicional
- Proyectos comerciales

**Acceso:**
- Frontend: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`

---

### 4. **Frontend Only**

```bash
kardo new mytheme --mode frontend
```

**Incluye:**
- ✅ Motor de plantillas KardoTheme
- ✅ Integración con KardoCSS
- ✅ Compilador de plantillas
- ✅ Generador de sitios estáticos

**Ideal para:**
- Diseñadores frontend
- Sitios estáticos (SSG)
- Desarrollo de temas
- Prototipado rápido

**Uso:**
```bash
cd mytheme
python build.py  # Compila a HTML estático en /dist
```

---

## 🎯 Ejemplos Completos

### Ejemplo 1: API REST Simple

```bash
# 1. Crear proyecto
kardo new taskapi --mode core

# 2. Entrar al proyecto
cd taskapi

# 3. Configurar entorno
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Ejecutar
uvicorn main:app --reload
```

**Resultado:** API REST funcionando en `http://localhost:8000`

---

### Ejemplo 2: CMS con Panel de Administración

```bash
# 1. Crear proyecto
kardo new myblog --mode admin

# 2. Setup
cd myblog
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Crear usuario admin
python -c "from admin.auth import create_admin; create_admin()"

# 4. Ejecutar
uvicorn main:app --reload
```

**Resultado:** 
- API: `http://localhost:8000/api/`
- Admin: `http://localhost:8000/admin/`

---

### Ejemplo 3: Sitio Web Completo

```bash
# 1. Crear proyecto
kardo new mywebsite --mode full

# 2. Setup
cd mywebsite
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Instalar KardoCSS (opcional pero recomendado)
pip install kardocss
kardocss build -o themes/frontend/default/static/css/kardocss.min.css --minify

# 4. Crear admin
python -c "from admin.auth import create_admin; create_admin()"

# 5. Ejecutar
uvicorn main:app --reload
```

**Resultado:**
- Frontend: `http://localhost:8000/`
- Admin: `http://localhost:8000/admin/`
- API: `http://localhost:8000/api/`

---

### Ejemplo 4: Solo Frontend (Sitio Estático)

```bash
# 1. Crear proyecto
kardo new portfolio --mode frontend

# 2. Setup
cd portfolio
python3.14 -m venv venv
source venv/bin/activate
pip install kardocore kardocss

# 3. Compilar CSS
kardocss build -o themes/minimal/static/css/styles.css

# 4. Compilar HTML
python build.py

# 5. Ver resultado
cd dist
python -m http.server 8000
```

**Resultado:** Sitio estático en `http://localhost:8000`

---

## ⚙️ Configuración

Cada proyecto incluye un archivo `.env` con configuración por defecto:

```bash
# Editar configuración
nano .env
```

**Variables principales:**

```bash
# General
KARDO_DEBUG=true
KARDO_MODE=full

# Servidor
KARDO_HOST=127.0.0.1
KARDO_PORT=8000

# Seguridad
KARDO_SECRET_KEY=auto-generada

# Base de datos
KARDO_DATABASE_URL=sqlite:///miproyecto.db

# IA (opcional)
KARDO_AI_ENABLED=false
KARDO_AI_PROVIDER=openai
KARDO_AI_API_KEY=
```

---

## 🔧 Comandos Útiles

```bash
# Crear nuevo proyecto
kardo new <nombre> --mode <modo>

# Alias corto
krd new <nombre> -m <modo>

# Ver ayuda
kardo --help

# Ver versión
kardo --version
```

---

## 📚 Estructura de Proyecto

### Core Only
```
myapi/
├── core/
│   ├── app.py
│   ├── routes/
│   ├── models/
│   └── settings.py
├── main.py
├── .env
└── requirements.txt
```

### Core + Admin
```
mycms/
├── core/
├── admin/
│   ├── templates/
│   └── static/
├── main.py
└── .env
```

### Full CMS
```
mysite/
├── core/
├── admin/
├── themes/
│   └── frontend/
│       └── default/
│           ├── templates/
│           └── static/
├── plugins/
├── ai/
├── uploads/
├── media/
└── .env
```

### Frontend Only
```
mytheme/
├── themes/
│   └── minimal/
│       ├── templates/
│       └── static/
├── build.py
└── dist/
```

---

## 🚀 Despliegue en Producción

### Con Gunicorn + Uvicorn

```bash
# Instalar
pip install gunicorn

# Ejecutar
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Con Docker

```bash
# Crear Dockerfile (incluido en el proyecto)
docker build -t miproyecto .
docker run -p 8000:8000 miproyecto
```

### Con Systemd (Linux)

```bash
# Crear servicio
sudo nano /etc/systemd/system/miproyecto.service

# Habilitar
sudo systemctl enable miproyecto
sudo systemctl start miproyecto
```

---

## 🆘 Solución de Problemas

### Error: "kardo: command not found"

```bash
# Reinstalar KardoCore
pip install --upgrade kardocore

# O usar directamente
python -m kardocore.cli.installer new miproyecto --mode core
```

### Error: "Port 8000 already in use"

```bash
# Usar otro puerto
uvicorn main:app --port 8001
```

### Error: "Module not found"

```bash
# Verificar que el entorno virtual está activado
source venv/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

---

## 📖 Recursos

- **Documentación completa**: [HOW-TO-INSTALL.md](HOW-TO-INSTALL.md)
- **GitHub**: https://github.com/webcien/KardoCore
- **Documentación online**: https://docs.kardocore.dev (próximamente)
- **Comunidad**: https://community.kardocore.dev (próximamente)

---

## 🎉 ¡Listo!

Ya puedes crear proyectos KardoCore con un solo comando. 

**¿Dudas?** Revisa la [documentación completa](HOW-TO-INSTALL.md) o abre un issue en GitHub.

---

**KardoCore v0.1.0-alpha** | MIT License | 2025

