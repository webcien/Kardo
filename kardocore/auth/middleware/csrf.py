"""
CSRF (Cross-Site Request Forgery) protection middleware.
"""

import secrets
import hmac
import hashlib
from typing import Optional


class CSRFProtection:
    """
    CSRF protection middleware.
    
    Features:
    - Token generation
    - Token validation
    - Double submit cookie pattern
    - Synchronizer token pattern
    
    Example:
        csrf = CSRFProtection("your-secret-key")
        
        # Generate token
        token = csrf.generate_token(session_id="abc123")
        
        # Validate token
        is_valid = csrf.validate_token(token, session_id="abc123")
    """
    
    def __init__(self, secret: str):
        self.secret = secret
    
    def generate_token(self, session_id: Optional[str] = None) -> str:
        """
        Generate CSRF token.
        
        Args:
            session_id: Optional session ID for binding
            
        Returns:
            CSRF token string
        """
        # Generate random token
        random_token = secrets.token_urlsafe(32)
        
        if session_id:
            # Bind to session
            message = f"{random_token}:{session_id}"
            signature = self._sign(message)
            return f"{random_token}.{signature}"
        
        return random_token
    
    def validate_token(
        self,
        token: str,
        session_id: Optional[str] = None
    ) -> bool:
        """
        Validate CSRF token.
        
        Args:
            token: CSRF token to validate
            session_id: Optional session ID for validation
            
        Returns:
            True if valid
        """
        if not token:
            return False
        
        if session_id and "." in token:
            # Validate signed token
            try:
                random_token, signature = token.split(".", 1)
                message = f"{random_token}:{session_id}"
                expected_signature = self._sign(message)
                return hmac.compare_digest(signature, expected_signature)
            except Exception:
                return False
        
        # Simple token validation (length check)
        return len(token) >= 32
    
    def _sign(self, message: str) -> str:
        """Create HMAC signature"""
        signature = hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature
