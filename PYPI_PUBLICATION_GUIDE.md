# Guía de Publicación en PyPI - KardoCore v0.2.0

**Fecha**: 25 de octubre de 2025  
**Versión**: 0.2.0  
**Paquete**: kardocore

---

## 📋 Resumen

Esta guía te ayudará a publicar KardoCore v0.2.0 en PyPI (Python Package Index) de forma segura y profesional.

---

## ✅ Estado Actual

### Archivos Generados

Las distribuciones ya están listas en el directorio `dist/`:

```
dist/
├── kardocore-0.2.0-py3-none-any.whl  (56 KB)  ← Wheel distribution
└── kardocore-0.2.0.tar.gz            (84 KB)  ← Source distribution
```

✅ **Verificación**: Ambos archivos pasaron `twine check`

---

## 🔐 Paso 1: Obtener API Token de PyPI

### 1.1. Acceder a tu cuenta de PyPI

1. Ve a https://pypi.org
2. Inicia sesión con tu cuenta

### 1.2. Crear API Token

1. Ve a **Account Settings** → **API tokens**
2. Click en **"Add API token"**
3. Configura el token:
   - **Token name**: `kardocore-upload` (o el nombre que prefieras)
   - **Scope**: 
     - Si es tu **primera publicación**: Selecciona **"Entire account"**
     - Si ya existe el paquete: Selecciona **"Project: kardocore"**
4. Click en **"Add token"**
5. **IMPORTANTE**: Copia el token inmediatamente (comienza con `pypi-...`)
   - Solo se muestra una vez
   - Guárdalo en un lugar seguro

### 1.3. Ejemplo de Token

```
pypi-AgEIcHlwaS5vcmcCJGFiY2RlZi0xMjM0LTU2NzgtOTBhYi1jZGVmZ2hpamtsbW4...
```

---

## 📦 Paso 2: Publicar en PyPI

### Opción A: Publicación Directa (Recomendada)

#### 2.1. Configurar Credenciales

Ejecuta este comando en tu terminal (reemplaza `YOUR_TOKEN` con tu token real):

```bash
cd /home/ubuntu/Kardo

# Publicar usando el token directamente
.venv/bin/twine upload dist/* -u __token__ -p YOUR_TOKEN
```

**Ejemplo completo**:
```bash
.venv/bin/twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGFiY2RlZi0xMjM0LTU2NzgtOTBhYi1jZGVmZ2hpamtsbW4...
```

#### 2.2. Salida Esperada

```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading kardocore-0.2.0-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 56.0/56.0 kB • 00:01 • 45.2 kB/s
Uploading kardocore-0.2.0.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 84.0/84.0 kB • 00:01 • 67.3 kB/s

View at:
https://pypi.org/project/kardocore/0.2.0/
```

---

### Opción B: Usando Archivo de Configuración

#### 2.1. Crear archivo `.pypirc`

```bash
nano ~/.pypirc
```

Contenido:
```ini
[pypi]
username = __token__
password = YOUR_TOKEN_HERE
```

**Reemplaza `YOUR_TOKEN_HERE`** con tu token real.

#### 2.2. Proteger el archivo

```bash
chmod 600 ~/.pypirc
```

#### 2.3. Publicar

```bash
cd /home/ubuntu/Kardo
.venv/bin/twine upload dist/*
```

---

## 🧪 Paso 3: Probar en TestPyPI (Opcional pero Recomendado)

Antes de publicar en PyPI real, puedes probar en TestPyPI.

### 3.1. Crear cuenta en TestPyPI

1. Ve a https://test.pypi.org
2. Crea una cuenta (diferente de PyPI)
3. Crea un API token igual que en PyPI

### 3.2. Publicar en TestPyPI

```bash
cd /home/ubuntu/Kardo
.venv/bin/twine upload --repository testpypi dist/* -u __token__ -p YOUR_TESTPYPI_TOKEN
```

### 3.3. Probar instalación desde TestPyPI

```bash
pip install --index-url https://test.pypi.org/simple/ kardocore
```

Si funciona correctamente, procede a publicar en PyPI real.

---

## ✅ Paso 4: Verificar Publicación

### 4.1. Verificar en PyPI

1. Ve a https://pypi.org/project/kardocore/
2. Verifica que aparezca la versión 0.2.0
3. Revisa la descripción y metadatos

### 4.2. Probar Instalación

```bash
# Crear entorno virtual limpio
python3.11 -m venv test_env
source test_env/bin/activate

# Instalar desde PyPI
pip install kardocore

# Verificar versión
python -c "import kardocore; print(kardocore.__version__)"

# Probar CLI
kardo --version
```

**Salida esperada**:
```
0.2.0
KardoCore v0.2.0
```

---

## 🔄 Paso 5: Actualizar Documentación

### 5.1. Actualizar README.md

Agrega badge de PyPI:

```markdown
[![PyPI version](https://badge.fury.io/py/kardocore.svg)](https://badge.fury.io/py/kardocore)
[![Python Versions](https://img.shields.io/pypi/pyversions/kardocore.svg)](https://pypi.org/project/kardocore/)
[![Downloads](https://pepy.tech/badge/kardocore)](https://pepy.tech/project/kardocore)
```

### 5.2. Crear Release en GitHub

```bash
cd /home/ubuntu/Kardo

# Crear tag
git tag -a v0.2.0 -m "Release v0.2.0 - Full CMS with Admin Panel"

# Push tag
git push origin v0.2.0
```

Luego en GitHub:
1. Ve a **Releases** → **Create a new release**
2. Selecciona tag `v0.2.0`
3. Título: `KardoCore v0.2.0`
4. Descripción: Copia el changelog
5. Adjunta los archivos de `dist/`
6. Publica el release

---

## 📝 Comandos Completos de Publicación

### Resumen de Comandos

```bash
# 1. Navegar al proyecto
cd /home/ubuntu/Kardo

# 2. Limpiar builds anteriores (si es necesario)
rm -rf dist/ build/ *.egg-info

# 3. Generar distribuciones
.venv/bin/python -m build

# 4. Verificar distribuciones
.venv/bin/twine check dist/*

# 5. Publicar en PyPI
.venv/bin/twine upload dist/* -u __token__ -p YOUR_TOKEN

# 6. Crear tag en Git
git tag -a v0.2.0 -m "Release v0.2.0"
git push origin v0.2.0
```

---

## ⚠️ Solución de Problemas

### Error: "File already exists"

Si ya publicaste esta versión antes:

```bash
# Incrementar versión en pyproject.toml
# version = "0.2.1"

# Regenerar distribuciones
rm -rf dist/
.venv/bin/python -m build

# Publicar nueva versión
.venv/bin/twine upload dist/* -u __token__ -p YOUR_TOKEN
```

### Error: "Invalid or non-existent authentication"

- Verifica que el token sea correcto
- Asegúrate de usar `-u __token__` (con doble guion bajo)
- Verifica que el token no haya expirado

### Error: "403 Forbidden"

- Verifica que el token tenga permisos correctos
- Si es primera publicación, usa token de "Entire account"
- Si el paquete existe, usa token específico del proyecto

---

## 🎯 Checklist de Publicación

Antes de publicar, verifica:

- [ ] `pyproject.toml` tiene la versión correcta (0.2.0)
- [ ] `README.md` está actualizado
- [ ] `LICENSE` está presente
- [ ] Distribuciones generadas (`dist/` contiene .whl y .tar.gz)
- [ ] `twine check dist/*` pasa sin errores
- [ ] Token de PyPI obtenido
- [ ] (Opcional) Probado en TestPyPI
- [ ] Commit y push de todos los cambios
- [ ] Tag de versión creado

---

## 📊 Información de las Distribuciones

### kardocore-0.2.0-py3-none-any.whl (56 KB)

**Wheel distribution** - Instalación rápida sin compilación

**Contenido**:
- Módulos Python compilados
- Metadatos del paquete
- Entry points (comando `kardo`)

### kardocore-0.2.0.tar.gz (84 KB)

**Source distribution** - Código fuente completo

**Contenido**:
- Código fuente Python
- README.md
- LICENSE
- pyproject.toml
- MANIFEST.in

---

## 🚀 Después de Publicar

### 1. Anunciar el Release

- **Twitter/X**: Anuncia la publicación
- **Reddit**: r/Python, r/webdev
- **Discord**: Comunidad de Python
- **LinkedIn**: Post profesional

### 2. Actualizar Documentación

- Actualizar sitio web (si existe)
- Actualizar ejemplos con nueva versión
- Crear tutorial de instalación

### 3. Monitorear

- **PyPI Stats**: https://pypistats.org/packages/kardocore
- **GitHub Stars**: Monitorear crecimiento
- **Issues**: Responder a problemas reportados

---

## 📞 Soporte

Si encuentras problemas durante la publicación:

1. **PyPI Help**: https://pypi.org/help/
2. **Twine Docs**: https://twine.readthedocs.io/
3. **GitHub Issues**: https://github.com/webcien/Kardo/issues

---

## 🎉 ¡Felicidades!

Una vez publicado, KardoCore v0.2.0 estará disponible para instalación en todo el mundo:

```bash
pip install kardocore
```

**URL del paquete**: https://pypi.org/project/kardocore/

---

**Preparado por**: Manus AI  
**Fecha**: 25 de octubre de 2025  
**Versión**: KardoCore v0.2.0

