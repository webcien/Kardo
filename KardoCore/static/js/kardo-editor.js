/**
 * KardoEditor - Editor de texto enriquecido nativo para KardoCore
 * Editor WYSIWYG ligero y moderno
 */

class KardoEditor {
    constructor(element, options = {}) {
        this.element = element;
        this.options = {
            height: '400px',
            toolbar: ['bold', 'italic', 'underline', '|', 'h1', 'h2', 'h3', '|', 'ul', 'ol', '|', 'link', 'image', '|', 'code', 'quote'],
            placeholder: 'Escribe aquí...',
            ...options
        };
        
        this.init();
    }
    
    init() {
        // Ocultar textarea original
        this.element.style.display = 'none';
        
        // Crear contenedor del editor
        this.container = document.createElement('div');
        this.container.className = 'kardo-editor';
        this.element.parentNode.insertBefore(this.container, this.element.nextSibling);
        
        // Crear toolbar
        this.createToolbar();
        
        // Crear área de edición
        this.createEditor();
        
        // Sincronizar con textarea
        this.syncContent();
        
        // Cargar contenido inicial
        if (this.element.value) {
            this.editor.innerHTML = this.element.value;
        }
    }
    
    createToolbar() {
        this.toolbar = document.createElement('div');
        this.toolbar.className = 'kardo-editor-toolbar';
        this.container.appendChild(this.toolbar);
        
        this.options.toolbar.forEach(tool => {
            if (tool === '|') {
                const separator = document.createElement('span');
                separator.className = 'kardo-editor-separator';
                separator.textContent = '|';
                this.toolbar.appendChild(separator);
            } else {
                const button = this.createToolbarButton(tool);
                this.toolbar.appendChild(button);
            }
        });
    }
    
    createToolbarButton(tool) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'kardo-editor-btn';
        button.title = this.getToolTitle(tool);
        button.innerHTML = this.getToolIcon(tool);
        
        button.addEventListener('click', (e) => {
            e.preventDefault();
            this.execCommand(tool);
        });
        
        return button;
    }
    
    createEditor() {
        this.editor = document.createElement('div');
        this.editor.className = 'kardo-editor-content';
        this.editor.contentEditable = true;
        this.editor.style.minHeight = this.options.height;
        
        if (this.options.placeholder) {
            this.editor.dataset.placeholder = this.options.placeholder;
        }
        
        this.container.appendChild(this.editor);
        
        // Eventos
        this.editor.addEventListener('input', () => this.syncContent());
        this.editor.addEventListener('paste', (e) => this.handlePaste(e));
    }
    
    execCommand(command) {
        this.editor.focus();
        
        switch(command) {
            case 'bold':
                document.execCommand('bold');
                break;
            case 'italic':
                document.execCommand('italic');
                break;
            case 'underline':
                document.execCommand('underline');
                break;
            case 'h1':
            case 'h2':
            case 'h3':
                document.execCommand('formatBlock', false, command);
                break;
            case 'ul':
                document.execCommand('insertUnorderedList');
                break;
            case 'ol':
                document.execCommand('insertOrderedList');
                break;
            case 'link':
                this.insertLink();
                break;
            case 'image':
                this.insertImage();
                break;
            case 'code':
                this.insertCode();
                break;
            case 'quote':
                document.execCommand('formatBlock', false, 'blockquote');
                break;
        }
        
        this.syncContent();
    }
    
    insertLink() {
        const url = prompt('Ingresa la URL:');
        if (url) {
            document.execCommand('createLink', false, url);
        }
    }
    
    insertImage() {
        // Usar Media Library si está disponible
        if (window.kardoMedia) {
            window.kardoMedia.openMediaLibrary((selectedMedia) => {
                selectedMedia.forEach(media => {
                    const imageOptions = this.showImageOptionsDialog();
                    const imageHTML = window.kardoMedia.generateOptimizedImageHTML(media, imageOptions);
                    this.insertHTML(imageHTML);
                });
            });
        } else {
            // Fallback a prompt
            const url = prompt('Ingresa la URL de la imagen:');
            if (url) {
                const alt = prompt('Texto alternativo (opcional):') || '';
                this.insertHTML(`<img src="${url}" alt="${alt}" loading="lazy" class="responsive-img">`);
            }
        }
    }
    
    showImageOptionsDialog() {
        const position = prompt('Posición (left/center/right/full):', 'center') || 'center';
        const caption = prompt('Pie de foto (opcional):') || '';
        
        return {
            position,
            caption,
            loading: 'lazy',
            sizes: position === 'full' ? '100vw' : '(max-width: 768px) 100vw, 50vw'
        };
    }
    
    insertHTML(html) {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.deleteContents();
            const fragment = range.createContextualFragment(html);
            range.insertNode(fragment);
        }
    }
    
    insertCode() {
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const code = document.createElement('code');
        code.textContent = range.toString() || 'código';
        range.deleteContents();
        range.insertNode(code);
    }
    
    handlePaste(e) {
        e.preventDefault();
        
        // Obtener texto plano
        const text = e.clipboardData.getData('text/plain');
        
        // Insertar como texto plano
        document.execCommand('insertText', false, text);
    }
    
    syncContent() {
        this.element.value = this.editor.innerHTML;
        
        // Trigger change event
        const event = new Event('change', { bubbles: true });
        this.element.dispatchEvent(event);
    }
    
    getContent() {
        return this.editor.innerHTML;
    }
    
    setContent(html) {
        this.editor.innerHTML = html;
        this.syncContent();
    }
    
    getToolTitle(tool) {
        const titles = {
            bold: 'Negrita',
            italic: 'Cursiva',
            underline: 'Subrayado',
            h1: 'Título 1',
            h2: 'Título 2',
            h3: 'Título 3',
            ul: 'Lista',
            ol: 'Lista numerada',
            link: 'Enlace',
            image: 'Imagen',
            code: 'Código',
            quote: 'Cita'
        };
        return titles[tool] || tool;
    }
    
    getToolIcon(tool) {
        const icons = {
            bold: '<strong>B</strong>',
            italic: '<em>I</em>',
            underline: '<u>U</u>',
            h1: 'H1',
            h2: 'H2',
            h3: 'H3',
            ul: '• Lista',
            ol: '1. Lista',
            link: '🔗',
            image: '🖼️',
            code: '</>',
            quote: '❝❞'
        };
        return icons[tool] || tool;
    }
}

// CSS para el editor (se puede mover a un archivo CSS separado)
const editorStyles = `
.kardo-editor {
    border: 1px solid #d1d5db;
    border-radius: 0.5rem;
    overflow: hidden;
    background: white;
}

.kardo-editor-toolbar {
    display: flex;
    gap: 0.25rem;
    padding: 0.5rem;
    background: #f3f4f6;
    border-bottom: 1px solid #d1d5db;
    flex-wrap: wrap;
}

.kardo-editor-btn {
    padding: 0.5rem 0.75rem;
    border: 1px solid #d1d5db;
    background: white;
    border-radius: 0.25rem;
    cursor: pointer;
    font-size: 0.875rem;
    transition: all 0.2s;
}

.kardo-editor-btn:hover {
    background: #e5e7eb;
    border-color: #9ca3af;
}

.kardo-editor-btn:active {
    background: #d1d5db;
}

.kardo-editor-separator {
    padding: 0 0.5rem;
    color: #d1d5db;
    display: flex;
    align-items: center;
}

.kardo-editor-content {
    padding: 1rem;
    min-height: 300px;
    max-height: 600px;
    overflow-y: auto;
    outline: none;
}

.kardo-editor-content:empty:before {
    content: attr(data-placeholder);
    color: #9ca3af;
    pointer-events: none;
}

.kardo-editor-content h1 {
    font-size: 2rem;
    font-weight: bold;
    margin: 1rem 0;
}

.kardo-editor-content h2 {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0.875rem 0;
}

.kardo-editor-content h3 {
    font-size: 1.25rem;
    font-weight: bold;
    margin: 0.75rem 0;
}

.kardo-editor-content p {
    margin: 0.5rem 0;
}

.kardo-editor-content ul,
.kardo-editor-content ol {
    margin: 0.5rem 0;
    padding-left: 2rem;
}

.kardo-editor-content blockquote {
    border-left: 4px solid #3b82f6;
    padding-left: 1rem;
    margin: 1rem 0;
    color: #6b7280;
    font-style: italic;
}

.kardo-editor-content code {
    background: #f3f4f6;
    padding: 0.125rem 0.25rem;
    border-radius: 0.25rem;
    font-family: monospace;
    font-size: 0.875em;
}

.kardo-editor-content a {
    color: #3b82f6;
    text-decoration: underline;
}

.kardo-editor-content img {
    max-width: 100%;
    height: auto;
    margin: 1rem 0;
}
`;

// Inyectar estilos
if (!document.getElementById('kardo-editor-styles')) {
    const style = document.createElement('style');
    style.id = 'kardo-editor-styles';
    style.textContent = editorStyles;
    document.head.appendChild(style);
}

// Auto-inicializar editores
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-kardo-editor]').forEach(textarea => {
        new KardoEditor(textarea);
    });
});

