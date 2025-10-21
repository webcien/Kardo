"""
Tokenizador de KardoTheme

Convierte el código de plantilla en tokens para su posterior procesamiento.
Soporta la sintaxis expresiva de KardoTheme con prefijo # para bloques.
"""

from enum import Enum
from typing import List, Optional
from dataclasses import dataclass


class TokenType(Enum):
    """Tipos de tokens en KardoTheme."""
    HTML = "HTML"              # HTML literal
    EXPR = "EXPR"              # Expresión dinámica {variable}
    FOR = "FOR"                # Bloque #for
    IF = "IF"                  # Bloque #if
    ELIF = "ELIF"              # Bloque #elif
    ELSE = "ELSE"              # Bloque #else
    END = "END"                # Cierre de bloque #end
    COMPONENT = "COMPONENT"    # Componente #component
    INCLUDE = "INCLUDE"        # Inclusión #include
    COMMENT = "COMMENT"        # Comentario {# ... #}


@dataclass
class Token:
    """Representa un token en la plantilla."""
    type: TokenType
    value: str
    line: int
    column: int


class KardoThemeTokenizer:
    """
    Tokenizador para el motor de plantillas KardoTheme.
    
    Convierte el código de plantilla en una lista de tokens que pueden
    ser procesados por el parser y el renderizador.
    """
    
    def __init__(self, template: str):
        """
        Inicializa el tokenizador.
        
        Args:
            template: Código de la plantilla a tokenizar
        """
        self.template = template
        self.tokens: List[Token] = []
        self.current_line = 1
        self.current_column = 1
    
    def tokenize(self) -> List[Token]:
        """
        Tokeniza la plantilla completa.
        
        Returns:
            Lista de tokens
        """
        lines = self.template.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            self.current_line = line_num
            self.current_column = 1
            self._tokenize_line(line)
        
        return self.tokens
    
    def _tokenize_line(self, line: str) -> None:
        """
        Tokeniza una línea de la plantilla.
        
        Args:
            line: Línea a tokenizar
        """
        stripped = line.lstrip()
        
        # Detectar bloques de control (comienzan con #)
        if stripped.startswith('#'):
            self._tokenize_control_block(stripped)
        # Detectar expresiones dinámicas {variable}
        elif '{' in line and '}' in line:
            self._tokenize_mixed_line(line)
        # HTML literal
        else:
            if line.strip():  # Ignorar líneas vacías
                self.tokens.append(Token(
                    type=TokenType.HTML,
                    value=line,
                    line=self.current_line,
                    column=self.current_column
                ))
    
    def _tokenize_control_block(self, line: str) -> None:
        """
        Tokeniza un bloque de control (#for, #if, etc.).
        
        Args:
            line: Línea que contiene el bloque de control
        """
        # Remover el # inicial
        line = line[1:].strip()
        
        # Detectar tipo de bloque
        if line.startswith('for '):
            # #for item in items
            value = line[4:].strip()
            self.tokens.append(Token(
                type=TokenType.FOR,
                value=value,
                line=self.current_line,
                column=self.current_column
            ))
        
        elif line.startswith('if '):
            # #if condition
            value = line[3:].strip()
            self.tokens.append(Token(
                type=TokenType.IF,
                value=value,
                line=self.current_line,
                column=self.current_column
            ))
        
        elif line.startswith('elif '):
            # #elif condition
            value = line[5:].strip()
            self.tokens.append(Token(
                type=TokenType.ELIF,
                value=value,
                line=self.current_line,
                column=self.current_column
            ))
        
        elif line == 'else':
            # #else
            self.tokens.append(Token(
                type=TokenType.ELSE,
                value='',
                line=self.current_line,
                column=self.current_column
            ))
        
        elif line == 'end':
            # #end
            self.tokens.append(Token(
                type=TokenType.END,
                value='',
                line=self.current_line,
                column=self.current_column
            ))
        
        elif line.startswith('component '):
            # #component nombre with data
            value = line[10:].strip()
            self.tokens.append(Token(
                type=TokenType.COMPONENT,
                value=value,
                line=self.current_line,
                column=self.current_column
            ))
        
        elif line.startswith('include '):
            # #include "template.html"
            value = line[8:].strip()
            self.tokens.append(Token(
                type=TokenType.INCLUDE,
                value=value,
                line=self.current_line,
                column=self.current_column
            ))
        
        else:
            # Bloque desconocido, tratarlo como HTML
            self.tokens.append(Token(
                type=TokenType.HTML,
                value=f"#{line}",
                line=self.current_line,
                column=self.current_column
            ))
    
    def _tokenize_mixed_line(self, line: str) -> None:
        """
        Tokeniza una línea que contiene HTML y expresiones dinámicas.
        
        Args:
            line: Línea mixta
        """
        parts = []
        current = ""
        i = 0
        
        while i < len(line):
            # Detectar inicio de expresión
            if line[i] == '{' and i + 1 < len(line):
                # Verificar si es comentario {# ... #}
                if line[i + 1] == '#':
                    # Buscar cierre de comentario
                    end = line.find('#}', i + 2)
                    if end != -1:
                        # Ignorar comentario
                        i = end + 2
                        continue
                
                # Guardar HTML acumulado
                if current:
                    self.tokens.append(Token(
                        type=TokenType.HTML,
                        value=current,
                        line=self.current_line,
                        column=self.current_column
                    ))
                    current = ""
                
                # Buscar cierre de expresión
                end = line.find('}', i + 1)
                if end != -1:
                    expr = line[i + 1:end]
                    self.tokens.append(Token(
                        type=TokenType.EXPR,
                        value=expr,
                        line=self.current_line,
                        column=i + 1
                    ))
                    i = end + 1
                else:
                    # No hay cierre, tratar como HTML
                    current += line[i]
                    i += 1
            else:
                current += line[i]
                i += 1
        
        # Guardar HTML restante
        if current:
            self.tokens.append(Token(
                type=TokenType.HTML,
                value=current,
                line=self.current_line,
                column=self.current_column
            ))
    
    def validate(self) -> List[str]:
        """
        Valida que los bloques estén correctamente balanceados.
        
        Returns:
            Lista de errores de validación
        """
        errors = []
        stack = []
        
        for token in self.tokens:
            if token.type in [TokenType.FOR, TokenType.IF]:
                stack.append((token.type, token.line))
            
            elif token.type == TokenType.END:
                if not stack:
                    errors.append(f"Line {token.line}: #end sin bloque de apertura")
                else:
                    stack.pop()
            
            elif token.type in [TokenType.ELIF, TokenType.ELSE]:
                if not stack or stack[-1][0] != TokenType.IF:
                    errors.append(f"Line {token.line}: #{token.type.value.lower()} fuera de bloque #if")
        
        # Verificar bloques sin cerrar
        for block_type, line in stack:
            errors.append(f"Line {line}: Bloque #{block_type.value.lower()} sin cerrar")
        
        return errors

