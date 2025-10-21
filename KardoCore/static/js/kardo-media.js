/**
 * KardoMedia - Sistema de Gestión de Medios
 * 
 * Características:
 * - Lazy loading automático
 * - Responsive images
 * - WebP support con fallback
 * - Optimización de rendimiento
 * - Integración con editor
 */

class KardoMedia {
    constructor(options = {}) {
        this.options = {
            apiEndpoint: options.apiEndpoint || '/api/media',
            maxFileSize: options.maxFileSize || 10 * 1024 * 1024, // 10 MB
            allowedTypes: options.allowedTypes || ['image/jpeg', 'image/png', 'image/gif', 'image/webp'],
            lazyLoad: options.lazyLoad !== false,
            webpSupport: null, // Se detecta automáticamente
            ...options
        };
        
        this.mediaLibrary = [];
        this.selectedMedia = [];
        
        this.init();
    }
    
    init() {
        this.detectWebPSupport();
        if (this.options.lazyLoad) {
            this.initLazyLoading();
        }
        this.initIntersectionObserver();
    }
    
    /**
     * Detecta soporte de WebP en el navegador
     */
    detectWebPSupport() {
        const canvas = document.createElement('canvas');
        if (canvas.getContext && canvas.getContext('2d')) {
            this.options.webpSupport = canvas.toDataURL('image/webp').indexOf('data:image/webp') === 0;
        } else {
            this.options.webpSupport = false;
        }
    }
    
    /**
     * Inicializa lazy loading para todas las imágenes
     */
    initLazyLoading() {
        // Usar Intersection Observer para lazy loading eficiente
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        this.loadImage(img);
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px', // Cargar 50px antes de entrar en viewport
                threshold: 0.01
            });
            
            // Observar todas las imágenes con data-src
            document.querySelectorAll('img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        } else {
            // Fallback para navegadores sin Intersection Observer
            document.querySelectorAll('img[data-src]').forEach(img => {
                this.loadImage(img);
            });
        }
    }
    
    /**
     * Carga una imagen de forma optimizada
     */
    loadImage(img) {
        const src = img.dataset.src;
        const srcset = img.dataset.srcset;
        
        if (!src) return;
        
        // Crear imagen temporal para precargar
        const tempImg = new Image();
        
        tempImg.onload = () => {
            img.src = src;
            if (srcset) {
                img.srcset = srcset;
            }
            img.classList.add('loaded');
            img.removeAttribute('data-src');
            img.removeAttribute('data-srcset');
        };
        
        tempImg.onerror = () => {
            img.classList.add('error');
            console.error(`Error cargando imagen: ${src}`);
        };
        
        tempImg.src = src;
    }
    
    /**
     * Inicializa Intersection Observer para animaciones y efectos
     */
    initIntersectionObserver() {
        if ('IntersectionObserver' in window) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('in-view');
                    }
                });
            }, {
                threshold: 0.1
            });
            
            document.querySelectorAll('.media-item').forEach(item => {
                observer.observe(item);
            });
        }
    }
    
    /**
     * Sube un archivo al servidor
     */
    async uploadFile(file, metadata = {}) {
        // Validar archivo
        const validation = this.validateFile(file);
        if (!validation.valid) {
            throw new Error(validation.error);
        }
        
        // Crear FormData
        const formData = new FormData();
        formData.append('file', file);
        formData.append('metadata', JSON.stringify(metadata));
        
        // Subir con progreso
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            
            // Progreso de subida
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percentComplete = (e.loaded / e.total) * 100;
                    this.onUploadProgress(percentComplete, file.name);
                }
            });
            
            // Completado
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } else {
                    reject(new Error(`Error ${xhr.status}: ${xhr.statusText}`));
                }
            });
            
            // Error
            xhr.addEventListener('error', () => {
                reject(new Error('Error de red al subir archivo'));
            });
            
            xhr.open('POST', `${this.options.apiEndpoint}/upload`);
            xhr.send(formData);
        });
    }
    
    /**
     * Valida un archivo antes de subirlo
     */
    validateFile(file) {
        // Validar tamaño
        if (file.size > this.options.maxFileSize) {
            return {
                valid: false,
                error: `Archivo demasiado grande. Máximo: ${this.options.maxFileSize / 1024 / 1024} MB`
            };
        }
        
        // Validar tipo
        if (!this.options.allowedTypes.includes(file.type)) {
            return {
                valid: false,
                error: `Tipo de archivo no permitido: ${file.type}`
            };
        }
        
        return { valid: true };
    }
    
    /**
     * Callback de progreso de subida
     */
    onUploadProgress(percent, filename) {
        // Emitir evento personalizado
        const event = new CustomEvent('media:upload:progress', {
            detail: { percent, filename }
        });
        document.dispatchEvent(event);
    }
    
    /**
     * Obtiene la lista de medios
     */
    async getMediaList(filters = {}) {
        const params = new URLSearchParams(filters);
        const response = await fetch(`${this.options.apiEndpoint}/list?${params}`);
        
        if (!response.ok) {
            throw new Error('Error obteniendo lista de medios');
        }
        
        this.mediaLibrary = await response.json();
        return this.mediaLibrary;
    }
    
    /**
     * Busca medios
     */
    async searchMedia(query) {
        const response = await fetch(`${this.options.apiEndpoint}/search?q=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error('Error buscando medios');
        }
        
        return await response.json();
    }
    
    /**
     * Actualiza metadata de un medio
     */
    async updateMetadata(mediaId, metadata) {
        const response = await fetch(`${this.options.apiEndpoint}/${mediaId}/metadata`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(metadata)
        });
        
        if (!response.ok) {
            throw new Error('Error actualizando metadata');
        }
        
        return await response.json();
    }
    
    /**
     * Elimina un medio
     */
    async deleteMedia(mediaId) {
        const response = await fetch(`${this.options.apiEndpoint}/${mediaId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('Error eliminando medio');
        }
        
        return true;
    }
    
    /**
     * Genera HTML de imagen optimizada
     */
    generateOptimizedImageHTML(media, options = {}) {
        const {
            alt = media.metadata?.alt || '',
            title = media.metadata?.title || '',
            className = '',
            sizes = '(max-width: 768px) 100vw, 50vw',
            loading = 'lazy',
            position = 'center', // left, center, right, full
            caption = media.metadata?.caption || ''
        } = options;
        
        // Construir srcset
        const srcset = Object.entries(media.thumbnails || {})
            .map(([name, thumb]) => `${thumb.url} ${thumb.width}w`)
            .join(', ');
        
        // Clases de posicionamiento
        const positionClass = `img-${position}`;
        
        // HTML de la imagen
        let html = `<figure class="media-figure ${positionClass} ${className}">`;
        
        // Placeholder blur (LQIP)
        const placeholder = media.thumbnails?.thumb?.url || media.url;
        html += `<div class="img-wrapper" style="background-image: url('${placeholder}'); filter: blur(10px);">`;
        
        html += `<img `;
        html += `src="${media.url}" `;
        if (srcset) {
            html += `srcset="${srcset}" `;
            html += `sizes="${sizes}" `;
        }
        html += `alt="${this.escapeHtml(alt)}" `;
        if (title) {
            html += `title="${this.escapeHtml(title)}" `;
        }
        html += `loading="${loading}" `;
        html += `width="${media.thumbnails?.large?.width || 1200}" `;
        html += `height="${media.thumbnails?.large?.height || 800}" `;
        html += `class="responsive-img" `;
        html += `/></div>`;
        
        // Caption
        if (caption) {
            html += `<figcaption>${this.escapeHtml(caption)}</figcaption>`;
        }
        
        html += `</figure>`;
        
        return html;
    }
    
    /**
     * Escapa HTML para prevenir XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    /**
     * Abre el modal de Media Library
     */
    openMediaLibrary(callback) {
        this.mediaLibraryCallback = callback;
        this.showMediaLibraryModal();
    }
    
    /**
     * Muestra el modal de Media Library
     */
    async showMediaLibraryModal() {
        // Obtener medios
        await this.getMediaList({ type: 'images' });
        
        // Crear modal
        const modal = this.createMediaLibraryModal();
        document.body.appendChild(modal);
        
        // Mostrar con animación
        setTimeout(() => modal.classList.add('show'), 10);
    }
    
    /**
     * Crea el HTML del modal de Media Library
     */
    createMediaLibraryModal() {
        const modal = document.createElement('div');
        modal.className = 'media-library-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="this.parentElement.remove()"></div>
            <div class="modal-content">
                <div class="modal-header">
                    <h2>📸 Biblioteca de Medios</h2>
                    <button class="close-btn" onclick="this.closest('.media-library-modal').remove()">✕</button>
                </div>
                
                <div class="modal-toolbar">
                    <div class="search-box">
                        <input type="text" placeholder="Buscar imágenes..." id="media-search">
                    </div>
                    <button class="k-btn k-btn-primary" onclick="document.getElementById('media-upload-input').click()">
                        📤 Subir Nueva Imagen
                    </button>
                    <input type="file" id="media-upload-input" accept="image/*" multiple style="display: none;">
                </div>
                
                <div class="media-grid" id="media-grid">
                    ${this.renderMediaGrid()}
                </div>
                
                <div class="modal-footer">
                    <button class="k-btn k-btn-secondary" onclick="this.closest('.media-library-modal').remove()">
                        Cancelar
                    </button>
                    <button class="k-btn k-btn-primary" id="insert-media-btn">
                        Insertar Seleccionadas
                    </button>
                </div>
            </div>
        `;
        
        // Event listeners
        this.attachMediaLibraryEvents(modal);
        
        return modal;
    }
    
    /**
     * Renderiza la grilla de medios
     */
    renderMediaGrid() {
        if (this.mediaLibrary.length === 0) {
            return '<div class="empty-state">No hay imágenes. Sube tu primera imagen.</div>';
        }
        
        return this.mediaLibrary.map(media => `
            <div class="media-item" data-media-id="${media.id}">
                <div class="media-thumbnail">
                    <img src="${media.thumbnails?.small?.url || media.url}" alt="${media.filename}">
                    <div class="media-overlay">
                        <button class="select-btn" data-media-id="${media.id}">✓</button>
                    </div>
                </div>
                <div class="media-info">
                    <div class="media-filename">${media.filename}</div>
                    <div class="media-size">${this.formatFileSize(media.size)}</div>
                </div>
            </div>
        `).join('');
    }
    
    /**
     * Adjunta event listeners al modal
     */
    attachMediaLibraryEvents(modal) {
        // Búsqueda
        const searchInput = modal.querySelector('#media-search');
        searchInput?.addEventListener('input', async (e) => {
            const results = await this.searchMedia(e.target.value);
            this.mediaLibrary = results;
            modal.querySelector('#media-grid').innerHTML = this.renderMediaGrid();
        });
        
        // Upload
        const uploadInput = modal.querySelector('#media-upload-input');
        uploadInput?.addEventListener('change', async (e) => {
            const files = Array.from(e.target.files);
            for (const file of files) {
                try {
                    await this.uploadFile(file);
                } catch (error) {
                    console.error('Error subiendo archivo:', error);
                }
            }
            // Recargar lista
            await this.getMediaList({ type: 'images' });
            modal.querySelector('#media-grid').innerHTML = this.renderMediaGrid();
        });
        
        // Selección de medios
        modal.addEventListener('click', (e) => {
            if (e.target.classList.contains('select-btn')) {
                const mediaId = e.target.dataset.mediaId;
                this.toggleMediaSelection(mediaId, modal);
            }
        });
        
        // Insertar
        const insertBtn = modal.querySelector('#insert-media-btn');
        insertBtn?.addEventListener('click', () => {
            if (this.mediaLibraryCallback) {
                this.mediaLibraryCallback(this.selectedMedia);
            }
            modal.remove();
        });
    }
    
    /**
     * Toggle selección de un medio
     */
    toggleMediaSelection(mediaId, modal) {
        const index = this.selectedMedia.findIndex(m => m.id === mediaId);
        
        if (index > -1) {
            this.selectedMedia.splice(index, 1);
        } else {
            const media = this.mediaLibrary.find(m => m.id === mediaId);
            if (media) {
                this.selectedMedia.push(media);
            }
        }
        
        // Actualizar UI
        const item = modal.querySelector(`[data-media-id="${mediaId}"]`);
        item?.classList.toggle('selected');
    }
    
    /**
     * Formatea el tamaño de archivo
     */
    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
        return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
    }
}

// Inicializar automáticamente
if (typeof window !== 'undefined') {
    window.KardoMedia = KardoMedia;
    
    // Auto-init lazy loading
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            new KardoMedia();
        });
    } else {
        new KardoMedia();
    }
}

