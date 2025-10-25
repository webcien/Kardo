"""
XSS (Cross-Site Scripting) Prevention

Auto-escaping and sanitization utilities.
"""

import html
import re
from typing import Any, Dict


class XSSProtection:
    """
    XSS Protection Utilities
    
    HTML escaping and sanitization.
    """
    
    # Dangerous HTML tags
    DANGEROUS_TAGS = [
        'script', 'iframe', 'object', 'embed', 'applet',
        'meta', 'link', 'style', 'base'
    ]
    
    # Dangerous attributes
    DANGEROUS_ATTRS = [
        'onclick', 'onload', 'onerror', 'onmouseover',
        'onfocus', 'onblur', 'onchange', 'onsubmit'
    ]
    
    @staticmethod
    def escape(text: str) -> str:
        """
        Escape HTML special characters
        
        Args:
            text: Input text
            
        Returns:
            HTML-escaped text
        """
        return html.escape(text)
        
    @staticmethod
    def escape_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively escape all strings in dict
        
        Args:
            data: Input dictionary
            
        Returns:
            Dictionary with escaped strings
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = html.escape(value)
            elif isinstance(value, dict):
                result[key] = XSSProtection.escape_dict(value)
            elif isinstance(value, list):
                result[key] = [
                    html.escape(v) if isinstance(v, str) else v
                    for v in value
                ]
            else:
                result[key] = value
        return result
        
    @classmethod
    def sanitize_html(cls, html_content: str) -> str:
        """
        Remove dangerous HTML tags and attributes
        
        Args:
            html_content: HTML string
            
        Returns:
            Sanitized HTML
        """
        # Remove dangerous tags
        for tag in cls.DANGEROUS_TAGS:
            pattern = f'<{tag}[^>]*>.*?</{tag}>'
            html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE | re.DOTALL)
            
        # Remove dangerous attributes
        for attr in cls.DANGEROUS_ATTRS:
            pattern = f'{attr}="[^"]*"'
            html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE)
            
        return html_content
        
    @staticmethod
    def add_csp_headers(response: Dict) -> Dict:
        """
        Add Content Security Policy headers
        
        Args:
            response: Response dict
            
        Returns:
            Response with CSP headers
        """
        if "headers" not in response:
            response["headers"] = {}
            
        # Strict CSP
        response["headers"]["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self'; "
            "frame-ancestors 'none';"
        )
        
        # Additional security headers
        response["headers"]["X-Content-Type-Options"] = "nosniff"
        response["headers"]["X-Frame-Options"] = "DENY"
        response["headers"]["X-XSS-Protection"] = "1; mode=block"
        
        return response
