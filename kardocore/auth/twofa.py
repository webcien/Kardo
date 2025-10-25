"""
Two-Factor Authentication (2FA)

TOTP-based 2FA support.
"""

import secrets
import time
import hmac
import hashlib
import base64
from typing import Optional


class TwoFactorAuth:
    """
    TOTP-based Two-Factor Authentication
    
    Compatible with Google Authenticator, Authy, etc.
    """
    
    @staticmethod
    def generate_secret() -> str:
        """Generate a new secret key for 2FA"""
        return base64.b32encode(secrets.token_bytes(20)).decode('utf-8')
        
    @staticmethod
    def get_totp_uri(secret: str, email: str, issuer: str = "KardoCore") -> str:
        """
        Get TOTP URI for QR code generation
        
        Args:
            secret: Base32 encoded secret
            email: User email
            issuer: App name
            
        Returns:
            otpauth:// URI
        """
        return f"otpauth://totp/{issuer}:{email}?secret={secret}&issuer={issuer}"
        
    @staticmethod
    def generate_totp(secret: str, time_step: int = 30) -> str:
        """
        Generate TOTP code
        
        Args:
            secret: Base32 encoded secret
            time_step: Time step in seconds (default 30)
            
        Returns:
            6-digit TOTP code
        """
        # Decode secret
        key = base64.b32decode(secret)
        
        # Get current time counter
        counter = int(time.time() / time_step)
        
        # Generate HMAC-SHA1
        counter_bytes = counter.to_bytes(8, 'big')
        hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
        
        # Dynamic truncation
        offset = hmac_hash[-1] & 0x0F
        code = int.from_bytes(hmac_hash[offset:offset+4], 'big') & 0x7FFFFFFF
        
        # Get 6-digit code
        return str(code % 1000000).zfill(6)
        
    @staticmethod
    def verify_totp(
        secret: str,
        code: str,
        window: int = 1,
        time_step: int = 30
    ) -> bool:
        """
        Verify TOTP code
        
        Args:
            secret: Base32 encoded secret
            code: User-provided code
            window: Number of time steps to check (±window)
            time_step: Time step in seconds
            
        Returns:
            True if code is valid
        """
        current_time = int(time.time() / time_step)
        
        # Check current and adjacent time windows
        for i in range(-window, window + 1):
            time_counter = current_time + i
            
            # Generate code for this time window
            key = base64.b32decode(secret)
            counter_bytes = time_counter.to_bytes(8, 'big')
            hmac_hash = hmac.new(key, counter_bytes, hashlib.sha1).digest()
            offset = hmac_hash[-1] & 0x0F
            expected_code = int.from_bytes(hmac_hash[offset:offset+4], 'big') & 0x7FFFFFFF
            expected_code = str(expected_code % 1000000).zfill(6)
            
            if secrets.compare_digest(code, expected_code):
                return True
                
        return False
        
    @staticmethod
    def generate_backup_codes(count: int = 10) -> list[str]:
        """
        Generate backup codes for 2FA recovery
        
        Args:
            count: Number of codes to generate
            
        Returns:
            List of backup codes
        """
        codes = []
        for _ in range(count):
            code = secrets.token_hex(4).upper()
            # Format as XXXX-XXXX
            formatted = f"{code[:4]}-{code[4:]}"
            codes.append(formatted)
        return codes
