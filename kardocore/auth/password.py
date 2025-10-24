"""
Password hashing and verification for KardoCore.

Supports:
- Bcrypt (recommended)
- Argon2 (most secure)
- PBKDF2 (fallback)

Philosophy: Secure by default
"""

import hashlib
import secrets
from typing import Optional
from enum import Enum


class HashAlgorithm(Enum):
    """Supported password hashing algorithms"""
    BCRYPT = "bcrypt"
    ARGON2 = "argon2"
    PBKDF2 = "pbkdf2"


class PasswordHasher:
    """
    Secure password hashing.
    
    Features:
    - Multiple algorithms (bcrypt, argon2, pbkdf2)
    - Automatic salt generation
    - Timing-attack resistant verification
    - Password strength validation
    
    Example:
        hasher = PasswordHasher()
        
        # Hash password
        hashed = hasher.hash("my_password")
        
        # Verify password
        is_valid = hasher.verify("my_password", hashed)
    """
    
    def __init__(self, algorithm: HashAlgorithm = HashAlgorithm.BCRYPT):
        self.algorithm = algorithm
    
    def hash(self, password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        if self.algorithm == HashAlgorithm.BCRYPT:
            return self._hash_bcrypt(password)
        elif self.algorithm == HashAlgorithm.ARGON2:
            return self._hash_argon2(password)
        else:
            return self._hash_pbkdf2(password)
    
    def verify(self, password: str, hashed: str) -> bool:
        """
        Verify a password against a hash.
        
        Args:
            password: Plain text password
            hashed: Hashed password
            
        Returns:
            True if password matches
        """
        # Detect algorithm from hash prefix
        if hashed.startswith("$2b$") or hashed.startswith("$2a$"):
            return self._verify_bcrypt(password, hashed)
        elif hashed.startswith("$argon2"):
            return self._verify_argon2(password, hashed)
        else:
            return self._verify_pbkdf2(password, hashed)
    
    def _hash_bcrypt(self, password: str) -> str:
        """Hash with bcrypt"""
        try:
            import bcrypt
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode(), salt).decode()
        except ImportError:
            # Fallback to PBKDF2 if bcrypt not available
            return self._hash_pbkdf2(password)
    
    def _verify_bcrypt(self, password: str, hashed: str) -> bool:
        """Verify bcrypt hash"""
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode(), hashed.encode())
        except ImportError:
            return False
    
    def _hash_argon2(self, password: str) -> str:
        """Hash with argon2"""
        try:
            from argon2 import PasswordHasher as Argon2Hasher
            ph = Argon2Hasher()
            return ph.hash(password)
        except ImportError:
            # Fallback to PBKDF2
            return self._hash_pbkdf2(password)
    
    def _verify_argon2(self, password: str, hashed: str) -> bool:
        """Verify argon2 hash"""
        try:
            from argon2 import PasswordHasher as Argon2Hasher
            from argon2.exceptions import VerifyMismatchError
            ph = Argon2Hasher()
            try:
                ph.verify(hashed, password)
                return True
            except VerifyMismatchError:
                return False
        except ImportError:
            return False
    
    def _hash_pbkdf2(self, password: str) -> str:
        """Hash with PBKDF2 (fallback)"""
        salt = secrets.token_bytes(32)
        iterations = 100000
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            iterations
        )
        # Format: pbkdf2$iterations$salt$hash
        return f"pbkdf2${iterations}${salt.hex()}${key.hex()}"
    
    def _verify_pbkdf2(self, password: str, hashed: str) -> bool:
        """Verify PBKDF2 hash"""
        try:
            parts = hashed.split('$')
            if len(parts) != 4 or parts[0] != 'pbkdf2':
                return False
            
            iterations = int(parts[1])
            salt = bytes.fromhex(parts[2])
            stored_key = parts[3]
            
            key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                iterations
            )
            
            return secrets.compare_digest(key.hex(), stored_key)
        except Exception:
            return False
    
    @staticmethod
    def validate_strength(
        password: str,
        min_length: int = 8,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digit: bool = True,
        require_special: bool = True
    ) -> tuple[bool, list[str]]:
        """
        Validate password strength.
        
        Returns:
            (is_valid, list_of_errors)
        """
        errors = []
        
        if len(password) < min_length:
            errors.append(f"Password must be at least {min_length} characters")
        
        if require_uppercase and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if require_lowercase and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if require_digit and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        if require_special and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
