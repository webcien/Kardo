"""
Motor de Plantillas KardoTheme

Interfaz principal para el sistema de plantillas de KardoCore.
"""

from pathlib import Path
from typing import Dict, Any, Optional
import hashlib

from kardocore.theme.tokenizer import KardoThemeTokenizer
from kardocore.theme.renderer import KardoThemeRenderer, RenderError


class TemplateNotFoundError(Exception):
    """Excepción lanzada cuando no se encuentra una plantilla."""
    pass


class KardoTheme:
    """
    Motor de plantillas KardoTheme.
    
    Proporciona una interfaz de alto nivel para cargar, compilar
    y renderizar plantillas con sintaxis KardoTheme.
    
    Características:
    - Sintaxis expresiva con prefijo #
    - Escape automático (anti-XSS)
    - Sandboxing de seguridad
    - Caché de plantillas compiladas
    - Contextos separados (frontend/admin)
    
    Ejemplo:
        theme = KardoTheme(template_dir="/themes/frontend/templates")
        html = theme.render("page.html", {"title": "Mi Página", "posts": posts})
    """
    
    def __init__(
        self,
        template_dir: str | Path,
        cache_enabled: bool = True,
        auto_escape: bool = True,
    ):
        """
        Inicializa el motor de plantillas.
        
        Args:
            template_dir: Directorio de plantillas
            cache_enabled: Si debe cachear plantillas compiladas
            auto_escape: Si debe escapar HTML automáticamente
        """
        self.template_dir = Path(template_dir)
        self.cache_enabled = cache_enabled
        self.auto_escape = auto_escape
        self._cache: Dict[str, Any] = {}
    
    def render(self, template_name: str, context: Dict[str, Any] = None) -> str:
        """
        Renderiza una plantilla.
        
        Args:
            template_name: Nombre del archivo de plantilla
            context: Contexto de variables para la plantilla
        
        Returns:
            HTML renderizado
        
        Raises:
            TemplateNotFoundError: Si la plantilla no existe
            RenderError: Si hay un error durante el renderizado
        """
        context = context or {}
        
        # Cargar plantilla
        template_path = self.template_dir / template_name
        
        if not template_path.exists():
            raise TemplateNotFoundError(f"Template not found: {template_name}")
        
        # Obtener tokens (desde caché o compilar)
        tokens = self._get_or_compile_template(template_path)
        
        # Renderizar
        renderer = KardoThemeRenderer(tokens, context)
        return renderer.render()
    
    def render_string(self, template_string: str, context: Dict[str, Any] = None) -> str:
        """
        Renderiza una plantilla desde un string.
        
        Args:
            template_string: Código de la plantilla
            context: Contexto de variables
        
        Returns:
            HTML renderizado
        """
        context = context or {}
        
        # Tokenizar
        tokenizer = KardoThemeTokenizer(template_string)
        tokens = tokenizer.tokenize()
        
        # Validar
        errors = tokenizer.validate()
        if errors:
            raise RenderError(f"Template validation failed: {', '.join(errors)}")
        
        # Renderizar
        renderer = KardoThemeRenderer(tokens, context)
        return renderer.render()
    
    def _get_or_compile_template(self, template_path: Path) -> list:
        """
        Obtiene tokens de plantilla desde caché o compila.
        
        Args:
            template_path: Path a la plantilla
        
        Returns:
            Lista de tokens
        """
        # Generar clave de caché
        cache_key = self._get_cache_key(template_path)
        
        # Verificar caché
        if self.cache_enabled and cache_key in self._cache:
            cached_mtime, cached_tokens = self._cache[cache_key]
            current_mtime = template_path.stat().st_mtime
            
            # Verificar si el archivo no ha cambiado
            if cached_mtime == current_mtime:
                return cached_tokens
        
        # Compilar plantilla
        tokens = self._compile_template(template_path)
        
        # Guardar en caché
        if self.cache_enabled:
            mtime = template_path.stat().st_mtime
            self._cache[cache_key] = (mtime, tokens)
        
        return tokens
    
    def _compile_template(self, template_path: Path) -> list:
        """
        Compila una plantilla a tokens.
        
        Args:
            template_path: Path a la plantilla
        
        Returns:
            Lista de tokens
        """
        # Leer plantilla
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Tokenizar
        tokenizer = KardoThemeTokenizer(template_content)
        tokens = tokenizer.tokenize()
        
        # Validar
        errors = tokenizer.validate()
        if errors:
            raise RenderError(
                f"Template compilation failed for {template_path.name}: "
                f"{', '.join(errors)}"
            )
        
        return tokens
    
    def _get_cache_key(self, template_path: Path) -> str:
        """
        Genera una clave de caché para una plantilla.
        
        Args:
            template_path: Path a la plantilla
        
        Returns:
            Clave de caché
        """
        return hashlib.md5(str(template_path).encode()).hexdigest()
    
    def clear_cache(self) -> None:
        """Limpia la caché de plantillas compiladas."""
        self._cache.clear()
    
    def precompile_all(self) -> int:
        """
        Precompila todas las plantillas en el directorio.
        
        Returns:
            Número de plantillas compiladas
        """
        count = 0
        
        for template_path in self.template_dir.rglob('*.html'):
            try:
                self._get_or_compile_template(template_path)
                count += 1
            except Exception as e:
                print(f"Warning: Failed to precompile {template_path.name}: {e}")
        
        return count


# Función de conveniencia
def render_template(
    template_path: str,
    context: Dict[str, Any] = None,
    template_dir: str = "."
) -> str:
    """
    Función de conveniencia para renderizar una plantilla.
    
    Args:
        template_path: Path a la plantilla
        context: Contexto de variables
        template_dir: Directorio de plantillas
    
    Returns:
        HTML renderizado
    """
    theme = KardoTheme(template_dir)
    return theme.render(template_path, context)

