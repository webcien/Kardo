# Publicación Rápida en PyPI

## Opción 1: Script Automatizado (Recomendado)

```bash
cd /home/ubuntu/Kardo
./publish_to_pypi.sh
```

El script te guiará paso a paso.

## Opción 2: Comando Manual

```bash
cd /home/ubuntu/Kardo

# Publicar con tu token
.venv/bin/twine upload dist/* -u __token__ -p YOUR_TOKEN
```

## Obtener Token de PyPI

1. Ve a https://pypi.org
2. Login → Account Settings → API tokens
3. Click "Add API token"
4. Scope: "Entire account" (primera vez) o "Project: kardocore"
5. Copia el token (empieza con `pypi-`)

## Verificar Publicación

```bash
pip install kardocore
python -c "import kardocore; print(kardocore.__version__)"
```

Debe mostrar: `0.2.0`

---

**Guía completa**: Ver `PYPI_PUBLICATION_GUIDE.md`
