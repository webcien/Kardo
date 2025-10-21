"""
KardoCore - Theme CLI
Comandos CLI para gestión de temas
"""

import click
from kardocore.packages.manager import PackageManager


@click.group()
def theme():
    """Gestión de temas para KardoCore"""
    pass


@theme.command()
@click.argument('slug')
@click.option('--type', '-t', default='frontend', type=click.Choice(['frontend', 'backend']), 
              help='Tipo de tema (frontend o backend)')
@click.option('--source', '-s', default='registry', type=click.Choice(['registry', 'github', 'local']),
              help='Fuente del tema')
@click.option('--path', '-p', default=None, help='Ruta local del tema (solo para source=local)')
def install(slug, type, source, path):
    """
    Instala un tema desde el registry o una fuente personalizada.
    
    Ejemplos:
    
        kardo theme install wellness-clinic
        
        kardo theme install admin-modern --type backend
        
        kardo theme install my-theme --source local --path /path/to/theme
    """
    import os
    
    # Obtener directorio del proyecto
    project_root = os.getcwd()
    
    # Crear gestor de paquetes
    manager = PackageManager(project_root)
    
    # Instalar tema
    if source == 'local':
        success = manager._install_from_local(slug, type, path)
    else:
        success = manager.install_theme(slug, type, source)
    
    if success:
        click.echo(f"✅ Tema '{slug}' instalado exitosamente")
        click.echo(f"📁 Ubicación: themes/{type}/{slug}")
        click.echo(f"\nPara activar el tema, edita tu configuración:")
        click.echo(f"  theme: '{slug}'")
    else:
        click.echo(f"❌ Error al instalar el tema '{slug}'")
        raise click.Abort()


@theme.command()
@click.option('--type', '-t', default=None, type=click.Choice(['frontend', 'backend']),
              help='Filtrar por tipo de tema')
def list(type):
    """
    Lista todos los temas instalados.
    
    Ejemplos:
    
        kardo theme list
        
        kardo theme list --type frontend
    """
    import os
    from tabulate import tabulate
    
    project_root = os.getcwd()
    manager = PackageManager(project_root)
    
    themes = manager.list_installed_themes(type)
    
    if not themes:
        click.echo("No hay temas instalados")
        return
    
    # Preparar datos para tabla
    table_data = []
    for theme in themes:
        table_data.append([
            theme.get('name', 'N/A'),
            theme.get('slug', 'N/A'),
            theme.get('type', 'N/A'),
            theme.get('version', 'N/A'),
            theme.get('category', 'N/A'),
        ])
    
    headers = ['Nombre', 'Slug', 'Tipo', 'Versión', 'Categoría']
    click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
    click.echo(f"\n📊 Total: {len(themes)} tema(s) instalado(s)")


@theme.command()
@click.argument('slug')
@click.option('--type', '-t', default='frontend', type=click.Choice(['frontend', 'backend']),
              help='Tipo de tema')
def info(slug, type):
    """
    Muestra información detallada de un tema instalado.
    
    Ejemplos:
    
        kardo theme info wellness-clinic
        
        kardo theme info admin-modern --type backend
    """
    import os
    
    project_root = os.getcwd()
    manager = PackageManager(project_root)
    
    theme = manager.get_theme_info(slug, type)
    
    if not theme:
        click.echo(f"❌ El tema '{slug}' no está instalado")
        raise click.Abort()
    
    # Mostrar información
    click.echo(f"\n{'='*60}")
    click.echo(f"  {theme.get('name', 'N/A')}")
    click.echo(f"{'='*60}\n")
    
    click.echo(f"Slug:         {theme.get('slug', 'N/A')}")
    click.echo(f"Versión:      {theme.get('version', 'N/A')}")
    click.echo(f"Tipo:         {theme.get('type', 'N/A')}")
    click.echo(f"Categoría:    {theme.get('category', 'N/A')}")
    click.echo(f"Autor:        {theme.get('author', 'N/A')}")
    click.echo(f"Licencia:     {theme.get('license', 'N/A')}")
    click.echo(f"\nDescripción:\n  {theme.get('description', 'N/A')}")
    
    if theme.get('tags'):
        click.echo(f"\nTags:\n  {', '.join(theme.get('tags', []))}")
    
    if theme.get('features'):
        click.echo(f"\nCaracterísticas:")
        for feature in theme.get('features', []):
            click.echo(f"  • {feature}")
    
    click.echo(f"\nUbicación:\n  {theme.get('installed_path', 'N/A')}")
    click.echo()


@theme.command()
@click.argument('slug')
@click.option('--type', '-t', default='frontend', type=click.Choice(['frontend', 'backend']),
              help='Tipo de tema')
@click.confirmation_option(prompt='¿Estás seguro de que quieres desinstalar este tema?')
def uninstall(slug, type):
    """
    Desinstala un tema.
    
    Ejemplos:
    
        kardo theme uninstall wellness-clinic
        
        kardo theme uninstall admin-modern --type backend
    """
    import os
    
    project_root = os.getcwd()
    manager = PackageManager(project_root)
    
    success = manager.uninstall_theme(slug, type)
    
    if success:
        click.echo(f"✅ Tema '{slug}' desinstalado exitosamente")
    else:
        click.echo(f"❌ Error al desinstalar el tema '{slug}'")
        raise click.Abort()


@theme.command()
@click.argument('query')
@click.option('--type', '-t', default=None, type=click.Choice(['frontend', 'backend']),
              help='Filtrar por tipo de tema')
def search(query, type):
    """
    Busca temas en el registry oficial.
    
    Ejemplos:
    
        kardo theme search salud
        
        kardo theme search dashboard --type backend
    """
    import os
    from tabulate import tabulate
    
    project_root = os.getcwd()
    manager = PackageManager(project_root)
    
    click.echo(f"🔍 Buscando '{query}' en el registry...")
    
    results = manager.search_themes(query, type)
    
    if not results:
        click.echo(f"No se encontraron temas que coincidan con '{query}'")
        return
    
    # Preparar datos para tabla
    table_data = []
    for theme in results:
        table_data.append([
            theme.get('name', 'N/A'),
            theme.get('slug', 'N/A'),
            theme.get('type', 'N/A'),
            theme.get('category', 'N/A'),
            theme.get('description', 'N/A')[:50] + '...' if len(theme.get('description', '')) > 50 else theme.get('description', 'N/A'),
        ])
    
    headers = ['Nombre', 'Slug', 'Tipo', 'Categoría', 'Descripción']
    click.echo(tabulate(table_data, headers=headers, tablefmt='grid'))
    click.echo(f"\n📊 Resultados: {len(results)} tema(s) encontrado(s)")
    click.echo(f"\nPara instalar un tema, usa: kardo theme install <slug>")


if __name__ == '__main__':
    theme()

