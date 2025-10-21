/**
 * KardoSEO - Sistema de gestión SEO para KardoCore
 * Incluye análisis en tiempo real, vista previa de Google y preparado para IA
 */

class KardoSEO {
    constructor(options = {}) {
        this.options = {
            titleInput: options.titleInput || '#title',
            slugInput: options.slugInput || '#slug',
            seoTitleInput: options.seoTitleInput || '#seo_title',
            seoDescriptionInput: options.seoDescriptionInput || '#seo_description',
            seoKeywordsInput: options.seoKeywordsInput || '#seo_keywords',
            contentInput: options.contentInput || '#content',
            previewContainer: options.previewContainer || '#seo-preview',
            scoreContainer: options.scoreContainer || '#seo-score',
            suggestionsContainer: options.suggestionsContainer || '#seo-suggestions',
            autoSlug: options.autoSlug !== false,
            aiEnabled: options.aiEnabled || false,
            ...options
        };
        
        this.init();
    }
    
    init() {
        // Generar slug automático
        if (this.options.autoSlug) {
            this.setupAutoSlug();
        }
        
        // Sincronizar campos SEO
        this.setupSEOSync();
        
        // Contadores de caracteres
        this.setupCharCounters();
        
        // Vista previa de Google
        this.setupGooglePreview();
        
        // Análisis SEO en tiempo real
        this.setupRealTimeAnalysis();
        
        // Generador de keywords
        this.setupKeywordExtractor();
        
        // Preparar para IA (futuro)
        if (this.options.aiEnabled) {
            this.setupAIFeatures();
        }
    }
    
    setupAutoSlug() {
        const titleInput = document.querySelector(this.options.titleInput);
        const slugInput = document.querySelector(this.options.slugInput);
        
        if (!titleInput || !slugInput) return;
        
        titleInput.addEventListener('input', (e) => {
            if (!slugInput.dataset.manuallyEdited) {
                slugInput.value = this.slugify(e.target.value);
                this.updateGooglePreview();
            }
        });
        
        slugInput.addEventListener('input', () => {
            slugInput.dataset.manuallyEdited = 'true';
            this.updateGooglePreview();
        });
    }
    
    setupSEOSync() {
        const titleInput = document.querySelector(this.options.titleInput);
        const seoTitleInput = document.querySelector(this.options.seoTitleInput);
        
        if (!titleInput || !seoTitleInput) return;
        
        // Sincronizar título principal con SEO title si está vacío
        titleInput.addEventListener('input', (e) => {
            if (!seoTitleInput.value || !seoTitleInput.dataset.manuallyEdited) {
                seoTitleInput.value = e.target.value;
                this.updateGooglePreview();
            }
        });
        
        seoTitleInput.addEventListener('input', () => {
            seoTitleInput.dataset.manuallyEdited = 'true';
            this.updateGooglePreview();
        });
    }
    
    setupCharCounters() {
        // Contador para SEO Title
        this.setupCounter(this.options.seoTitleInput, 60, 'seo-title-counter');
        
        // Contador para SEO Description
        this.setupCounter(this.options.seoDescriptionInput, 160, 'seo-description-counter');
        
        // Contador para Keywords
        const keywordsInput = document.querySelector(this.options.seoKeywordsInput);
        if (keywordsInput) {
            const counter = document.getElementById('seo-keywords-counter');
            keywordsInput.addEventListener('input', () => {
                const keywords = keywordsInput.value.split(',').filter(k => k.trim());
                const count = keywords.length;
                if (counter) {
                    counter.textContent = `${count} keywords`;
                    counter.className = count > 10 ? 'k-text-warning' : count < 3 ? 'k-text-gray-500' : 'k-text-success';
                }
            });
        }
    }
    
    setupCounter(selector, maxLength, counterId) {
        const input = document.querySelector(selector);
        if (!input) return;
        
        const counter = document.getElementById(counterId);
        
        input.addEventListener('input', () => {
            const length = input.value.length;
            if (counter) {
                counter.textContent = `${length}/${maxLength}`;
                
                if (length > maxLength) {
                    counter.className = 'k-text-danger';
                } else if (length > maxLength * 0.9) {
                    counter.className = 'k-text-warning';
                } else if (length > maxLength * 0.5) {
                    counter.className = 'k-text-success';
                } else {
                    counter.className = 'k-text-gray-500';
                }
            }
            
            this.updateGooglePreview();
        });
    }
    
    setupGooglePreview() {
        const container = document.querySelector(this.options.previewContainer);
        if (!container) return;
        
        // Crear estructura de vista previa
        container.innerHTML = `
            <div class="google-preview k-bg-white k-p-4 k-rounded-lg k-border k-border-gray-200">
                <div class="k-text-xs k-text-gray-500 k-mb-2">Vista previa en Google</div>
                <div class="preview-url k-text-sm k-text-success k-mb-1"></div>
                <div class="preview-title k-text-xl k-text-primary k-mb-1 k-cursor-pointer hover:k-underline"></div>
                <div class="preview-description k-text-sm k-text-gray-700"></div>
            </div>
        `;
        
        this.updateGooglePreview();
    }
    
    updateGooglePreview() {
        const container = document.querySelector(this.options.previewContainer);
        if (!container) return;
        
        const slug = document.querySelector(this.options.slugInput)?.value || 'post-slug';
        const seoTitle = document.querySelector(this.options.seoTitleInput)?.value || 'Título del Post';
        const seoDescription = document.querySelector(this.options.seoDescriptionInput)?.value || 'Descripción del post...';
        
        const urlPreview = container.querySelector('.preview-url');
        const titlePreview = container.querySelector('.preview-title');
        const descPreview = container.querySelector('.preview-description');
        
        if (urlPreview) {
            urlPreview.textContent = `https://tudominio.com/post/${slug}`;
        }
        
        if (titlePreview) {
            const truncatedTitle = seoTitle.length > 60 ? seoTitle.substring(0, 57) + '...' : seoTitle;
            titlePreview.textContent = truncatedTitle;
        }
        
        if (descPreview) {
            const truncatedDesc = seoDescription.length > 160 ? seoDescription.substring(0, 157) + '...' : seoDescription;
            descPreview.textContent = truncatedDesc;
        }
    }
    
    setupRealTimeAnalysis() {
        const inputs = [
            this.options.titleInput,
            this.options.slugInput,
            this.options.seoTitleInput,
            this.options.seoDescriptionInput,
            this.options.seoKeywordsInput,
            this.options.contentInput
        ];
        
        inputs.forEach(selector => {
            const input = document.querySelector(selector);
            if (input) {
                input.addEventListener('input', () => {
                    this.debounce(() => this.analyzeSEO(), 500);
                });
            }
        });
        
        // Análisis inicial
        setTimeout(() => this.analyzeSEO(), 1000);
    }
    
    async analyzeSEO() {
        const data = this.collectFormData();
        
        // Análisis local (sin backend por ahora)
        const analysis = this.performLocalAnalysis(data);
        
        // Mostrar resultados
        this.displayAnalysis(analysis);
        
        // En el futuro, esto también llamará al backend para análisis IA
        if (this.options.aiEnabled) {
            // await this.getAIAnalysis(data);
        }
    }
    
    performLocalAnalysis(data) {
        let score = 0;
        const issues = [];
        const suggestions = [];
        
        // Análisis del título
        if (data.title) {
            const titleLen = data.title.length;
            if (titleLen >= 30 && titleLen <= 60) {
                score += 20;
            } else if (titleLen < 30) {
                issues.push('⚠️ El título es muy corto');
                suggestions.push('Amplía el título a 30-60 caracteres');
                score += 10;
            } else {
                issues.push('⚠️ El título es muy largo');
                suggestions.push('Acorta el título a 60 caracteres o menos');
                score += 10;
            }
        }
        
        // Análisis del slug
        if (data.slug) {
            if (data.slug.length <= 75 && /^[a-z0-9-]+$/.test(data.slug)) {
                score += 15;
            } else {
                issues.push('⚠️ El slug necesita mejoras');
                score += 5;
            }
        }
        
        // Análisis de meta descripción
        if (data.seo_description) {
            const descLen = data.seo_description.length;
            if (descLen >= 120 && descLen <= 160) {
                score += 20;
            } else if (descLen < 120) {
                issues.push('⚠️ Meta descripción muy corta');
                suggestions.push('Amplía la descripción a 120-160 caracteres');
                score += 10;
            } else {
                issues.push('⚠️ Meta descripción muy larga');
                suggestions.push('Acorta la descripción a 160 caracteres');
                score += 10;
            }
        } else {
            issues.push('❌ Falta meta descripción');
            suggestions.push('Agrega una descripción atractiva');
        }
        
        // Análisis de keywords
        if (data.seo_keywords) {
            const keywords = data.seo_keywords.split(',').filter(k => k.trim());
            if (keywords.length >= 3 && keywords.length <= 10) {
                score += 15;
            } else if (keywords.length < 3) {
                issues.push('⚠️ Pocas keywords');
                suggestions.push('Agrega 5-10 keywords relevantes');
                score += 5;
            } else {
                issues.push('⚠️ Demasiadas keywords');
                suggestions.push('Reduce a 5-10 keywords principales');
                score += 5;
            }
        } else {
            issues.push('⚠️ No hay keywords');
            suggestions.push('Agrega keywords relevantes');
        }
        
        // Análisis del contenido
        if (data.content) {
            const textContent = data.content.replace(/<[^>]+>/g, '');
            const words = textContent.split(/\s+/).length;
            
            if (words >= 300) {
                score += 15;
            } else {
                issues.push('⚠️ Contenido muy corto');
                suggestions.push('Amplía el contenido a al menos 300 palabras');
                score += 5;
            }
        }
        
        return {
            score,
            maxScore: 100,
            issues,
            suggestions
        };
    }
    
    displayAnalysis(analysis) {
        // Mostrar score
        const scoreContainer = document.querySelector(this.options.scoreContainer);
        if (scoreContainer) {
            const percentage = Math.round((analysis.score / analysis.maxScore) * 100);
            let color = 'k-text-danger';
            let label = 'Necesita mejoras';
            
            if (percentage >= 80) {
                color = 'k-text-success';
                label = 'Excelente';
            } else if (percentage >= 60) {
                color = 'k-text-warning';
                label = 'Bueno';
            }
            
            scoreContainer.innerHTML = `
                <div class="k-flex k-items-center k-gap-4">
                    <div class="k-text-4xl k-font-bold ${color}">${percentage}%</div>
                    <div>
                        <div class="k-text-lg k-font-semibold">${label}</div>
                        <div class="k-text-sm k-text-gray-600">Score SEO</div>
                    </div>
                </div>
                <div class="k-w-full k-bg-gray-200 k-rounded-full k-h-2 k-mt-4">
                    <div class="${color.replace('text', 'bg')} k-h-2 k-rounded-full" style="width: ${percentage}%"></div>
                </div>
            `;
        }
        
        // Mostrar sugerencias
        const suggestionsContainer = document.querySelector(this.options.suggestionsContainer);
        if (suggestionsContainer) {
            let html = '<div class="k-space-y-2">';
            
            if (analysis.issues.length > 0) {
                html += '<div class="k-font-semibold k-mb-2">Problemas detectados:</div>';
                analysis.issues.forEach(issue => {
                    html += `<div class="k-text-sm k-text-gray-700">${issue}</div>`;
                });
            }
            
            if (analysis.suggestions.length > 0) {
                html += '<div class="k-font-semibold k-mt-4 k-mb-2">Sugerencias:</div>';
                analysis.suggestions.forEach(suggestion => {
                    html += `<div class="k-text-sm k-text-blue-600">💡 ${suggestion}</div>`;
                });
            }
            
            if (analysis.issues.length === 0 && analysis.suggestions.length === 0) {
                html += '<div class="k-text-success">✅ Todo se ve bien!</div>';
            }
            
            html += '</div>';
            suggestionsContainer.innerHTML = html;
        }
    }
    
    setupKeywordExtractor() {
        const extractBtn = document.getElementById('extract-keywords-btn');
        if (!extractBtn) return;
        
        extractBtn.addEventListener('click', () => {
            const title = document.querySelector(this.options.titleInput)?.value || '';
            const content = document.querySelector(this.options.contentInput)?.value || '';
            const keywordsInput = document.querySelector(this.options.seoKeywordsInput);
            
            if (!keywordsInput) return;
            
            const keywords = this.extractKeywords(title, content);
            keywordsInput.value = keywords.join(', ');
            keywordsInput.dispatchEvent(new Event('input'));
        });
    }
    
    extractKeywords(title, content) {
        // Limpiar HTML
        const text = (title + ' ' + content).replace(/<[^>]+>/g, '').toLowerCase();
        
        // Palabras comunes a ignorar
        const stopWords = new Set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no',
            'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'todo',
            'the', 'be', 'to', 'of', 'and', 'in', 'that', 'have', 'it', 'for'
        ]);
        
        // Extraer palabras
        const words = text.match(/\b[a-záéíóúñ]{4,}\b/g) || [];
        
        // Contar frecuencia
        const wordFreq = {};
        words.forEach(word => {
            if (!stopWords.has(word)) {
                wordFreq[word] = (wordFreq[word] || 0) + 1;
            }
        });
        
        // Ordenar y retornar top 5
        return Object.entries(wordFreq)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(([word]) => word);
    }
    
    setupAIFeatures() {
        // Placeholder para futuras características de IA
        console.log('🤖 Características de IA preparadas para integración futura');
        
        // Aquí se agregarán:
        // - Botón "Optimizar con IA"
        // - Sugerencias de títulos alternativos
        // - Análisis semántico de keywords
        // - Generación de meta descripciones
    }
    
    collectFormData() {
        return {
            title: document.querySelector(this.options.titleInput)?.value || '',
            slug: document.querySelector(this.options.slugInput)?.value || '',
            seo_title: document.querySelector(this.options.seoTitleInput)?.value || '',
            seo_description: document.querySelector(this.options.seoDescriptionInput)?.value || '',
            seo_keywords: document.querySelector(this.options.seoKeywordsInput)?.value || '',
            content: document.querySelector(this.options.contentInput)?.value || ''
        };
    }
    
    slugify(text) {
        return text
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9\s-]/g, '')
            .trim()
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-');
    }
    
    debounce(func, wait) {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(func, wait);
    }
}

// Auto-inicializar si existe el contenedor SEO
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('#seo-preview') || document.querySelector('[data-kardo-seo]')) {
        window.kardoSEO = new KardoSEO();
    }
});

