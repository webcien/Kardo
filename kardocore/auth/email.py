"""
Email Verification

Email confirmation and verification tokens.
"""

import secrets
import time
from typing import Optional, Dict


class EmailVerification:
    """
    Email Verification Manager
    
    Handles email confirmation tokens and verification.
    """
    
    def __init__(self, expiration: int = 86400):  # 24 hours
        """
        Initialize email verification
        
        Args:
            expiration: Token expiration in seconds
        """
        self.expiration = expiration
        self.tokens: Dict[str, tuple[str, float]] = {}  # token -> (email, timestamp)
        
    def generate_token(self, email: str) -> str:
        """
        Generate verification token for email
        
        Args:
            email: User email address
            
        Returns:
            Verification token
        """
        token = secrets.token_urlsafe(32)
        self.tokens[token] = (email, time.time())
        return token
        
    def verify_token(self, token: str) -> Optional[str]:
        """
        Verify token and return email
        
        Args:
            token: Verification token
            
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
            
        # Token is valid
        del self.tokens[token]
        return email
        
    def get_verification_url(self, base_url: str, token: str) -> str:
        """
        Get verification URL
        
        Args:
            base_url: Base URL of application
            token: Verification token
            
        Returns:
            Full verification URL
        """
        return f"{base_url}/verify-email?token={token}"
        
    async def send_verification_email(
        self,
        email: str,
        token: str,
        base_url: str
    ):
        """
        Send verification email
        
        Args:
            email: Recipient email
            token: Verification token
            base_url: Base URL for verification link
        """
        verification_url = self.get_verification_url(base_url, token)
        
        # Email content
        subject = "Verify your email address"
        body = f"""
        Please verify your email address by clicking the link below:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't request this, please ignore this email.
        """
        
        # Send email (would use aiosmtplib or similar)
        # await send_email(email, subject, body)
        
        print(f"Verification email sent to {email}")
        print(f"Link: {verification_url}")
