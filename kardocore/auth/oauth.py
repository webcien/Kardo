"""
OAuth Authentication Providers

Support for Google, GitHub, Facebook, and custom OAuth providers.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
import secrets
import time


@dataclass
class OAuthProvider:
    """OAuth provider configuration"""
    name: str
    client_id: str
    client_secret: str
    authorize_url: str
    token_url: str
    userinfo_url: str
    scope: str


class OAuth:
    """
    OAuth Authentication Manager
    
    Supports multiple OAuth providers.
    """
    
    def __init__(self, redirect_uri: str):
        self.redirect_uri = redirect_uri
        self.providers: Dict[str, OAuthProvider] = {}
        self.states: Dict[str, float] = {}  # state -> timestamp
        
    def register_provider(
        self,
        name: str,
        client_id: str,
        client_secret: str,
        authorize_url: str,
        token_url: str,
        userinfo_url: str,
        scope: str = "openid profile email"
    ):
        """Register an OAuth provider"""
        provider = OAuthProvider(
            name=name,
            client_id=client_id,
            client_secret=client_secret,
            authorize_url=authorize_url,
            token_url=token_url,
            userinfo_url=userinfo_url,
            scope=scope
        )
        self.providers[name] = provider
        
    def get_authorization_url(self, provider_name: str) -> tuple[str, str]:
        """
        Get authorization URL for OAuth flow
        
        Returns:
            (authorization_url, state)
        """
        provider = self.providers.get(provider_name)
        if not provider:
            raise ValueError(f"Unknown provider: {provider_name}")
            
        # Generate state for CSRF protection
        state = secrets.token_urlsafe(32)
        self.states[state] = time.time()
        
        # Build authorization URL
        params = {
            "client_id": provider.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": provider.scope,
            "state": state
        }
        
        query = "&".join(f"{k}={v}" for k, v in params.items())
        auth_url = f"{provider.authorize_url}?{query}"
        
        return auth_url, state
        
    async def exchange_code(
        self,
        provider_name: str,
        code: str,
        state: str
    ) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Returns:
            User info dict
        """
        # Verify state
        if state not in self.states:
            raise ValueError("Invalid state")
            
        # Check state expiration (5 minutes)
        if time.time() - self.states[state] > 300:
            del self.states[state]
            raise ValueError("State expired")
            
        del self.states[state]
        
        provider = self.providers[provider_name]
        
        # Exchange code for token
        # (Simplified - would use aiohttp in real implementation)
        token_data = {
            "code": code,
            "client_id": provider.client_id,
            "client_secret": provider.client_secret,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code"
        }
        
        # Get access token
        # access_token = await self._post(provider.token_url, token_data)
        
        # Get user info
        # user_info = await self._get(provider.userinfo_url, access_token)
        
        # Placeholder return
        return {
            "email": "user@example.com",
            "name": "User Name",
            "provider": provider_name
        }
        
    @classmethod
    def google(cls, client_id: str, client_secret: str, redirect_uri: str):
        """Create OAuth instance for Google"""
        oauth = cls(redirect_uri)
        oauth.register_provider(
            "google",
            client_id,
            client_secret,
            "https://accounts.google.com/o/oauth2/v2/auth",
            "https://oauth2.googleapis.com/token",
            "https://www.googleapis.com/oauth2/v2/userinfo",
            "openid profile email"
        )
        return oauth
        
    @classmethod
    def github(cls, client_id: str, client_secret: str, redirect_uri: str):
        """Create OAuth instance for GitHub"""
        oauth = cls(redirect_uri)
        oauth.register_provider(
            "github",
            client_id,
            client_secret,
            "https://github.com/login/oauth/authorize",
            "https://github.com/login/oauth/access_token",
            "https://api.github.com/user",
            "user:email"
        )
        return oauth
