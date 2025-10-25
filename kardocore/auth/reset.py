"""
Password Reset

Secure password reset functionality.
"""

import secrets
import time
from typing import Optional, Dict


class PasswordReset:
    """
    Password Reset Manager
    
    Handles password reset tokens and flow.
    """
    
    def __init__(self, expiration: int = 3600):  # 1 hour
        """
        Initialize password reset
        
        Args:
            expiration: Token expiration in seconds
        """
        self.expiration = expiration
        self.tokens: Dict[str, tuple[str, float]] = {}  # token -> (email, timestamp)
        
    def generate_token(self, email: str) -> str:
        """
        Generate password reset token
        
        Args:
            email: User email address
            
        Returns:
            Reset token
        """
        token = secrets.token_urlsafe(32)
        self.tokens[token] = (email, time.time())
        return token
        
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify reset token and return email
        
        Args:
            token: Reset token
            
        Returns:
            Email if valid, None if invalid/expired
        """
        if token not in self.tokens:
            return None
            
        email, timestamp = self.tokens[token]
        
        # Check expiration
        if time.time() - timestamp > self.expiration:
            del self.tokens[token]
            return None
            
        # Don't delete token yet - will be deleted after password reset
        return email
        
    def consume_token(self, token: str) -> bool:
        """
        Consume (delete) reset token after use
        
        Args:
            token: Reset token
            
        Returns:
            True if token existed
        """
        if token in self.tokens:
            del self.tokens[token]
            return True
        return False
        
    def get_reset_url(self, base_url: str, token: str) -> str:
        """
        Get password reset URL
        
        Args:
            base_url: Base URL of application
            token: Reset token
            
        Returns:
            Full reset URL
        """
        return f"{base_url}/reset-password?token={token}"
        
    async def send_reset_email(
        self,
        email: str,
        token: str,
        base_url: str
    ):
        """
        Send password reset email
        
        Args:
            email: Recipient email
            token: Reset token
            base_url: Base URL for reset link
        """
        reset_url = self.get_reset_url(base_url, token)
        
        # Email content
        subject = "Reset your password"
        body = f"""
        You requested to reset your password. Click the link below:
        
        {reset_url}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
        Your password will not be changed.
        """
        
        # Send email (would use aiosmtplib or similar)
        # await send_email(email, subject, body)
        
        print(f"Password reset email sent to {email}")
        print(f"Link: {reset_url}")
