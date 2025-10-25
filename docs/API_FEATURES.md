# API Features Documentation

Complete REST API generation, OpenAPI documentation, and CORS support for KardoCore.

## Features

- **REST API Generator** - Auto-generate CRUD endpoints from models
- **OpenAPI/Swagger** - Auto-generate API documentation
- **CORS Middleware** - Cross-origin resource sharing support

---

## REST API Generator

Auto-generate REST APIs from your models with zero boilerplate.

### Basic Usage

```python
from kardocore.api import RESTAPIGenerator
from kardocore.db import Database

# Initialize generator
api = RESTAPIGenerator(base_path="/api/v1")

# Register models
api.register_model(User, name="users")
api.register_model(Post, name="posts")

# Get generated routes
routes = api.get_routes()

# Add to your app
for path, method, handler in routes:
    app.add_route(path, handler, methods=[method])
```

### Generated Endpoints

For each model, the following endpoints are generated:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/{model}` | List all records |
| POST | `/api/{model}` | Create new record |
| GET | `/api/{model}/{id}` | Get record by ID |
| PUT | `/api/{model}/{id}` | Update record |
| DELETE | `/api/{model}/{id}` | Delete record |

### Exclude Operations

```python
# Only generate read operations
api.register_model(
    User,
    name="users",
    exclude=["create", "update", "delete"]
)
```

---

## OpenAPI/Swagger Documentation

Auto-generate OpenAPI 3.0 specification and Swagger UI.

### Generate Specification

```python
from kardocore.api import OpenAPIGenerator

# Get OpenAPI spec
spec = api.get_openapi_spec()

# Serve as JSON
@app.route("/api/openapi.json")
async def openapi_spec(request):
    return spec
```

### Swagger UI

```python
from kardocore.api import SwaggerUI

# Serve Swagger UI
@app.route("/api/docs")
async def api_docs(request):
    html = SwaggerUI.get_html("/api/openapi.json")
    return html
```

Visit `/api/docs` to see interactive API documentation.

---

## CORS Middleware

Handle Cross-Origin Resource Sharing for API requests.

### Basic Usage

```python
from kardocore.api import CORSMiddleware

# Allow all origins
cors = CORSMiddleware(allow_origins=["*"])

# Add to app
app.add_middleware(cors)
```

### Advanced Configuration

```python
cors = CORSMiddleware(
    allow_origins=[
        "https://example.com",
        "https://app.example.com"
    ],
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
    allow_credentials=True,
    max_age=3600  # 1 hour
)
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `allow_origins` | List of allowed origins | `["*"]` |
| `allow_methods` | List of allowed HTTP methods | `["GET", "POST", "PUT", "DELETE", "OPTIONS"]` |
| `allow_headers` | List of allowed headers | `["Content-Type", "Authorization"]` |
| `allow_credentials` | Allow credentials (cookies, auth) | `False` |
| `max_age` | Preflight cache time (seconds) | `600` |

---

## Complete Example

```python
from kardocore import KardoCore
from kardocore.api import RESTAPIGenerator, SwaggerUI, CORSMiddleware
from kardocore.db import Database, Model

# Define models
class User(Model):
    __table_name__ = "users"
    id: int
    email: str
    name: str

class Post(Model):
    __table_name__ = "posts"
    id: int
    title: str
    content: str
    user_id: int

# Initialize app
app = KardoCore()
db = Database("sqlite://app.db")

# Setup API
api = RESTAPIGenerator(base_path="/api/v1")
api.register_model(User, "users")
api.register_model(Post, "posts")

# Add routes
for path, method, handler in api.get_routes():
    app.add_route(path, handler, methods=[method])

# Add API docs
@app.route("/api/docs")
async def api_docs(request):
    return SwaggerUI.get_html("/api/openapi.json")

@app.route("/api/openapi.json")
async def openapi_spec(request):
    return api.get_openapi_spec()

# Add CORS
app.add_middleware(CORSMiddleware(allow_origins=["*"]))

# Run
app.run()
```

Now you have:
- Full REST API at `/api/v1/users` and `/api/v1/posts`
- Interactive docs at `/api/docs`
- CORS enabled for all origins

---

## API Response Format

### Success Response

```json
{
  "data": { ... },
  "message": "Operation successful"
}
```

### List Response

```json
{
  "data": [ ... ],
  "page": 1,
  "per_page": 20
}
```

### Error Response

```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

---

## Pagination

List endpoints support pagination via query parameters:

```
GET /api/v1/users?page=2&per_page=50
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `page` | Page number (1-indexed) | `1` |
| `per_page` | Items per page | `20` |

---

## Best Practices

1. **Use versioning** - Include version in base path (`/api/v1`)
2. **Enable CORS carefully** - Don't use `["*"]` in production
3. **Add authentication** - Protect endpoints with JWT or sessions
4. **Rate limiting** - Use rate limiting middleware
5. **Validate input** - Add validation to model fields
6. **Document custom endpoints** - Add to OpenAPI spec manually

---

## Security

### Authentication

```python
from kardocore.auth import JWTAuth

# Add JWT middleware
app.add_middleware(JWTAuth(secret_key="your-secret"))
```

### Rate Limiting

```python
from kardocore.auth import RateLimiter

# Limit API requests
limiter = RateLimiter(max_requests=100, window=60)
app.add_middleware(limiter)
```

---

## Links

- [Database Documentation](DATABASE.md)
- [Authentication Documentation](AUTHENTICATION.md)
- [KardoCore Documentation](../README.md)

