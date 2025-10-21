"""
Sistema de routing mejorado para KardoCore
"""
import re
from typing import Dict, Callable, Tuple, Optional


class Router:
    """Router simple pero robusto para manejar rutas con parámetros"""
    
    def __init__(self):
        self.routes: Dict[Tuple[str, str], Callable] = {}
        self.compiled_routes = []
    
    def add_route(self, method: str, path: str, handler: Callable):
        """Agregar una ruta"""
        self.routes[(method, path)] = handler
        
        # Compilar patrón regex para rutas con parámetros
        if "{" in path:
            # Convertir /admin/posts/edit/{post_id} a regex
            pattern = path
            param_names = []
            
            # Encontrar todos los parámetros
            for match in re.finditer(r'\{([^}]+)\}', path):
                param_name = match.group(1)
                param_names.append(param_name)
                # Reemplazar {param} con un grupo regex
                pattern = pattern.replace(f'{{{param_name}}}', r'([^/]+)')
            
            # Anclar el patrón
            pattern = f'^{pattern}$'
            
            self.compiled_routes.append({
                'method': method,
                'pattern': re.compile(pattern),
                'param_names': param_names,
                'handler': handler,
                'original_path': path
            })
    
    def match(self, method: str, path: str) -> Optional[Tuple[Callable, Dict[str, str]]]:
        """
        Encontrar handler para una ruta
        Returns: (handler, path_params) o None
        """
        # Intentar match exacto primero
        handler = self.routes.get((method, path))
        if handler:
            return (handler, {})
        
        # Intentar match con parámetros
        for route in self.compiled_routes:
            if route['method'] == method:
                match = route['pattern'].match(path)
                if match:
                    # Extraer parámetros
                    params = {}
                    for i, param_name in enumerate(route['param_names']):
                        params[param_name] = match.group(i + 1)
                    
                    return (route['handler'], params)
        
        return None

