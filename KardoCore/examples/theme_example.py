"""
Ejemplo de uso del motor de plantillas KardoTheme

Demuestra las características principales del sistema de plantillas.
"""

from kardocore.theme import KardoTheme, render_template


def example_basic():
    """Ejemplo básico de renderizado."""
    print("="*60)
    print("Ejemplo 1: Renderizado Básico")
    print("="*60)
    
    template = """
    <h1>{title}</h1>
    <p>{description}</p>
    """
    
    theme = KardoTheme(template_dir=".")
    html = theme.render_string(template, {
        "title": "¡Hola, KardoTheme!",
        "description": "Motor de plantillas nativo de KardoCore"
    })
    
    print(html)
    print()


def example_loop():
    """Ejemplo de bucles."""
    print("="*60)
    print("Ejemplo 2: Bucles #for")
    print("="*60)
    
    template = """
    <ul>
    #for item in items
      <li>{item.name}: {item.price}</li>
    #end
    </ul>
    """
    
    theme = KardoTheme(template_dir=".")
    html = theme.render_string(template, {
        "items": [
            {"name": "Producto 1", "price": "$10"},
            {"name": "Producto 2", "price": "$20"},
            {"name": "Producto 3", "price": "$30"},
        ]
    })
    
    print(html)
    print()


def example_conditional():
    """Ejemplo de condicionales."""
    print("="*60)
    print("Ejemplo 3: Condicionales #if/#else")
    print("="*60)
    
    template = """
    #if user.is_admin
      <p>Bienvenido, administrador {user.name}</p>
    #else
      <p>Hola, {user.name}</p>
    #end
    """
    
    theme = KardoTheme(template_dir=".")
    
    # Usuario admin
    html1 = theme.render_string(template, {
        "user": {"name": "Juan", "is_admin": True}
    })
    print("Admin:", html1.strip())
    
    # Usuario normal
    html2 = theme.render_string(template, {
        "user": {"name": "María", "is_admin": False}
    })
    print("Normal:", html2.strip())
    print()


def example_nested():
    """Ejemplo de estructuras anidadas."""
    print("="*60)
    print("Ejemplo 4: Estructuras Anidadas")
    print("="*60)
    
    template = """
    <div class="posts">
    #for category in categories
      <section>
        <h2>{category.name}</h2>
        #if category.posts
          <ul>
          #for post in category.posts
            <li>{post.title}</li>
          #end
          </ul>
        #else
          <p>No hay posts en esta categoría</p>
        #end
      </section>
    #end
    </div>
    """
    
    theme = KardoTheme(template_dir=".")
    html = theme.render_string(template, {
        "categories": [
            {
                "name": "Tecnología",
                "posts": [
                    {"title": "Python 3.14"},
                    {"title": "KardoCore Framework"},
                ]
            },
            {
                "name": "Diseño",
                "posts": []
            },
        ]
    })
    
    print(html)
    print()


def example_auto_escape():
    """Ejemplo de escape automático (seguridad XSS)."""
    print("="*60)
    print("Ejemplo 5: Escape Automático (Anti-XSS)")
    print("="*60)
    
    template = """
    <div>
      <p>Comentario: {comment}</p>
    </div>
    """
    
    theme = KardoTheme(template_dir=".")
    html = theme.render_string(template, {
        "comment": "<script>alert('XSS')</script>Comentario malicioso"
    })
    
    print("HTML generado (script escapado):")
    print(html)
    print()


def example_from_file():
    """Ejemplo de renderizado desde archivo."""
    print("="*60)
    print("Ejemplo 6: Renderizado desde Archivo")
    print("="*60)
    
    try:
        theme = KardoTheme(template_dir="examples/templates")
        html = theme.render("example.html", {
            "page": {
                "title": "Mi Sitio Web",
                "description": "Construido con KardoCore y KardoTheme"
            },
            "user": {
                "is_authenticated": True,
                "name": "Juan Quezada",
                "email": "juan@example.com"
            },
            "posts": [
                {
                    "id": 1,
                    "title": "Introducción a KardoCore",
                    "excerpt": "Aprende los conceptos básicos del framework",
                    "author": "Juan"
                },
                {
                    "id": 2,
                    "title": "KardoTheme: Motor de Plantillas",
                    "excerpt": "Descubre la sintaxis expresiva de KardoTheme",
                    "author": "María"
                },
                {
                    "id": 3,
                    "title": "KardoCSS: Framework CSS Mobile-First",
                    "excerpt": "Construye interfaces responsive con facilidad",
                    "author": "Pedro"
                },
            ]
        })
        
        # Guardar HTML generado
        with open("examples/output.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        print("✅ HTML generado y guardado en examples/output.html")
        print(f"📏 Tamaño: {len(html)} bytes")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()


if __name__ == "__main__":
    print("\n" + "🎨 " + "="*58)
    print("  KardoTheme - Ejemplos de Uso del Motor de Plantillas")
    print("="*60 + "\n")
    
    example_basic()
    example_loop()
    example_conditional()
    example_nested()
    example_auto_escape()
    example_from_file()
    
    print("="*60)
    print("✨ Todos los ejemplos completados")
    print("="*60 + "\n")

