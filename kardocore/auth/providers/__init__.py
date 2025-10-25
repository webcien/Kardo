"""
OAuth Providers
"""

from kardocore.auth.providers.google import GoogleOAuthProvider
from kardocore.auth.providers.github import GitHubOAuthProvider

__all__ = ["GoogleOAuthProvider", "GitHubOAuthProvider"]
