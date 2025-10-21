"""
KardoCore - Package Manager
Gestor principal de paquetes, temas y plugins
"""

import os
import yaml
import shutil
from typing import Dict, List, Optional, Any
from pathlib import Path


class PackageManager:
    """
    Gestor de paquetes para KardoCore.
    
    Maneja la instalación, actualización y eliminación de:
    - Temas (frontend y backend)
    - Plugins
    - Extensiones
    """
    
    def __init__(self, project_root: str):
        """
        Inicializa el gestor de paquetes.
        
        Args:
            project_root: Ruta raíz del proyecto KardoCore
        """
        self.project_root = Path(project_root)
        self.themes_dir = self.project_root / "themes"
        self.plugins_dir = self.project_root / "plugins"
        self.cache_dir = self.project_root / ".kardo" / "cache"
        
        # Crear directorios si no existen
        self._ensure_directories()
        
        # Registry de paquetes
        self.registry_url = "https://raw.githubusercontent.com/webcien/KardoTemplates/main/registry.yaml"
    
    def _ensure_directories(self) -> None:
        """Asegura que existan los directorios necesarios."""
        dirs = [
            self.themes_dir / "frontend",
            self.themes_dir / "backend",
            self.plugins_dir,
            self.cache_dir,
        ]
        
        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
    
    def install_theme(self, slug: str, theme_type: str = "frontend", source: str = "registry") -> bool:
        """
        Instala un tema desde el registry o desde una fuente personalizada.
        
        Args:
            slug: Slug del tema (ej. 'wellness-clinic')
            theme_type: Tipo de tema ('frontend' o 'backend')
            source: Fuente del tema ('registry', 'github', 'local')
        
        Returns:
            True si la instalación fue exitosa
        """
        print(f"📦 Instalando tema: {slug} ({theme_type})...")
        
        try:
            if source == "registry":
                return self._install_from_registry(slug, theme_type)
            elif source == "github":
                return self._install_from_github(slug, theme_type)
            elif source == "local":
                return self._install_from_local(slug, theme_type)
            else:
                print(f"❌ Fuente desconocida: {source}")
                return False
        
        except Exception as e:
            print(f"❌ Error al instalar tema: {e}")
            return False
    
    def _install_from_registry(self, slug: str, theme_type: str) -> bool:
        """Instala un tema desde el registry oficial."""
        import requests
        
        # Descargar registry
        try:
            response = requests.get(self.registry_url)
            response.raise_for_status()
            registry = yaml.safe_load(response.text)
        except Exception as e:
            print(f"❌ Error al descargar registry: {e}")
            return False
        
        # Buscar tema en registry
        theme_info = None
        for theme in registry.get("themes", []):
            if theme["slug"] == slug and theme["type"] == theme_type:
                theme_info = theme
                break
        
        if not theme_info:
            print(f"❌ Tema no encontrado en registry: {slug}")
            return False
        
        # Descargar tema desde GitHub
        github_url = theme_info.get("download_url")
        if not github_url:
            print(f"❌ URL de descarga no disponible para: {slug}")
            return False
        
        return self._download_and_install(github_url, slug, theme_type)
    
    def _download_and_install(self, url: str, slug: str, theme_type: str) -> bool:
        """Descarga e instala un tema desde una URL."""
        import requests
        import zipfile
        import tempfile
        
        try:
            # Descargar archivo
            print(f"⬇️  Descargando desde: {url}")
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Guardar en archivo temporal
            with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    tmp_file.write(chunk)
                tmp_path = tmp_file.name
            
            # Extraer archivo
            extract_dir = self.cache_dir / slug
            extract_dir.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Mover a directorio de temas
            target_dir = self.themes_dir / theme_type / slug
            
            # Buscar directorio del tema dentro del archivo extraído
            theme_dir = self._find_theme_directory(extract_dir)
            
            if theme_dir:
                if target_dir.exists():
                    shutil.rmtree(target_dir)
                shutil.copytree(theme_dir, target_dir)
                print(f"✅ Tema instalado en: {target_dir}")
                return True
            else:
                print(f"❌ No se encontró el directorio del tema en el archivo descargado")
                return False
        
        except Exception as e:
            print(f"❌ Error al descargar e instalar: {e}")
            return False
        
        finally:
            # Limpiar archivos temporales
            if 'tmp_path' in locals():
                os.unlink(tmp_path)
    
    def _find_theme_directory(self, extract_dir: Path) -> Optional[Path]:
        """Encuentra el directorio del tema dentro del archivo extraído."""
        # Buscar theme.yaml en subdirectorios
        for root, dirs, files in os.walk(extract_dir):
            if "theme.yaml" in files:
                return Path(root)
        
        return None
    
    def _install_from_github(self, slug: str, theme_type: str, repo: str = "webcien/KardoTemplates") -> bool:
        """Instala un tema directamente desde GitHub."""
        # Construir URL de descarga
        url = f"https://github.com/{repo}/archive/refs/heads/main.zip"
        return self._download_and_install(url, slug, theme_type)
    
    def _install_from_local(self, slug: str, theme_type: str, local_path: str = None) -> bool:
        """Instala un tema desde un directorio local."""
        if not local_path:
            print(f"❌ Debe especificar la ruta local del tema")
            return False
        
        source_dir = Path(local_path)
        if not source_dir.exists():
            print(f"❌ El directorio no existe: {local_path}")
            return False
        
        # Verificar que sea un tema válido
        theme_yaml = source_dir / "theme.yaml"
        if not theme_yaml.exists():
            print(f"❌ No se encontró theme.yaml en: {local_path}")
            return False
        
        # Copiar al directorio de temas
        target_dir = self.themes_dir / theme_type / slug
        
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        shutil.copytree(source_dir, target_dir)
        print(f"✅ Tema instalado desde local: {target_dir}")
        return True
    
    def list_installed_themes(self, theme_type: str = None) -> List[Dict[str, Any]]:
        """
        Lista los temas instalados.
        
        Args:
            theme_type: Filtrar por tipo ('frontend', 'backend', o None para todos)
        
        Returns:
            Lista de diccionarios con información de los temas
        """
        themes = []
        
        search_dirs = []
        if theme_type:
            search_dirs.append(self.themes_dir / theme_type)
        else:
            search_dirs.extend([
                self.themes_dir / "frontend",
                self.themes_dir / "backend"
            ])
        
        for theme_dir in search_dirs:
            if not theme_dir.exists():
                continue
            
            for theme_path in theme_dir.iterdir():
                if not theme_path.is_dir():
                    continue
                
                theme_yaml = theme_path / "theme.yaml"
                if theme_yaml.exists():
                    with open(theme_yaml, 'r', encoding='utf-8') as f:
                        theme_info = yaml.safe_load(f)
                        theme_info['installed_path'] = str(theme_path)
                        themes.append(theme_info)
        
        return themes
    
    def uninstall_theme(self, slug: str, theme_type: str = "frontend") -> bool:
        """
        Desinstala un tema.
        
        Args:
            slug: Slug del tema
            theme_type: Tipo de tema ('frontend' o 'backend')
        
        Returns:
            True si la desinstalación fue exitosa
        """
        theme_dir = self.themes_dir / theme_type / slug
        
        if not theme_dir.exists():
            print(f"❌ El tema no está instalado: {slug}")
            return False
        
        try:
            shutil.rmtree(theme_dir)
            print(f"✅ Tema desinstalado: {slug}")
            return True
        except Exception as e:
            print(f"❌ Error al desinstalar tema: {e}")
            return False
    
    def get_theme_info(self, slug: str, theme_type: str = "frontend") -> Optional[Dict[str, Any]]:
        """
        Obtiene información de un tema instalado.
        
        Args:
            slug: Slug del tema
            theme_type: Tipo de tema
        
        Returns:
            Diccionario con información del tema o None si no está instalado
        """
        theme_dir = self.themes_dir / theme_type / slug
        theme_yaml = theme_dir / "theme.yaml"
        
        if not theme_yaml.exists():
            return None
        
        with open(theme_yaml, 'r', encoding='utf-8') as f:
            theme_info = yaml.safe_load(f)
            theme_info['installed_path'] = str(theme_dir)
            return theme_info
    
    def search_themes(self, query: str, theme_type: str = None) -> List[Dict[str, Any]]:
        """
        Busca temas en el registry.
        
        Args:
            query: Término de búsqueda
            theme_type: Filtrar por tipo
        
        Returns:
            Lista de temas que coinciden con la búsqueda
        """
        import requests
        
        try:
            response = requests.get(self.registry_url)
            response.raise_for_status()
            registry = yaml.safe_load(response.text)
        except Exception as e:
            print(f"❌ Error al buscar temas: {e}")
            return []
        
        results = []
        query_lower = query.lower()
        
        for theme in registry.get("themes", []):
            # Filtrar por tipo si se especificó
            if theme_type and theme.get("type") != theme_type:
                continue
            
            # Buscar en nombre, descripción y tags
            if (query_lower in theme.get("name", "").lower() or
                query_lower in theme.get("description", "").lower() or
                query_lower in " ".join(theme.get("tags", [])).lower()):
                results.append(theme)
        
        return results

