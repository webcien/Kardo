"""
Rate limiting middleware for preventing brute force attacks.
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
from collections import defaultdict


class RateLimiter:
    """
    Rate limiter for login attempts and API calls.
    
    Features:
    - Per-IP rate limiting
    - Per-user rate limiting
    - Configurable limits and windows
    - Automatic cleanup
    
    Example:
        limiter = RateLimiter(max_attempts=5, window=300)  # 5 attempts per 5 minutes
        
        # Check if allowed
        is_allowed, retry_after = limiter.is_allowed("192.168.1.1")
        if not is_allowed:
            print(f"Rate limited. Retry after {retry_after} seconds")
        else:
            # Record attempt
            limiter.record_attempt("192.168.1.1")
    """
    
    def __init__(
        self,
        max_attempts: int = 5,
        window: int = 300,  # 5 minutes
        cleanup_interval: int = 3600  # 1 hour
    ):
        self.max_attempts = max_attempts
        self.window = window
        self.cleanup_interval = cleanup_interval
        self.attempts: Dict[str, list] = defaultdict(list)
        self.last_cleanup = datetime.now()
    
    def is_allowed(self, identifier: str) -> Tuple[bool, int]:
        """
        Check if request is allowed.
        
        Args:
            identifier: IP address or user ID
            
        Returns:
            (is_allowed, retry_after_seconds)
        """
        self._cleanup_if_needed()
        
        now = datetime.now()
        window_start = now - timedelta(seconds=self.window)
        
        # Get attempts in current window
        attempts = self.attempts[identifier]
        recent_attempts = [t for t in attempts if t > window_start]
        
        if len(recent_attempts) >= self.max_attempts:
            # Calculate retry after
            oldest_attempt = min(recent_attempts)
            retry_after = int((oldest_attempt + timedelta(seconds=self.window) - now).total_seconds())
            return False, max(0, retry_after)
        
        return True, 0
    
    def record_attempt(self, identifier: str):
        """Record an attempt"""
        self.attempts[identifier].append(datetime.now())
    
    def reset(self, identifier: str):
        """Reset attempts for identifier"""
        if identifier in self.attempts:
            del self.attempts[identifier]
    
    def _cleanup_if_needed(self):
        """Cleanup old attempts"""
        now = datetime.now()
        if (now - self.last_cleanup).total_seconds() < self.cleanup_interval:
            return
        
        window_start = now - timedelta(seconds=self.window)
        
        # Remove old attempts
        for identifier in list(self.attempts.keys()):
            self.attempts[identifier] = [
                t for t in self.attempts[identifier]
                if t > window_start
            ]
            
            # Remove empty entries
            if not self.attempts[identifier]:
                del self.attempts[identifier]
        
        self.last_cleanup = now
