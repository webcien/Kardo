"""
Renderizador de KardoTheme

Procesa tokens y genera HTML final con sandboxing y escape automático.
"""

import html
from typing import Any, Dict, List
from kardocore.theme.tokenizer import Token, TokenType


class RenderError(Exception):
    """Excepción lanzada cuando hay un error de renderizado."""
    pass


class SafeContext:
    """
    Contexto seguro para evaluación de expresiones.
    
    Proporciona acceso controlado a variables sin permitir
    ejecución arbitraria de código Python.
    """
    
    def __init__(self, data: Dict[str, Any]):
        """
        Inicializa el contexto.
        
        Args:
            data: Diccionario de variables disponibles
        """
        self._data = data
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Obtiene un valor del contexto usando notación de punto.
        
        Args:
            path: Path de la variable (ej: "user.name")
            default: Valor por defecto si no existe
        
        Returns:
            Valor de la variable
        """
        parts = path.split('.')
        value = self._data
        
        for part in parts:
            if isinstance(value, dict):
                value = value.get(part)
            elif hasattr(value, part):
                value = getattr(value, part)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def evaluate(self, expr: str) -> Any:
        """
        Evalúa una expresión de forma segura.
        
        Args:
            expr: Expresión a evaluar
        
        Returns:
            Resultado de la evaluación
        """
        expr = expr.strip()
        
        # Soportar operadores simples
        # TODO: Implementar parser de expresiones más robusto
        
        # Por ahora, solo soportar acceso a variables
        return self.get(expr, '')


class KardoThemeRenderer:
    """
    Renderizador de plantillas KardoTheme.
    
    Procesa tokens y genera HTML final con escape automático
    y sandboxing de seguridad.
    """
    
    def __init__(self, tokens: List[Token], context: Dict[str, Any]):
        """
        Inicializa el renderizador.
        
        Args:
            tokens: Lista de tokens a renderizar
            context: Contexto de variables
        """
        self.tokens = tokens
        self.context = SafeContext(context)
        self.output: List[str] = []
        self.current_index = 0
    
    def render(self) -> str:
        """
        Renderiza la plantilla completa.
        
        Returns:
            HTML renderizado
        """
        self.output = []
        self.current_index = 0
        
        while self.current_index < len(self.tokens):
            self._render_token(self.tokens[self.current_index])
            self.current_index += 1
        
        return ''.join(self.output)
    
    def _render_token(self, token: Token) -> None:
        """
        Renderiza un token individual.
        
        Args:
            token: Token a renderizar
        """
        if token.type == TokenType.HTML:
            self.output.append(token.value)
        
        elif token.type == TokenType.EXPR:
            value = self.context.evaluate(token.value)
            # Escape automático para prevenir XSS
            self.output.append(html.escape(str(value)))
        
        elif token.type == TokenType.FOR:
            self._render_for_loop(token)
        
        elif token.type == TokenType.IF:
            self._render_if_block(token)
        
        elif token.type == TokenType.COMPONENT:
            self._render_component(token)
        
        elif token.type == TokenType.INCLUDE:
            self._render_include(token)
    
    def _render_for_loop(self, token: Token) -> None:
        """
        Renderiza un bucle #for.
        
        Args:
            token: Token FOR
        """
        # Parsear expresión: "item in items"
        parts = token.value.split(' in ')
        if len(parts) != 2:
            raise RenderError(f"Line {token.line}: Sintaxis inválida en #for")
        
        var_name = parts[0].strip()
        iterable_expr = parts[1].strip()
        
        # Obtener iterable del contexto
        iterable = self.context.evaluate(iterable_expr)
        
        if not hasattr(iterable, '__iter__'):
            raise RenderError(f"Line {token.line}: {iterable_expr} no es iterable")
        
        # Encontrar tokens del cuerpo del bucle (hasta #end)
        body_tokens = self._extract_block_tokens()
        
        # Renderizar para cada elemento
        for item in iterable:
            # Crear nuevo contexto con la variable del bucle
            loop_context = self.context._data.copy()
            loop_context[var_name] = item
            
            # Renderizar cuerpo del bucle
            renderer = KardoThemeRenderer(body_tokens, loop_context)
            self.output.append(renderer.render())
    
    def _render_if_block(self, token: Token) -> None:
        """
        Renderiza un bloque condicional #if.
        
        Args:
            token: Token IF
        """
        # Evaluar condición
        condition = self.context.evaluate(token.value)
        
        # Extraer bloques if/elif/else
        blocks = self._extract_conditional_blocks()
        
        # Determinar qué bloque renderizar
        if condition:
            # Renderizar bloque if
            renderer = KardoThemeRenderer(blocks['if'], self.context._data)
            self.output.append(renderer.render())
        else:
            # Verificar elif
            rendered = False
            for elif_condition, elif_tokens in blocks.get('elif', []):
                if self.context.evaluate(elif_condition):
                    renderer = KardoThemeRenderer(elif_tokens, self.context._data)
                    self.output.append(renderer.render())
                    rendered = True
                    break
            
            # Si no se renderizó ningún elif, renderizar else
            if not rendered and 'else' in blocks:
                renderer = KardoThemeRenderer(blocks['else'], self.context._data)
                self.output.append(renderer.render())
    
    def _render_component(self, token: Token) -> None:
        """
        Renderiza un componente.
        
        Args:
            token: Token COMPONENT
        """
        # TODO: Implementar sistema de componentes
        # Por ahora, solo un placeholder
        self.output.append(f"<!-- Component: {token.value} -->")
    
    def _render_include(self, token: Token) -> None:
        """
        Renderiza una inclusión de plantilla.
        
        Args:
            token: Token INCLUDE
        """
        # TODO: Implementar sistema de includes
        # Por ahora, solo un placeholder
        self.output.append(f"<!-- Include: {token.value} -->")
    
    def _extract_block_tokens(self) -> List[Token]:
        """
        Extrae tokens de un bloque hasta encontrar #end.
        
        Returns:
            Lista de tokens del bloque
        """
        block_tokens = []
        depth = 1
        self.current_index += 1
        
        while self.current_index < len(self.tokens) and depth > 0:
            token = self.tokens[self.current_index]
            
            if token.type in [TokenType.FOR, TokenType.IF]:
                depth += 1
                block_tokens.append(token)
            elif token.type == TokenType.END:
                depth -= 1
                if depth > 0:
                    block_tokens.append(token)
            else:
                block_tokens.append(token)
            
            self.current_index += 1
        
        return block_tokens
    
    def _extract_conditional_blocks(self) -> Dict[str, Any]:
        """
        Extrae bloques de una estructura if/elif/else.
        
        Returns:
            Diccionario con bloques 'if', 'elif', 'else'
        """
        blocks = {'if': [], 'elif': [], 'else': []}
        current_block = 'if'
        depth = 1
        self.current_index += 1
        
        while self.current_index < len(self.tokens) and depth > 0:
            token = self.tokens[self.current_index]
            
            if token.type in [TokenType.FOR, TokenType.IF]:
                depth += 1
                if current_block == 'if':
                    blocks['if'].append(token)
                elif current_block == 'else':
                    blocks['else'].append(token)
            
            elif token.type == TokenType.ELIF and depth == 1:
                # Nuevo bloque elif
                current_block = 'elif'
                # Guardar condición y tokens del elif
                elif_condition = token.value
                elif_tokens = []
                blocks['elif'].append((elif_condition, elif_tokens))
            
            elif token.type == TokenType.ELSE and depth == 1:
                current_block = 'else'
            
            elif token.type == TokenType.END:
                depth -= 1
                if depth > 0:
                    if current_block == 'if':
                        blocks['if'].append(token)
                    elif current_block == 'else':
                        blocks['else'].append(token)
            
            else:
                if current_block == 'if':
                    blocks['if'].append(token)
                elif current_block == 'elif':
                    # Agregar a la última tupla elif
                    blocks['elif'][-1][1].append(token)
                elif current_block == 'else':
                    blocks['else'].append(token)
            
            self.current_index += 1
        
        return blocks

