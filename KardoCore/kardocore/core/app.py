"""
Núcleo ASGI de KardoCore

Implementación del servidor ASGI base del framework, inspirado en FastAPI
pero desarrollado desde cero. Compatible con Uvicorn, Hypercorn y Daphne.

Aprovecha características de Python 3.14:
- Múltiples intérpretes (PEP 734)
- Evaluación diferida de anotaciones (PEP 649/749)
- Template strings (PEP 750) para sanitización
"""

import asyncio
from typing import Any, Callable, Dict, List, Optional
from datetime import datetime
import inspect

from kardocore.core.events import EventManager, Events
from kardocore.core.models.base import KardoModel


class Request:
    """
    Representa una petición HTTP entrante.
    
    Encapsula el scope ASGI y proporciona una interfaz conveniente
    para acceder a headers, query params, body, etc.
    """
    
    def __init__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        self.scope = scope
        self.receive = receive
        self.send = send
        self._body: Optional[bytes] = None
        self._json: Optional[Dict[str, Any]] = None
    
    @property
    def method(self) -> str:
        """Método HTTP de la petición."""
        return self.scope.get("method", "GET")
    
    @property
    def path(self) -> str:
        """Path de la petición."""
        return self.scope.get("path", "/")
    
    @property
    def query_string(self) -> str:
        """Query string de la petición."""
        return self.scope.get("query_string", b"").decode("utf-8")
    
    @property
    def headers(self) -> Dict[str, str]:
        """Headers de la petición."""
        return {
            k.decode("utf-8"): v.decode("utf-8")
            for k, v in self.scope.get("headers", [])
        }
    
    async def body(self) -> bytes:
        """Lee el body de la petición."""
        if self._body is None:
            body_parts = []
            while True:
                message = await self.receive()
                if message["type"] == "http.request":
                    body_parts.append(message.get("body", b""))
                    if not message.get("more_body", False):
                        break
            self._body = b"".join(body_parts)
        return self._body
    
    async def json(self) -> Dict[str, Any]:
        """Parsea el body como JSON."""
        if self._json is None:
            import json
            body = await self.body()
            self._json = json.loads(body.decode("utf-8"))
        return self._json
    
    async def form(self) -> Dict[str, Any]:
        """Parsea el body como form data."""
        from urllib.parse import parse_qs
        body = await self.body()
        return parse_qs(body.decode("utf-8"))


class Response:
    """
    Representa una respuesta HTTP.
    
    Soporta diferentes tipos de contenido: JSON, HTML, texto plano, etc.
    """
    
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: str = "text/plain",
    ):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {}
        self.media_type = media_type
    
    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        """Envía la respuesta al cliente."""
        # Preparar body
        if isinstance(self.content, (dict, list)):
            import json
            body = json.dumps(self.content).encode("utf-8")
            self.media_type = "application/json"
        elif isinstance(self.content, str):
            body = self.content.encode("utf-8")
        elif isinstance(self.content, bytes):
            body = self.content
        elif isinstance(self.content, KardoModel):
            body = self.content.json().encode("utf-8")
            self.media_type = "application/json"
        else:
            body = str(self.content).encode("utf-8")
        
        # Preparar headers
        headers = [
            (b"content-type", self.media_type.encode("utf-8")),
            (b"content-length", str(len(body)).encode("utf-8")),
        ]
        
        for key, value in self.headers.items():
            headers.append((key.encode("utf-8"), value.encode("utf-8")))
        
        # Enviar respuesta
        await send({
            "type": "http.response.start",
            "status": self.status_code,
            "headers": headers,
        })
        
        await send({
            "type": "http.response.body",
            "body": body,
        })


class JSONResponse(Response):
    """Respuesta JSON."""
    
    def __init__(self, content: Any, status_code: int = 200, **kwargs):
        super().__init__(content, status_code, media_type="application/json", **kwargs)


class HTMLResponse(Response):
    """Respuesta HTML."""
    
    def __init__(self, content: str, status_code: int = 200, **kwargs):
        super().__init__(content, status_code, media_type="text/html; charset=utf-8", **kwargs)


class Route:
    """
    Representa una ruta en el framework.
    
    Asocia un path y método HTTP con un handler.
    """
    
    def __init__(
        self,
        path: str,
        handler: Callable,
        methods: List[str] = None,
        name: Optional[str] = None,
    ):
        self.path = path
        self.handler = handler
        self.methods = methods or ["GET"]
        self.name = name or handler.__name__
    
    def matches(self, path: str, method: str) -> bool:
        """Verifica si la ruta coincide con el path y método."""
        # TODO: Implementar matching con parámetros de ruta (/users/{id})
        return self.path == path and method in self.methods
    
    async def handle(self, request: Request) -> Response:
        """Ejecuta el handler de la ruta."""
        # Inyección de dependencias simple
        if inspect.iscoroutinefunction(self.handler):
            result = await self.handler(request)
        else:
            result = self.handler(request)
        
        # Convertir resultado a Response si es necesario
        if isinstance(result, Response):
            return result
        elif isinstance(result, (dict, list)):
            return JSONResponse(result)
        elif isinstance(result, str):
            return HTMLResponse(result)
        else:
            return Response(result)


class KardoApp:
    """
    Aplicación principal de KardoCore.
    
    Implementa el protocolo ASGI y gestiona rutas, middleware,
    eventos y configuración del framework.
    
    Ejemplo:
        app = KardoApp()
        
        @app.route("/")
        async def index(request):
            return {"message": "Hello, KardoCore!"}
        
        @app.on_event("on_startup")
        async def startup():
            print("KardoCore iniciado")
    """
    
    def __init__(self, title: str = "KardoCore App", version: str = "0.1.0"):
        self.title = title
        self.version = version
        self.routes: List[Route] = []
        self.event_manager = EventManager()
        self.middleware: List[Callable] = []
        self._startup_complete = False
    
    def route(
        self,
        path: str,
        methods: List[str] = None,
        name: Optional[str] = None,
    ):
        """
        Decorador para registrar una ruta.
        
        Uso:
            @app.route("/users", methods=["GET", "POST"])
            async def users(request):
                return {"users": []}
        """
        def decorator(func: Callable) -> Callable:
            route = Route(path, func, methods, name)
            self.routes.append(route)
            return func
        return decorator
    
    def get(self, path: str, **kwargs):
        """Decorador para rutas GET."""
        return self.route(path, methods=["GET"], **kwargs)
    
    def post(self, path: str, **kwargs):
        """Decorador para rutas POST."""
        return self.route(path, methods=["POST"], **kwargs)
    
    def put(self, path: str, **kwargs):
        """Decorador para rutas PUT."""
        return self.route(path, methods=["PUT"], **kwargs)
    
    def delete(self, path: str, **kwargs):
        """Decorador para rutas DELETE."""
        return self.route(path, methods=["DELETE"], **kwargs)
    
    def on_event(self, event_name: str):
        """
        Decorador para registrar un handler de evento.
        
        Uso:
            @app.on_event("on_startup")
            async def startup():
                print("Iniciando...")
        """
        def decorator(func: Callable) -> Callable:
            self.event_manager.on(event_name, func)
            return func
        return decorator
    
    def add_middleware(self, middleware: Callable):
        """Agrega un middleware a la aplicación."""
        self.middleware.append(middleware)
    
    async def _startup(self):
        """Ejecuta eventos de startup."""
        if not self._startup_complete:
            await self.event_manager.emit(Events.ON_STARTUP)
            self._startup_complete = True
    
    async def _shutdown(self):
        """Ejecuta eventos de shutdown."""
        await self.event_manager.emit(Events.ON_SHUTDOWN)
    
    async def _find_route(self, path: str, method: str) -> Optional[Route]:
        """Encuentra una ruta que coincida con el path y método."""
        for route in self.routes:
            if route.matches(path, method):
                return route
        return None
    
    async def _handle_request(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        """Maneja una petición HTTP."""
        request = Request(scope, receive, send)
        
        # Buscar ruta
        route = await self._find_route(request.path, request.method)
        
        if route is None:
            # Ruta no encontrada
            response = JSONResponse(
                {"error": "Not Found", "path": request.path},
                status_code=404
            )
        else:
            try:
                # Ejecutar handler
                response = await route.handle(request)
            except Exception as e:
                # Error en handler
                response = JSONResponse(
                    {"error": "Internal Server Error", "detail": str(e)},
                    status_code=500
                )
        
        # Enviar respuesta
        await response(scope, receive, send)
    
    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable):
        """
        Punto de entrada ASGI.
        
        Este método es llamado por el servidor ASGI (Uvicorn, Hypercorn, etc.)
        para cada petición.
        """
        if scope["type"] == "lifespan":
            # Manejo de eventos de ciclo de vida
            while True:
                message = await receive()
                if message["type"] == "lifespan.startup":
                    await self._startup()
                    await send({"type": "lifespan.startup.complete"})
                elif message["type"] == "lifespan.shutdown":
                    await self._shutdown()
                    await send({"type": "lifespan.shutdown.complete"})
                    return
        
        elif scope["type"] == "http":
            # Manejo de peticiones HTTP
            await self._handle_request(scope, receive, send)
        
        else:
            raise NotImplementedError(f"Scope type {scope['type']} not supported")

