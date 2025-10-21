"""
Sistema de Gestión de Medios de KardoCore

Maneja subida, procesamiento, almacenamiento y gestión de imágenes y archivos multimedia.
Preparado para CDN y optimización automática.
"""

import os
import hashlib
import mimetypes
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import json


class MediaManager:
    """
    Gestor principal de medios.
    
    Características:
    - Subida de archivos con validación
    - Generación automática de thumbnails
    - Optimización de imágenes
    - Metadata completa
    - Preparado para CDN
    """
    
    def __init__(self, base_path: str = "/uploads", cdn_url: Optional[str] = None):
        """
        Inicializa el gestor de medios.
        
        Args:
            base_path: Ruta base para almacenamiento local
            cdn_url: URL del CDN (opcional, usa local si no se especifica)
        """
        self.base_path = base_path
        self.cdn_url = cdn_url
        self.cdn_enabled = cdn_url is not None
        
        # Configuración
        self.allowed_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.md'],
            'videos': ['.mp4', '.webm', '.ogg'],
            'audio': ['.mp3', '.wav', '.ogg']
        }
        
        self.max_file_size = 10 * 1024 * 1024  # 10 MB
        
        # Tamaños de thumbnails
        self.thumbnail_sizes = {
            'thumb': (150, 150),
            'small': (300, 300),
            'medium': (600, 600),
            'large': (1200, 1200),
        }
        
        # Base de datos de medios (en producción usar DB real)
        self.media_db = {}
        self._load_media_db()
    
    def _load_media_db(self):
        """Carga la base de datos de medios desde archivo JSON."""
        db_path = os.path.join(self.base_path, 'media_db.json')
        if os.path.exists(db_path):
            with open(db_path, 'r') as f:
                self.media_db = json.load(f)
    
    def _save_media_db(self):
        """Guarda la base de datos de medios en archivo JSON."""
        db_path = os.path.join(self.base_path, 'media_db.json')
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with open(db_path, 'w') as f:
            json.dump(self.media_db, f, indent=2)
    
    def upload_file(self, file_data: bytes, filename: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Sube un archivo al sistema.
        
        Args:
            file_data: Datos binarios del archivo
            filename: Nombre original del archivo
            metadata: Metadata adicional (alt, title, description, etc.)
        
        Returns:
            Diccionario con información del archivo subido
        """
        # Validar archivo
        validation = self._validate_file(file_data, filename)
        if not validation['valid']:
            raise ValueError(validation['error'])
        
        # Generar nombre único
        file_hash = hashlib.md5(file_data).hexdigest()[:12]
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        ext = os.path.splitext(filename)[1].lower()
        unique_filename = f"{timestamp}_{file_hash}{ext}"
        
        # Determinar tipo de archivo
        file_type = self._get_file_type(ext)
        
        # Crear estructura de carpetas
        year_month = datetime.now().strftime('%Y/%m')
        upload_dir = os.path.join(self.base_path, file_type, year_month)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Guardar archivo original
        file_path = os.path.join(upload_dir, unique_filename)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # Procesar imagen si es necesario
        thumbnails = {}
        if file_type == 'images' and ext != '.svg':
            thumbnails = self._generate_thumbnails(file_path, upload_dir, unique_filename)
        
        # Crear registro de media
        media_id = f"media_{file_hash}_{timestamp}"
        media_record = {
            'id': media_id,
            'filename': filename,
            'unique_filename': unique_filename,
            'path': file_path,
            'url': self._get_url(file_path),
            'type': file_type,
            'mime_type': mimetypes.guess_type(filename)[0],
            'size': len(file_data),
            'thumbnails': thumbnails,
            'metadata': metadata or {},
            'uploaded_at': datetime.now().isoformat(),
            'used_in': [],  # IDs de posts que usan esta imagen
        }
        
        # Guardar en base de datos
        self.media_db[media_id] = media_record
        self._save_media_db()
        
        return media_record
    
    def _validate_file(self, file_data: bytes, filename: str) -> Dict:
        """Valida un archivo antes de subirlo."""
        # Validar tamaño
        if len(file_data) > self.max_file_size:
            return {
                'valid': False,
                'error': f'Archivo demasiado grande. Máximo: {self.max_file_size / 1024 / 1024} MB'
            }
        
        # Validar extensión
        ext = os.path.splitext(filename)[1].lower()
        all_extensions = []
        for exts in self.allowed_extensions.values():
            all_extensions.extend(exts)
        
        if ext not in all_extensions:
            return {
                'valid': False,
                'error': f'Extensión no permitida: {ext}'
            }
        
        return {'valid': True}
    
    def _get_file_type(self, ext: str) -> str:
        """Determina el tipo de archivo por su extensión."""
        for file_type, extensions in self.allowed_extensions.items():
            if ext in extensions:
                return file_type
        return 'other'
    
    def _generate_thumbnails(self, original_path: str, output_dir: str, base_filename: str) -> Dict:
        """
        Genera thumbnails de una imagen.
        
        Nota: En producción usar Pillow o similar.
        Por ahora retorna estructura preparada.
        """
        thumbnails = {}
        
        try:
            # Importar Pillow si está disponible
            from PIL import Image
            
            img = Image.open(original_path)
            
            for size_name, (width, height) in self.thumbnail_sizes.items():
                # Calcular dimensiones manteniendo aspect ratio
                img_copy = img.copy()
                img_copy.thumbnail((width, height), Image.Resampling.LANCZOS)
                
                # Guardar thumbnail
                thumb_filename = f"{os.path.splitext(base_filename)[0]}_{size_name}.jpg"
                thumb_path = os.path.join(output_dir, thumb_filename)
                
                # Convertir a RGB si es necesario (para PNG con transparencia)
                if img_copy.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img_copy.size, (255, 255, 255))
                    if img_copy.mode == 'P':
                        img_copy = img_copy.convert('RGBA')
                    background.paste(img_copy, mask=img_copy.split()[-1] if img_copy.mode == 'RGBA' else None)
                    img_copy = background
                
                img_copy.save(thumb_path, 'JPEG', quality=85, optimize=True)
                
                thumbnails[size_name] = {
                    'path': thumb_path,
                    'url': self._get_url(thumb_path),
                    'width': img_copy.width,
                    'height': img_copy.height
                }
        
        except ImportError:
            # Pillow no disponible, retornar estructura vacía
            pass
        except Exception as e:
            print(f"Error generando thumbnails: {e}")
        
        return thumbnails
    
    def _get_url(self, file_path: str) -> str:
        """Genera la URL del archivo (local o CDN)."""
        relative_path = file_path.replace(self.base_path, '').lstrip('/')
        
        if self.cdn_enabled:
            return f"{self.cdn_url}/{relative_path}"
        else:
            return f"/uploads/{relative_path}"
    
    def get_media(self, media_id: str) -> Optional[Dict]:
        """Obtiene información de un medio por su ID."""
        return self.media_db.get(media_id)
    
    def list_media(self, file_type: Optional[str] = None, limit: int = 50, offset: int = 0) -> List[Dict]:
        """
        Lista medios con filtros y paginación.
        
        Args:
            file_type: Tipo de archivo a filtrar (images, documents, etc.)
            limit: Cantidad máxima de resultados
            offset: Offset para paginación
        
        Returns:
            Lista de registros de medios
        """
        media_list = list(self.media_db.values())
        
        # Filtrar por tipo
        if file_type:
            media_list = [m for m in media_list if m['type'] == file_type]
        
        # Ordenar por fecha (más recientes primero)
        media_list.sort(key=lambda x: x['uploaded_at'], reverse=True)
        
        # Paginación
        return media_list[offset:offset + limit]
    
    def update_metadata(self, media_id: str, metadata: Dict) -> bool:
        """Actualiza la metadata de un medio."""
        if media_id in self.media_db:
            self.media_db[media_id]['metadata'].update(metadata)
            self._save_media_db()
            return True
        return False
    
    def delete_media(self, media_id: str) -> bool:
        """
        Elimina un medio del sistema.
        
        Args:
            media_id: ID del medio a eliminar
        
        Returns:
            True si se eliminó correctamente
        """
        if media_id not in self.media_db:
            return False
        
        media = self.media_db[media_id]
        
        # Eliminar archivo original
        try:
            if os.path.exists(media['path']):
                os.remove(media['path'])
            
            # Eliminar thumbnails
            for thumb_data in media.get('thumbnails', {}).values():
                if os.path.exists(thumb_data['path']):
                    os.remove(thumb_data['path'])
        except Exception as e:
            print(f"Error eliminando archivos: {e}")
        
        # Eliminar de base de datos
        del self.media_db[media_id]
        self._save_media_db()
        
        return True
    
    def search_media(self, query: str) -> List[Dict]:
        """Busca medios por nombre o metadata."""
        results = []
        query_lower = query.lower()
        
        for media in self.media_db.values():
            # Buscar en nombre de archivo
            if query_lower in media['filename'].lower():
                results.append(media)
                continue
            
            # Buscar en metadata
            metadata = media.get('metadata', {})
            if any(query_lower in str(v).lower() for v in metadata.values()):
                results.append(media)
        
        return results
    
    def get_responsive_image_html(self, media_id: str, alt: str = "", 
                                  sizes: str = "(max-width: 768px) 100vw, 50vw") -> str:
        """
        Genera HTML de imagen responsive con srcset.
        
        Args:
            media_id: ID del medio
            alt: Texto alternativo
            sizes: Atributo sizes para responsive
        
        Returns:
            HTML de la imagen
        """
        media = self.get_media(media_id)
        if not media:
            return ""
        
        # Construir srcset
        srcset_parts = []
        thumbnails = media.get('thumbnails', {})
        
        for size_name, thumb_data in thumbnails.items():
            srcset_parts.append(f"{thumb_data['url']} {thumb_data['width']}w")
        
        srcset = ", ".join(srcset_parts)
        
        # Usar metadata si existe
        alt_text = media.get('metadata', {}).get('alt', alt)
        title = media.get('metadata', {}).get('title', '')
        
        html = f'<img src="{media["url"]}" '
        if srcset:
            html += f'srcset="{srcset}" sizes="{sizes}" '
        html += f'alt="{alt_text}" '
        if title:
            html += f'title="{title}" '
        html += 'loading="lazy" />'
        
        return html


class ImageEditor:
    """
    Editor básico de imágenes.
    
    Funcionalidades:
    - Crop
    - Resize
    - Rotate
    - Flip
    - Filtros básicos
    """
    
    def __init__(self, media_manager: MediaManager):
        self.media_manager = media_manager
    
    def crop_image(self, media_id: str, x: int, y: int, width: int, height: int) -> Dict:
        """Recorta una imagen."""
        try:
            from PIL import Image
            
            media = self.media_manager.get_media(media_id)
            if not media:
                raise ValueError("Media no encontrado")
            
            img = Image.open(media['path'])
            cropped = img.crop((x, y, x + width, y + height))
            
            # Guardar como nueva versión
            crop_filename = f"{os.path.splitext(media['unique_filename'])[0]}_crop.jpg"
            crop_path = os.path.join(os.path.dirname(media['path']), crop_filename)
            cropped.save(crop_path, 'JPEG', quality=90)
            
            return {
                'path': crop_path,
                'url': self.media_manager._get_url(crop_path),
                'width': width,
                'height': height
            }
        
        except ImportError:
            raise RuntimeError("Pillow no está instalado")
    
    def resize_image(self, media_id: str, width: int, height: int) -> Dict:
        """Redimensiona una imagen."""
        try:
            from PIL import Image
            
            media = self.media_manager.get_media(media_id)
            if not media:
                raise ValueError("Media no encontrado")
            
            img = Image.open(media['path'])
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Guardar como nueva versión
            resize_filename = f"{os.path.splitext(media['unique_filename'])[0]}_resize.jpg"
            resize_path = os.path.join(os.path.dirname(media['path']), resize_filename)
            resized.save(resize_path, 'JPEG', quality=90)
            
            return {
                'path': resize_path,
                'url': self.media_manager._get_url(resize_path),
                'width': width,
                'height': height
            }
        
        except ImportError:
            raise RuntimeError("Pillow no está instalado")


# Instancia global
media_manager = MediaManager(base_path="/home/ubuntu/testproject/uploads")
image_editor = ImageEditor(media_manager)

