"""
Ejemplo de aplicación simple con KardoCore

Este ejemplo demuestra las características básicas del framework:
- Definición de rutas
- Manejo de peticiones
- Validación de datos
- Sistema de eventos
- Configuración
"""

from kardocore import KardoApp, JSONResponse, HTMLResponse, KardoModel, String, Integer, Email, event, Events


# Definir un modelo de datos
class User(KardoModel):
    """Modelo de usuario con validación automática."""
    id: int = Integer(required=False)
    name: str = String(min_length=2, max_length=100)
    email: str = Email(required=True)
    age: int = Integer(min_value=18, max_value=120, required=False)


# Crear la aplicación
app = KardoApp(title="KardoCore Simple App", version="1.0.0")


# Base de datos simulada
users_db = []


# Eventos del ciclo de vida
@app.on_event(Events.ON_STARTUP)
async def startup():
    """Ejecutado al iniciar la aplicación."""
    print("🚀 KardoCore iniciado")
    print("📝 Servidor escuchando en http://127.0.0.1:8000")
    print("📚 Documentación: http://127.0.0.1:8000/docs")


@app.on_event(Events.ON_SHUTDOWN)
async def shutdown():
    """Ejecutado al cerrar la aplicación."""
    print("👋 KardoCore detenido")


# Rutas
@app.get("/")
async def index(request):
    """Página de inicio."""
    return HTMLResponse("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>KardoCore Simple App</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                }
                h1 { color: #2c3e50; }
                .endpoint {
                    background: #f8f9fa;
                    padding: 15px;
                    margin: 10px 0;
                    border-left: 4px solid #3498db;
                }
                code {
                    background: #e9ecef;
                    padding: 2px 6px;
                    border-radius: 3px;
                }
            </style>
        </head>
        <body>
            <h1>🎉 ¡Bienvenido a KardoCore!</h1>
            <p>Framework Python Híbrido, Modular e IA-Ready</p>
            
            <h2>Endpoints Disponibles:</h2>
            
            <div class="endpoint">
                <strong>GET /</strong><br>
                Esta página de inicio
            </div>
            
            <div class="endpoint">
                <strong>GET /api/users</strong><br>
                Listar todos los usuarios
            </div>
            
            <div class="endpoint">
                <strong>POST /api/users</strong><br>
                Crear un nuevo usuario<br>
                Body: <code>{"name": "Juan", "email": "juan@example.com", "age": 30}</code>
            </div>
            
            <div class="endpoint">
                <strong>GET /api/health</strong><br>
                Estado del servidor
            </div>
            
            <h2>Características:</h2>
            <ul>
                <li>✅ Servidor ASGI asíncrono</li>
                <li>✅ Validación automática de datos</li>
                <li>✅ Sistema de eventos</li>
                <li>✅ Respuestas JSON y HTML</li>
                <li>✅ Python 3.14+</li>
            </ul>
        </body>
        </html>
    """)


@app.get("/api/health")
async def health(request):
    """Endpoint de salud del servidor."""
    return {
        "status": "healthy",
        "framework": "KardoCore",
        "version": app.version,
        "users_count": len(users_db)
    }


@app.get("/api/users")
async def list_users(request):
    """Lista todos los usuarios."""
    return {
        "users": [user.dict() for user in users_db],
        "total": len(users_db)
    }


@app.post("/api/users")
async def create_user(request):
    """Crea un nuevo usuario con validación automática."""
    try:
        # Obtener datos del body
        data = await request.json()
        
        # Crear y validar usuario
        user = User(**data)
        
        # Asignar ID
        user.id = len(users_db) + 1
        
        # Guardar en "base de datos"
        users_db.append(user)
        
        # Emitir evento
        await app.event_manager.emit(Events.ON_USER_CREATED, user)
        
        return JSONResponse(
            {
                "message": "Usuario creado exitosamente",
                "user": user.dict()
            },
            status_code=201
        )
    
    except Exception as e:
        return JSONResponse(
            {
                "error": "Error al crear usuario",
                "detail": str(e)
            },
            status_code=400
        )


# Event listener para nuevos usuarios
@event(Events.ON_USER_CREATED)
async def on_user_created(user):
    """Ejecutado cuando se crea un nuevo usuario."""
    print(f"✨ Nuevo usuario creado: {user.name} ({user.email})")
    # Aquí podrías:
    # - Enviar email de bienvenida
    # - Generar contenido con IA
    # - Registrar en analytics
    # - etc.


# Punto de entrada
if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("  KardoCore - Framework Python Híbrido e IA-Ready")
    print("="*60 + "\n")
    
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info"
    )

