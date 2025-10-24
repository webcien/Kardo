"""
JWT (JSON Web Token) support for KardoCore.
"""

import json
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class JWT:
    """
    JWT token generation and verification.
    
    Features:
    - HS256 algorithm (HMAC with SHA-256)
    - Token expiration
    - Custom claims
    - Secure by default
    
    Example:
        jwt = JWT("your-secret-key")
        
        # Create token
        token = jwt.encode({"user_id": 1, "email": "john@example.com"})
        
        # Verify token
        payload = jwt.decode(token)
        if payload:
            print(f"User ID: {payload['user_id']}")
    """
    
    def __init__(self, secret: str, algorithm: str = "HS256"):
        self.secret = secret
        self.algorithm = algorithm
    
    def encode(
        self,
        payload: Dict[str, Any],
        expires_in: int = 3600  # 1 hour
    ) -> str:
        """
        Create JWT token.
        
        Args:
            payload: Token payload (claims)
            expires_in: Expiration time in seconds
            
        Returns:
            JWT token string
        """
        # Add standard claims
        now = datetime.utcnow()
        payload = payload.copy()
        payload["iat"] = int(now.timestamp())  # Issued at
        payload["exp"] = int((now + timedelta(seconds=expires_in)).timestamp())  # Expiration
        
        # Create header
        header = {
            "alg": self.algorithm,
            "typ": "JWT"
        }
        
        # Encode header and payload
        header_b64 = self._base64_encode(json.dumps(header))
        payload_b64 = self._base64_encode(json.dumps(payload))
        
        # Create signature
        message = f"{header_b64}.{payload_b64}"
        signature = self._sign(message)
        signature_b64 = self._base64_encode(signature)
        
        return f"{message}.{signature_b64}"
    
    def decode(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Payload dict if valid, None otherwise
        """
        try:
            # Split token
            parts = token.split(".")
            if len(parts) != 3:
                return None
            
            header_b64, payload_b64, signature_b64 = parts
            
            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            expected_signature = self._sign(message)
            actual_signature = self._base64_decode(signature_b64)
            
            if not hmac.compare_digest(expected_signature, actual_signature):
                return None
            
            # Decode payload
            payload_json = self._base64_decode(payload_b64)
            payload = json.loads(payload_json)
            
            # Check expiration
            if "exp" in payload:
                exp = payload["exp"]
                if datetime.utcnow().timestamp() > exp:
                    return None
            
            return payload
            
        except Exception:
            return None
    
    def _sign(self, message: str) -> bytes:
        """Create HMAC signature"""
        return hmac.new(
            self.secret.encode(),
            message.encode(),
            hashlib.sha256
        ).digest()
    
    def _base64_encode(self, data: str | bytes) -> str:
        """Base64 URL-safe encode"""
        if isinstance(data, str):
            data = data.encode()
        return base64.urlsafe_b64encode(data).decode().rstrip("=")
    
    def _base64_decode(self, data: str) -> bytes:
        """Base64 URL-safe decode"""
        # Add padding
        padding = 4 - (len(data) % 4)
        if padding != 4:
            data += "=" * padding
        return base64.urlsafe_b64decode(data)
