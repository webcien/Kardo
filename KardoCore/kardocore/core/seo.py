"""
Módulo SEO de KardoCore
Sistema modular de SEO con soporte para optimización IA
"""
from typing import Dict, List, Optional, Tuple
import re
from datetime import datetime


class SEOAnalyzer:
    """Analizador SEO con hooks para IA futura"""
    
    def __init__(self):
        self.ai_enabled = False  # Se activará cuando se integre IA
        self.ai_provider = None
    
    def analyze_content(self, post_data: dict) -> Dict[str, any]:
        """
        Analiza el contenido y retorna sugerencias SEO
        En el futuro, esto se potenciará con IA
        """
        analysis = {
            'score': 0,
            'max_score': 100,
            'issues': [],
            'suggestions': [],
            'ai_suggestions': [],  # Para futuras sugerencias de IA
        }
        
        # Análisis del título
        title_analysis = self._analyze_title(post_data.get('title', ''))
        analysis['score'] += title_analysis['score']
        analysis['issues'].extend(title_analysis['issues'])
        analysis['suggestions'].extend(title_analysis['suggestions'])
        
        # Análisis del slug
        slug_analysis = self._analyze_slug(post_data.get('slug', ''))
        analysis['score'] += slug_analysis['score']
        analysis['issues'].extend(slug_analysis['issues'])
        
        # Análisis de meta descripción
        desc_analysis = self._analyze_meta_description(post_data.get('seo_description', ''))
        analysis['score'] += desc_analysis['score']
        analysis['issues'].extend(desc_analysis['issues'])
        analysis['suggestions'].extend(desc_analysis['suggestions'])
        
        # Análisis de keywords
        keywords_analysis = self._analyze_keywords(
            post_data.get('seo_keywords', ''),
            post_data.get('content', '')
        )
        analysis['score'] += keywords_analysis['score']
        analysis['issues'].extend(keywords_analysis['issues'])
        
        # Análisis del contenido
        content_analysis = self._analyze_content_quality(post_data.get('content', ''))
        analysis['score'] += content_analysis['score']
        analysis['issues'].extend(content_analysis['issues'])
        analysis['suggestions'].extend(content_analysis['suggestions'])
        
        # Hook para IA (futuro)
        if self.ai_enabled and self.ai_provider:
            ai_suggestions = self._get_ai_suggestions(post_data)
            analysis['ai_suggestions'] = ai_suggestions
        
        return analysis
    
    def _analyze_title(self, title: str) -> dict:
        """Analiza el título del post"""
        result = {'score': 0, 'issues': [], 'suggestions': []}
        
        if not title:
            result['issues'].append("❌ El título está vacío")
            return result
        
        title_len = len(title)
        
        if title_len < 30:
            result['issues'].append(f"⚠️ Título muy corto ({title_len} caracteres). Recomendado: 30-60")
            result['suggestions'].append("Amplía el título para incluir más palabras clave relevantes")
            result['score'] += 5
        elif title_len > 60:
            result['issues'].append(f"⚠️ Título muy largo ({title_len} caracteres). Puede cortarse en resultados de búsqueda")
            result['suggestions'].append("Acorta el título a 60 caracteres o menos")
            result['score'] += 10
        else:
            result['score'] += 20
        
        # Verificar si tiene números (mejora CTR)
        if re.search(r'\d+', title):
            result['score'] += 5
        else:
            result['suggestions'].append("Considera agregar números al título (ej: '10 formas de...')")
        
        return result
    
    def _analyze_slug(self, slug: str) -> dict:
        """Analiza el slug/URL"""
        result = {'score': 0, 'issues': []}
        
        if not slug:
            result['issues'].append("❌ El slug está vacío")
            return result
        
        if len(slug) > 75:
            result['issues'].append(f"⚠️ Slug muy largo ({len(slug)} caracteres). Máximo recomendado: 75")
            result['score'] += 5
        else:
            result['score'] += 15
        
        # Verificar caracteres especiales
        if re.search(r'[^a-z0-9-]', slug):
            result['issues'].append("⚠️ El slug contiene caracteres no recomendados")
            result['score'] += 5
        else:
            result['score'] += 10
        
        return result
    
    def _analyze_meta_description(self, description: str) -> dict:
        """Analiza la meta descripción"""
        result = {'score': 0, 'issues': [], 'suggestions': []}
        
        if not description:
            result['issues'].append("❌ La meta descripción está vacía")
            result['suggestions'].append("Agrega una descripción atractiva de 120-160 caracteres")
            return result
        
        desc_len = len(description)
        
        if desc_len < 120:
            result['issues'].append(f"⚠️ Meta descripción muy corta ({desc_len} caracteres)")
            result['suggestions'].append("Amplía la descripción a 120-160 caracteres para mejor visibilidad")
            result['score'] += 10
        elif desc_len > 160:
            result['issues'].append(f"⚠️ Meta descripción muy larga ({desc_len} caracteres). Se cortará en resultados")
            result['suggestions'].append("Acorta la descripción a 160 caracteres o menos")
            result['score'] += 10
        else:
            result['score'] += 20
        
        # Verificar call-to-action
        cta_words = ['descubre', 'aprende', 'conoce', 'lee', 'encuentra', 'explora']
        if any(word in description.lower() for word in cta_words):
            result['score'] += 5
        else:
            result['suggestions'].append("Considera agregar un call-to-action (descubre, aprende, etc.)")
        
        return result
    
    def _analyze_keywords(self, keywords: str, content: str) -> dict:
        """Analiza las keywords"""
        result = {'score': 0, 'issues': []}
        
        if not keywords:
            result['issues'].append("⚠️ No hay keywords definidas")
            result['score'] += 5
            return result
        
        keywords_list = [k.strip() for k in keywords.split(',') if k.strip()]
        
        if len(keywords_list) > 10:
            result['issues'].append(f"⚠️ Demasiadas keywords ({len(keywords_list)}). Recomendado: 5-10")
            result['score'] += 5
        elif len(keywords_list) < 3:
            result['issues'].append(f"⚠️ Pocas keywords ({len(keywords_list)}). Recomendado: 5-10")
            result['score'] += 10
        else:
            result['score'] += 15
        
        # Verificar si las keywords están en el contenido
        content_lower = content.lower()
        keywords_in_content = sum(1 for kw in keywords_list if kw.lower() in content_lower)
        
        if keywords_in_content < len(keywords_list) * 0.7:
            result['issues'].append("⚠️ Algunas keywords no aparecen en el contenido")
            result['score'] += 5
        else:
            result['score'] += 10
        
        return result
    
    def _analyze_content_quality(self, content: str) -> dict:
        """Analiza la calidad del contenido"""
        result = {'score': 0, 'issues': [], 'suggestions': []}
        
        if not content:
            result['issues'].append("❌ El contenido está vacío")
            return result
        
        # Contar palabras (aproximado, sin HTML)
        text_content = re.sub(r'<[^>]+>', '', content)
        words = len(text_content.split())
        
        if words < 300:
            result['issues'].append(f"⚠️ Contenido muy corto ({words} palabras). Mínimo recomendado: 300")
            result['suggestions'].append("Amplía el contenido para mejorar el SEO")
            result['score'] += 5
        elif words < 600:
            result['score'] += 10
            result['suggestions'].append("Buen inicio. Contenido de 1000+ palabras tiene mejor ranking")
        else:
            result['score'] += 15
        
        # Verificar encabezados
        h_tags = len(re.findall(r'<h[1-6]>', content, re.IGNORECASE))
        if h_tags == 0:
            result['issues'].append("⚠️ No hay encabezados (H1-H6) en el contenido")
            result['suggestions'].append("Agrega encabezados para mejorar la estructura")
            result['score'] += 5
        else:
            result['score'] += 10
        
        # Verificar imágenes
        images = len(re.findall(r'<img', content, re.IGNORECASE))
        if images == 0:
            result['suggestions'].append("Considera agregar imágenes para mejorar el engagement")
        else:
            result['score'] += 5
        
        return result
    
    def _get_ai_suggestions(self, post_data: dict) -> List[dict]:
        """
        Obtiene sugerencias de IA (placeholder para futura implementación)
        
        En el futuro, esto llamará a:
        - OpenAI GPT para optimización de títulos
        - Análisis semántico de keywords
        - Sugerencias de contenido relacionado
        - Optimización de meta descripciones
        """
        # Placeholder - se implementará cuando se integre KardoAI
        return [
            {
                'type': 'ai_suggestion',
                'category': 'title',
                'message': '🤖 IA: Sugerencias disponibles próximamente',
                'confidence': 0.0
            }
        ]
    
    def generate_slug_suggestions(self, title: str, count: int = 3) -> List[str]:
        """
        Genera sugerencias de slug
        En el futuro, la IA generará variaciones optimizadas
        """
        base_slug = self._slugify(title)
        suggestions = [base_slug]
        
        # Variación corta
        words = base_slug.split('-')
        if len(words) > 3:
            short_slug = '-'.join(words[:4])
            suggestions.append(short_slug)
        
        # Variación con keyword principal
        if len(words) > 1:
            keyword_slug = '-'.join(words[:2])
            suggestions.append(keyword_slug)
        
        return suggestions[:count]
    
    def _slugify(self, text: str) -> str:
        """Convierte texto a slug SEO-friendly"""
        slug = text.lower()
        
        # Caracteres especiales
        replacements = {
            'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
            'ñ': 'n', 'ü': 'u',
        }
        for old, new in replacements.items():
            slug = slug.replace(old, new)
        
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        
        return slug
    
    def generate_meta_description(self, content: str, max_length: int = 155) -> str:
        """
        Genera una meta descripción desde el contenido
        En el futuro, la IA creará descripciones optimizadas
        """
        # Limpiar HTML
        text = re.sub(r'<[^>]+>', '', content)
        text = text.strip()
        
        if len(text) <= max_length:
            return text
        
        # Cortar en la última palabra completa
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > 0:
            truncated = truncated[:last_space]
        
        return truncated + '...'
    
    def extract_keywords(self, title: str, content: str, count: int = 5) -> List[str]:
        """
        Extrae keywords relevantes
        En el futuro, la IA usará NLP para extraer keywords semánticas
        """
        # Limpiar HTML
        text = re.sub(r'<[^>]+>', '', content).lower()
        text = f"{title.lower()} {text}"
        
        # Palabras comunes a ignorar
        stop_words = {
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no', 'haber',
            'por', 'con', 'su', 'para', 'como', 'estar', 'tener', 'le', 'lo', 'todo',
            'pero', 'más', 'hacer', 'o', 'poder', 'decir', 'este', 'ir', 'otro', 'ese',
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it', 'for',
            'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his'
        }
        
        # Extraer palabras
        words = re.findall(r'\b[a-záéíóúñ]{4,}\b', text)
        
        # Contar frecuencia
        word_freq = {}
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Ordenar por frecuencia
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        # Retornar top keywords
        return [word for word, freq in sorted_words[:count]]


class SEOOptimizer:
    """
    Optimizador SEO con hooks para IA
    """
    
    def __init__(self):
        self.analyzer = SEOAnalyzer()
    
    async def optimize_post(self, post_data: dict, use_ai: bool = False) -> dict:
        """
        Optimiza un post para SEO
        
        Args:
            post_data: Datos del post
            use_ai: Si se debe usar IA para optimización (futuro)
        
        Returns:
            dict con sugerencias y datos optimizados
        """
        optimizations = {
            'original': post_data.copy(),
            'optimized': post_data.copy(),
            'changes': [],
            'analysis': self.analyzer.analyze_content(post_data)
        }
        
        # Optimizar slug si está vacío o es genérico
        if not post_data.get('slug') or post_data['slug'] == 'untitled':
            new_slug = self.analyzer._slugify(post_data.get('title', ''))
            optimizations['optimized']['slug'] = new_slug
            optimizations['changes'].append({
                'field': 'slug',
                'old': post_data.get('slug'),
                'new': new_slug,
                'reason': 'Generado desde el título'
            })
        
        # Generar meta descripción si está vacía
        if not post_data.get('seo_description'):
            new_desc = self.analyzer.generate_meta_description(post_data.get('content', ''))
            optimizations['optimized']['seo_description'] = new_desc
            optimizations['changes'].append({
                'field': 'seo_description',
                'old': '',
                'new': new_desc,
                'reason': 'Generada desde el contenido'
            })
        
        # Extraer keywords si están vacías
        if not post_data.get('seo_keywords'):
            keywords = self.analyzer.extract_keywords(
                post_data.get('title', ''),
                post_data.get('content', '')
            )
            new_keywords = ', '.join(keywords)
            optimizations['optimized']['seo_keywords'] = new_keywords
            optimizations['changes'].append({
                'field': 'seo_keywords',
                'old': '',
                'new': new_keywords,
                'reason': 'Extraídas del contenido'
            })
        
        # Hook para IA (futuro)
        if use_ai:
            # Aquí se llamará a KardoAI para optimizaciones avanzadas
            optimizations['ai_optimizations'] = {
                'available': False,
                'message': 'Optimización IA disponible próximamente'
            }
        
        return optimizations


# Instancia global
seo_optimizer = SEOOptimizer()

