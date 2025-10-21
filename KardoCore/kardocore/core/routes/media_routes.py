"""
API de Gestión de Medios para KardoCore
"""

import json
import os
from core.media import media_manager, image_editor


async def handle_media_upload(request):
    """Maneja la subida de archivos"""
    try:
        # En producción, parsear multipart/form-data correctamente
        # Por ahora, respuesta de ejemplo
        return {
            'status': 200,
            'headers': [
                (b'content-type', b'application/json'),
            ],
            'body': json.dumps({
                'success': True,
                'message': 'Archivo subido correctamente',
                'media': {
                    'id': 'media_example_001',
                    'filename': 'example.jpg',
                    'url': '/uploads/images/2025/10/example.jpg',
                    'thumbnails': {
                        'thumb': {'url': '/uploads/images/2025/10/example_thumb.jpg', 'width': 150, 'height': 150},
                        'small': {'url': '/uploads/images/2025/10/example_small.jpg', 'width': 300, 'height': 300},
                        'medium': {'url': '/uploads/images/2025/10/example_medium.jpg', 'width': 600, 'height': 600},
                        'large': {'url': '/uploads/images/2025/10/example_large.jpg', 'width': 1200, 'height': 1200},
                    }
                }
            }).encode()
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({'success': False, 'error': str(e)}).encode()
        }


async def handle_media_list(request):
    """Lista los medios disponibles"""
    try:
        # Obtener parámetros de query
        query_string = request.get('query_string', '')
        params = {}
        if query_string:
            for param in query_string.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
        
        file_type = params.get('type', 'images')
        limit = int(params.get('limit', 50))
        offset = int(params.get('offset', 0))
        
        # Obtener lista de medios
        media_list = media_manager.list_media(file_type, limit, offset)
        
        return {
            'status': 200,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({
                'success': True,
                'media': media_list,
                'total': len(media_manager.media_db),
                'limit': limit,
                'offset': offset
            }).encode()
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({'success': False, 'error': str(e)}).encode()
        }


async def handle_media_search(request):
    """Busca medios por query"""
    try:
        query_string = request.get('query_string', '')
        query = ''
        if query_string:
            for param in query_string.split('&'):
                if param.startswith('q='):
                    query = param[2:]
                    break
        
        results = media_manager.search_media(query)
        
        return {
            'status': 200,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({
                'success': True,
                'results': results,
                'query': query
            }).encode()
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({'success': False, 'error': str(e)}).encode()
        }


async def handle_media_get(request, media_id):
    """Obtiene información de un medio específico"""
    try:
        media = media_manager.get_media(media_id)
        
        if not media:
            return {
                'status': 404,
                'headers': [(b'content-type', b'application/json')],
                'body': json.dumps({'success': False, 'error': 'Media no encontrado'}).encode()
            }
        
        return {
            'status': 200,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({
                'success': True,
                'media': media
            }).encode()
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({'success': False, 'error': str(e)}).encode()
        }


async def handle_media_update_metadata(request, media_id):
    """Actualiza la metadata de un medio"""
    try:
        # Parsear JSON del body
        body = request.get('body', b'')
        metadata = json.loads(body.decode())
        
        success = media_manager.update_metadata(media_id, metadata)
        
        if not success:
            return {
                'status': 404,
                'headers': [(b'content-type', b'application/json')],
                'body': json.dumps({'success': False, 'error': 'Media no encontrado'}).encode()
            }
        
        return {
            'status': 200,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({
                'success': True,
                'message': 'Metadata actualizada correctamente'
            }).encode()
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({'success': False, 'error': str(e)}).encode()
        }


async def handle_media_delete(request, media_id):
    """Elimina un medio"""
    try:
        success = media_manager.delete_media(media_id)
        
        if not success:
            return {
                'status': 404,
                'headers': [(b'content-type', b'application/json')],
                'body': json.dumps({'success': False, 'error': 'Media no encontrado'}).encode()
            }
        
        return {
            'status': 200,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({
                'success': True,
                'message': 'Media eliminado correctamente'
            }).encode()
        }
    except Exception as e:
        return {
            'status': 500,
            'headers': [(b'content-type', b'application/json')],
            'body': json.dumps({'success': False, 'error': str(e)}).encode()
        }


# Registrar rutas
def register_media_routes(app):
    """Registra las rutas de API de medios en la aplicación"""
    app.add_route('POST', '/api/media/upload', handle_media_upload)
    app.add_route('GET', '/api/media/list', handle_media_list)
    app.add_route('GET', '/api/media/search', handle_media_search)
    app.add_route('GET', '/api/media/{media_id}', handle_media_get)
    app.add_route('PUT', '/api/media/{media_id}/metadata', handle_media_update_metadata)
    app.add_route('DELETE', '/api/media/{media_id}', handle_media_delete)

