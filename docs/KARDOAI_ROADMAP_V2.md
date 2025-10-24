# KardoAI Development Roadmap v2.0

**Version**: 0.1.0 (Planning Phase)  
**Last Updated**: October 24, 2025  
**Status**: Pre-Development  
**Philosophy**: Fast, Typed, Secure, Modular, Intelligent, Modern

---

## 🎯 Vision & Philosophy

KardoAI is the native AI integration layer for KardoCore, designed following the core principles:

- **🚀 Fast**: Minimal overhead, async-first, optimized for performance
- **📝 Typed**: Full type hints, runtime validation, IDE support
- **🔒 Secure**: API key management, content filtering, audit logging
- **🧩 Modular**: Plugin architecture, provider-agnostic, extensible
- **🧠 Intelligent**: Smart caching, cost optimization, fallback strategies
- **⚡ Modern**: Python 3.11+, async/await, latest best practices

**Key Principle**: KardoAI should work with **ANY** AI provider (existing or future) without modifying core code. Providers are plugins that can be added, removed, or switched dynamically.

---

## 🚀 Top 3 Critical Development Steps

### Step 1: Universal AI Provider Plugin System 🔴 **HIGHEST PRIORITY**

**Objective**: Create a universal, extensible plugin system that allows ANY AI provider to be integrated without modifying core code.

#### Core Philosophy

Instead of hardcoding specific providers (OpenAI, Anthropic, etc.), we create:
1. **Protocol-based interface** - Any provider that implements the protocol works
2. **Plugin discovery system** - Auto-discover installed providers
3. **Dynamic loading** - Load providers at runtime
4. **Multi-provider support** - Use multiple providers simultaneously
5. **Hot-swapping** - Switch providers without restart

#### Technical Implementation

**1.1 Provider Protocol (Interface)**

```python
# kardocore/ai/protocols.py

from typing import Protocol, AsyncIterator, Optional, List, Dict, Any
from dataclasses import dataclass

@dataclass
class AIMessage:
    """Universal message format"""
    role: str  # system, user, assistant, function
    content: str
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class AIResponse:
    """Universal response format"""
    content: str
    model: str
    provider: str
    usage: Dict[str, int]  # tokens, cost, etc.
    metadata: Dict[str, Any]
    raw_response: Any  # Original provider response

@dataclass
class AICapabilities:
    """Provider capabilities"""
    supports_chat: bool = True
    supports_streaming: bool = True
    supports_embeddings: bool = False
    supports_images: bool = False
    supports_audio: bool = False
    supports_functions: bool = False
    max_tokens: int = 4096
    context_window: int = 8192

class AIProviderProtocol(Protocol):
    """
    Protocol that ANY AI provider must implement.
    This is not a base class - it's a structural type.
    Any class with these methods is a valid provider.
    """
    
    @property
    def name(self) -> str:
        """Provider name (e.g., 'openai', 'anthropic', 'custom-llm')"""
        ...
    
    @property
    def capabilities(self) -> AICapabilities:
        """What this provider can do"""
        ...
    
    async def generate(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """Generate text completion"""
        ...
    
    async def chat(
        self,
        messages: List[AIMessage],
        *,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> AIResponse:
        """Chat completion with conversation history"""
        ...
    
    async def stream(
        self,
        prompt: str,
        *,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> AsyncIterator[str]:
        """Stream text generation"""
        ...
    
    async def embed(
        self,
        text: str,
        *,
        model: Optional[str] = None
    ) -> List[float]:
        """Generate embeddings (if supported)"""
        ...
    
    async def health_check(self) -> bool:
        """Check if provider is available"""
        ...
```

**1.2 Provider Registry & Discovery**

```python
# kardocore/ai/registry.py

from typing import Dict, Type, Optional, List
from importlib import import_module
from pathlib import Path
import inspect

class AIProviderRegistry:
    """
    Registry for AI providers.
    Providers can be registered programmatically or auto-discovered.
    """
    
    _providers: Dict[str, Type] = {}
    _instances: Dict[str, Any] = {}
    
    @classmethod
    def register(
        cls,
        name: str,
        provider_class: Type,
        *,
        auto_instantiate: bool = False,
        **config
    ):
        """
        Register a provider.
        
        Example:
            registry.register('my-ai', MyAIProvider, api_key='...')
        """
        # Validate provider implements protocol
        if not cls._implements_protocol(provider_class):
            raise TypeError(
                f"{provider_class.__name__} does not implement AIProviderProtocol"
            )
        
        cls._providers[name] = provider_class
        
        if auto_instantiate:
            cls._instances[name] = provider_class(**config)
    
    @classmethod
    def unregister(cls, name: str):
        """Unregister a provider"""
        cls._providers.pop(name, None)
        cls._instances.pop(name, None)
    
    @classmethod
    def get(cls, name: str, **config) -> Any:
        """
        Get provider instance.
        Creates new instance if not cached.
        """
        if name in cls._instances:
            return cls._instances[name]
        
        if name not in cls._providers:
            raise ValueError(f"Provider '{name}' not registered")
        
        provider_class = cls._providers[name]
        instance = provider_class(**config)
        cls._instances[name] = instance
        return instance
    
    @classmethod
    def list_providers(cls) -> List[str]:
        """List all registered providers"""
        return list(cls._providers.keys())
    
    @classmethod
    def discover_providers(cls, search_paths: Optional[List[Path]] = None):
        """
        Auto-discover providers from:
        1. kardocore/ai/providers/ (built-in)
        2. ~/.kardo/providers/ (user-installed)
        3. Custom search paths
        """
        if search_paths is None:
            search_paths = []
        
        # Built-in providers
        builtin_path = Path(__file__).parent / "providers"
        search_paths.insert(0, builtin_path)
        
        # User providers
        user_path = Path.home() / ".kardo" / "providers"
        if user_path.exists():
            search_paths.append(user_path)
        
        for path in search_paths:
            if not path.exists():
                continue
            
            for file in path.glob("*.py"):
                if file.stem.startswith("_"):
                    continue
                
                try:
                    # Import module
                    module_name = f"kardocore.ai.providers.{file.stem}"
                    module = import_module(module_name)
                    
                    # Find provider classes
                    for name, obj in inspect.getmembers(module, inspect.isclass):
                        if cls._implements_protocol(obj) and not name.startswith("_"):
                            # Auto-register with module name
                            provider_name = file.stem.replace("_", "-")
                            cls.register(provider_name, obj)
                            
                except Exception as e:
                    # Log but don't fail
                    print(f"Failed to load provider from {file}: {e}")
    
    @classmethod
    def _implements_protocol(cls, provider_class: Type) -> bool:
        """Check if class implements AIProviderProtocol"""
        required_methods = [
            'name', 'capabilities', 'generate', 'chat', 
            'stream', 'embed', 'health_check'
        ]
        return all(hasattr(provider_class, method) for method in required_methods)

# Decorator for easy registration
def ai_provider(name: str, **config):
    """
    Decorator to register a provider.
    
    Example:
        @ai_provider('my-ai')
        class MyAIProvider:
            ...
    """
    def decorator(cls):
        AIProviderRegistry.register(name, cls, **config)
        return cls
    return decorator
```

**1.3 Multi-Provider Manager**

```python
# kardocore/ai/manager.py

from typing import Optional, List, Dict, Any, Callable
from .registry import AIProviderRegistry
from .protocols import AIMessage, AIResponse, AICapabilities
import asyncio

class AIProviderManager:
    """
    Manages multiple AI providers with:
    - Load balancing
    - Failover
    - Cost optimization
    - Provider selection strategies
    """
    
    def __init__(self):
        self.providers: Dict[str, Any] = {}
        self.default_provider: Optional[str] = None
        self.fallback_chain: List[str] = []
        self.strategy: str = "default"  # default, cheapest, fastest, round-robin
        self._round_robin_index = 0
    
    def add_provider(
        self,
        name: str,
        provider_or_config: Any,
        *,
        is_default: bool = False,
        priority: int = 0
    ):
        """Add a provider to the manager"""
        if isinstance(provider_or_config, dict):
            # It's a config, get from registry
            provider = AIProviderRegistry.get(name, **provider_or_config)
        else:
            # It's already an instance
            provider = provider_or_config
        
        self.providers[name] = {
            "instance": provider,
            "priority": priority,
            "enabled": True,
            "stats": {
                "requests": 0,
                "failures": 0,
                "total_tokens": 0,
                "avg_latency": 0.0
            }
        }
        
        if is_default or self.default_provider is None:
            self.default_provider = name
        
        # Update fallback chain
        self._update_fallback_chain()
    
    def remove_provider(self, name: str):
        """Remove a provider"""
        self.providers.pop(name, None)
        if self.default_provider == name:
            self.default_provider = next(iter(self.providers.keys()), None)
        self._update_fallback_chain()
    
    def set_default(self, name: str):
        """Set default provider"""
        if name not in self.providers:
            raise ValueError(f"Provider '{name}' not found")
        self.default_provider = name
    
    def set_strategy(self, strategy: str):
        """
        Set provider selection strategy:
        - default: Use default provider
        - cheapest: Select cheapest provider
        - fastest: Select fastest provider
        - round-robin: Rotate between providers
        - smart: AI-based selection (future)
        """
        self.strategy = strategy
    
    async def generate(
        self,
        prompt: str,
        *,
        provider: Optional[str] = None,
        fallback: bool = True,
        **kwargs
    ) -> AIResponse:
        """
        Generate with automatic provider selection and fallback.
        """
        selected_provider = provider or self._select_provider()
        
        if not fallback:
            # No fallback, use selected provider only
            return await self._call_provider(selected_provider, "generate", prompt, **kwargs)
        
        # Try with fallback chain
        providers_to_try = [selected_provider] + [
            p for p in self.fallback_chain if p != selected_provider
        ]
        
        last_error = None
        for provider_name in providers_to_try:
            try:
                response = await self._call_provider(
                    provider_name,
                    "generate",
                    prompt,
                    **kwargs
                )
                return response
            except Exception as e:
                last_error = e
                self._record_failure(provider_name)
                continue
        
        raise RuntimeError(
            f"All providers failed. Last error: {last_error}"
        )
    
    async def chat(
        self,
        messages: List[AIMessage],
        *,
        provider: Optional[str] = None,
        fallback: bool = True,
        **kwargs
    ) -> AIResponse:
        """Chat with automatic provider selection and fallback"""
        selected_provider = provider or self._select_provider()
        
        if not fallback:
            return await self._call_provider(selected_provider, "chat", messages, **kwargs)
        
        providers_to_try = [selected_provider] + [
            p for p in self.fallback_chain if p != selected_provider
        ]
        
        last_error = None
        for provider_name in providers_to_try:
            try:
                response = await self._call_provider(
                    provider_name,
                    "chat",
                    messages,
                    **kwargs
                )
                return response
            except Exception as e:
                last_error = e
                self._record_failure(provider_name)
                continue
        
        raise RuntimeError(f"All providers failed. Last error: {last_error}")
    
    async def stream(
        self,
        prompt: str,
        *,
        provider: Optional[str] = None,
        **kwargs
    ):
        """Stream generation (no fallback for streaming)"""
        selected_provider = provider or self._select_provider()
        provider_instance = self.providers[selected_provider]["instance"]
        
        async for chunk in provider_instance.stream(prompt, **kwargs):
            yield chunk
    
    def _select_provider(self) -> str:
        """Select provider based on strategy"""
        if self.strategy == "default":
            return self.default_provider
        
        elif self.strategy == "round-robin":
            enabled = [
                name for name, data in self.providers.items()
                if data["enabled"]
            ]
            if not enabled:
                return self.default_provider
            
            provider = enabled[self._round_robin_index % len(enabled)]
            self._round_robin_index += 1
            return provider
        
        elif self.strategy == "cheapest":
            # Select provider with lowest cost
            # (requires cost tracking implementation)
            return self.default_provider
        
        elif self.strategy == "fastest":
            # Select provider with lowest latency
            fastest = min(
                self.providers.items(),
                key=lambda x: x[1]["stats"]["avg_latency"]
            )
            return fastest[0]
        
        return self.default_provider
    
    async def _call_provider(
        self,
        provider_name: str,
        method: str,
        *args,
        **kwargs
    ):
        """Call provider method with stats tracking"""
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not found")
        
        provider_data = self.providers[provider_name]
        if not provider_data["enabled"]:
            raise RuntimeError(f"Provider '{provider_name}' is disabled")
        
        provider = provider_data["instance"]
        
        # Track stats
        import time
        start = time.time()
        
        try:
            result = await getattr(provider, method)(*args, **kwargs)
            
            # Update stats
            latency = time.time() - start
            stats = provider_data["stats"]
            stats["requests"] += 1
            stats["avg_latency"] = (
                (stats["avg_latency"] * (stats["requests"] - 1) + latency)
                / stats["requests"]
            )
            
            if hasattr(result, "usage"):
                stats["total_tokens"] += result.usage.get("total_tokens", 0)
            
            return result
            
        except Exception as e:
            provider_data["stats"]["failures"] += 1
            raise
    
    def _record_failure(self, provider_name: str):
        """Record provider failure"""
        if provider_name in self.providers:
            self.providers[provider_name]["stats"]["failures"] += 1
    
    def _update_fallback_chain(self):
        """Update fallback chain based on priority"""
        self.fallback_chain = sorted(
            [name for name, data in self.providers.items() if data["enabled"]],
            key=lambda x: self.providers[x]["priority"],
            reverse=True
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all providers"""
        return {
            name: data["stats"]
            for name, data in self.providers.items()
        }
```

**1.4 Main KardoAI Interface**

```python
# kardocore/ai/__init__.py

from typing import Optional, List, Dict, Any
from .manager import AIProviderManager
from .registry import AIProviderRegistry, ai_provider
from .protocols import AIMessage, AIResponse, AICapabilities

class KardoAI:
    """
    Main KardoAI interface.
    
    Usage:
        # Simple usage with default provider
        ai = KardoAI(provider='openai', api_key='...')
        response = await ai.generate("Hello")
        
        # Multi-provider with fallback
        ai = KardoAI()
        ai.add_provider('openai', api_key='...', is_default=True)
        ai.add_provider('anthropic', api_key='...', priority=1)
        ai.add_provider('google', api_key='...', priority=2)
        
        response = await ai.generate("Hello")  # Auto-fallback
        
        # Switch provider dynamically
        response = await ai.generate("Hello", provider='anthropic')
    """
    
    def __init__(
        self,
        provider: Optional[str] = None,
        api_key: Optional[str] = None,
        **config
    ):
        # Auto-discover providers
        AIProviderRegistry.discover_providers()
        
        # Initialize manager
        self.manager = AIProviderManager()
        
        # Add initial provider if specified
        if provider:
            self.manager.add_provider(
                provider,
                {"api_key": api_key, **config},
                is_default=True
            )
    
    def add_provider(
        self,
        name: str,
        *,
        is_default: bool = False,
        priority: int = 0,
        **config
    ):
        """Add a provider"""
        self.manager.add_provider(name, config, is_default=is_default, priority=priority)
        return self
    
    def remove_provider(self, name: str):
        """Remove a provider"""
        self.manager.remove_provider(name)
        return self
    
    def set_default(self, name: str):
        """Set default provider"""
        self.manager.set_default(name)
        return self
    
    def set_strategy(self, strategy: str):
        """Set provider selection strategy"""
        self.manager.set_strategy(strategy)
        return self
    
    async def generate(
        self,
        prompt: str,
        *,
        provider: Optional[str] = None,
        fallback: bool = True,
        **kwargs
    ) -> AIResponse:
        """Generate text"""
        return await self.manager.generate(
            prompt,
            provider=provider,
            fallback=fallback,
            **kwargs
        )
    
    async def chat(
        self,
        messages: List[AIMessage],
        *,
        provider: Optional[str] = None,
        fallback: bool = True,
        **kwargs
    ) -> AIResponse:
        """Chat completion"""
        return await self.manager.chat(
            messages,
            provider=provider,
            fallback=fallback,
            **kwargs
        )
    
    async def stream(
        self,
        prompt: str,
        *,
        provider: Optional[str] = None,
        **kwargs
    ):
        """Stream generation"""
        async for chunk in self.manager.stream(prompt, provider=provider, **kwargs):
            yield chunk
    
    def list_providers(self) -> List[str]:
        """List available providers"""
        return AIProviderRegistry.list_providers()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics"""
        return self.manager.get_stats()

# Export main components
__all__ = [
    'KardoAI',
    'AIMessage',
    'AIResponse',
    'AICapabilities',
    'AIProviderRegistry',
    'ai_provider',
]
```

**1.5 Example Provider Plugin**

```python
# Example: Custom provider plugin
# File: ~/.kardo/providers/my_custom_ai.py

from kardocore.ai import ai_provider, AIMessage, AIResponse, AICapabilities
from typing import List, Optional, AsyncIterator
import httpx

@ai_provider('my-custom-ai')
class MyCustomAIProvider:
    """Custom AI provider example"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.my-ai.com", **config):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    @property
    def name(self) -> str:
        return "my-custom-ai"
    
    @property
    def capabilities(self) -> AICapabilities:
        return AICapabilities(
            supports_chat=True,
            supports_streaming=True,
            supports_embeddings=True,
            max_tokens=8000,
            context_window=16000
        )
    
    async def generate(self, prompt: str, **kwargs) -> AIResponse:
        response = await self.client.post(
            f"{self.base_url}/generate",
            json={"prompt": prompt, **kwargs},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        data = response.json()
        
        return AIResponse(
            content=data["text"],
            model=data["model"],
            provider=self.name,
            usage=data["usage"],
            metadata={},
            raw_response=data
        )
    
    async def chat(self, messages: List[AIMessage], **kwargs) -> AIResponse:
        # Implementation...
        pass
    
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]:
        # Implementation...
        pass
    
    async def embed(self, text: str, **kwargs) -> List[float]:
        # Implementation...
        pass
    
    async def health_check(self) -> bool:
        try:
            response = await self.client.get(f"{self.base_url}/health")
            return response.status_code == 200
        except:
            return False
```

#### Deliverables

- ✅ Provider Protocol (interface)
- ✅ Provider Registry with auto-discovery
- ✅ Multi-Provider Manager
- ✅ Main KardoAI class
- ✅ Plugin system
- ✅ Example plugins (OpenAI, Anthropic, Google)
- ✅ CLI for provider management
- ✅ Documentation
- ✅ Unit tests

#### Timeline
**3-4 weeks**

---

### Step 2: Intelligent Vector Storage & Semantic Search 🟡 **HIGH PRIORITY**

**Objective**: Create a universal, provider-agnostic vector storage system with intelligent caching and semantic search.

#### Core Philosophy

- **Any vector DB**: Support any vector database (ChromaDB, Pinecone, Weaviate, Qdrant, custom)
- **Local-first**: Work offline with local vector DB
- **Smart caching**: Intelligent embedding cache to reduce API calls
- **Async-first**: Non-blocking operations
- **Type-safe**: Full type hints

#### Technical Implementation

**2.1 Vector Storage Protocol**

```python
# kardocore/ai/vector/protocols.py

from typing import Protocol, List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class VectorDocument:
    """Universal document format"""
    id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any]

@dataclass
class SearchResult:
    """Search result with score"""
    document: VectorDocument
    score: float
    distance: float

class VectorStorageProtocol(Protocol):
    """Protocol for vector storage backends"""
    
    @property
    def name(self) -> str:
        """Storage backend name"""
        ...
    
    async def create_collection(
        self,
        name: str,
        dimension: int,
        **kwargs
    ):
        """Create collection/index"""
        ...
    
    async def add(
        self,
        collection: str,
        documents: List[VectorDocument]
    ):
        """Add documents"""
        ...
    
    async def search(
        self,
        collection: str,
        query_embedding: List[float],
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Search similar documents"""
        ...
    
    async def delete(
        self,
        collection: str,
        document_ids: List[str]
    ):
        """Delete documents"""
        ...
    
    async def health_check(self) -> bool:
        """Check if storage is available"""
        ...
```

**2.2 Smart Embedding Cache**

```python
# kardocore/ai/vector/cache.py

from typing import List, Optional, Dict
import hashlib
import json
from pathlib import Path

class EmbeddingCache:
    """
    Intelligent embedding cache to reduce API calls.
    
    Features:
    - Persistent cache (disk)
    - In-memory cache (LRU)
    - TTL support
    - Cost tracking
    """
    
    def __init__(
        self,
        cache_dir: Optional[Path] = None,
        max_memory_size: int = 1000,
        ttl_seconds: Optional[int] = None
    ):
        self.cache_dir = cache_dir or Path.home() / ".kardo" / "cache" / "embeddings"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.memory_cache: Dict[str, List[float]] = {}
        self.max_memory_size = max_memory_size
        self.ttl_seconds = ttl_seconds
        
        self.stats = {
            "hits": 0,
            "misses": 0,
            "api_calls_saved": 0
        }
    
    def _hash_text(self, text: str, model: str) -> str:
        """Generate cache key"""
        key = f"{model}:{text}"
        return hashlib.sha256(key.encode()).hexdigest()
    
    async def get(
        self,
        text: str,
        model: str
    ) -> Optional[List[float]]:
        """Get embedding from cache"""
        cache_key = self._hash_text(text, model)
        
        # Check memory cache
        if cache_key in self.memory_cache:
            self.stats["hits"] += 1
            return self.memory_cache[cache_key]
        
        # Check disk cache
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            try:
                with open(cache_file) as f:
                    data = json.load(f)
                
                # Check TTL
                if self.ttl_seconds:
                    import time
                    if time.time() - data["timestamp"] > self.ttl_seconds:
                        cache_file.unlink()
                        self.stats["misses"] += 1
                        return None
                
                embedding = data["embedding"]
                
                # Add to memory cache
                if len(self.memory_cache) < self.max_memory_size:
                    self.memory_cache[cache_key] = embedding
                
                self.stats["hits"] += 1
                return embedding
                
            except Exception:
                pass
        
        self.stats["misses"] += 1
        return None
    
    async def set(
        self,
        text: str,
        model: str,
        embedding: List[float]
    ):
        """Store embedding in cache"""
        cache_key = self._hash_text(text, model)
        
        # Memory cache
        if len(self.memory_cache) < self.max_memory_size:
            self.memory_cache[cache_key] = embedding
        
        # Disk cache
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            import time
            with open(cache_file, 'w') as f:
                json.dump({
                    "text": text,
                    "model": model,
                    "embedding": embedding,
                    "timestamp": time.time()
                }, f)
            
            self.stats["api_calls_saved"] += 1
        except Exception:
            pass
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        hit_rate = (
            self.stats["hits"] / (self.stats["hits"] + self.stats["misses"])
            if (self.stats["hits"] + self.stats["misses"]) > 0
            else 0
        )
        
        return {
            **self.stats,
            "hit_rate": hit_rate,
            "memory_size": len(self.memory_cache)
        }
```

**2.3 Semantic Search Service**

```python
# kardocore/ai/search.py

from typing import List, Optional, Dict, Any
from .kardoai import KardoAI
from .vector.protocols import VectorStorageProtocol, VectorDocument, SearchResult
from .vector.cache import EmbeddingCache

class SemanticSearch:
    """
    Universal semantic search service.
    Works with any vector storage backend.
    """
    
    def __init__(
        self,
        ai: KardoAI,
        vector_storage: VectorStorageProtocol,
        collection: str = "default",
        *,
        use_cache: bool = True,
        embedding_model: Optional[str] = None
    ):
        self.ai = ai
        self.vector_storage = vector_storage
        self.collection = collection
        self.embedding_model = embedding_model
        
        self.cache = EmbeddingCache() if use_cache else None
    
    async def _get_embedding(self, text: str) -> List[float]:
        """Get embedding with caching"""
        model = self.embedding_model or "default"
        
        # Check cache
        if self.cache:
            cached = await self.cache.get(text, model)
            if cached:
                return cached
        
        # Generate embedding
        embedding = await self.ai.manager.providers[
            self.ai.manager.default_provider
        ]["instance"].embed(text, model=self.embedding_model)
        
        # Store in cache
        if self.cache:
            await self.cache.set(text, model, embedding)
        
        return embedding
    
    async def index_document(
        self,
        doc_id: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Index a document"""
        embedding = await self._get_embedding(content)
        
        doc = VectorDocument(
            id=doc_id,
            content=content,
            embedding=embedding,
            metadata=metadata or {}
        )
        
        await self.vector_storage.add(self.collection, [doc])
    
    async def index_batch(
        self,
        documents: List[Dict[str, Any]],
        *,
        batch_size: int = 100
    ):
        """Index multiple documents in batches"""
        import asyncio
        
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            # Generate embeddings in parallel
            tasks = [
                self._get_embedding(doc["content"])
                for doc in batch
            ]
            embeddings = await asyncio.gather(*tasks)
            
            # Create vector documents
            vector_docs = [
                VectorDocument(
                    id=doc["id"],
                    content=doc["content"],
                    embedding=embedding,
                    metadata=doc.get("metadata", {})
                )
                for doc, embedding in zip(batch, embeddings)
            ]
            
            # Add to storage
            await self.vector_storage.add(self.collection, vector_docs)
    
    async def search(
        self,
        query: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        """Semantic search"""
        query_embedding = await self._get_embedding(query)
        
        results = await self.vector_storage.search(
            self.collection,
            query_embedding,
            limit=limit,
            filters=filters
        )
        
        return results
    
    async def delete_document(self, doc_id: str):
        """Delete document"""
        await self.vector_storage.delete(self.collection, [doc_id])
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if self.cache:
            return self.cache.get_stats()
        return {}
```

#### Deliverables

- ✅ Vector storage protocol
- ✅ Smart embedding cache
- ✅ Semantic search service
- ✅ Example adapters (ChromaDB, Pinecone, Qdrant)
- ✅ Model mixin for searchable models
- ✅ CLI commands
- ✅ Admin UI
- ✅ Documentation

#### Timeline
**3-4 weeks**

---

### Step 3: RAG System with Content Generation 🟢 **MEDIUM-HIGH PRIORITY**

**Objective**: Intelligent content generation with Retrieval Augmented Generation (RAG) for accurate, context-aware content.

#### Core Philosophy

- **Context-aware**: Use existing content as context
- **Accurate**: RAG ensures factual accuracy
- **Customizable**: Configurable prompts and strategies
- **Streaming**: Real-time content generation
- **Cost-optimized**: Smart token management

#### Technical Implementation

```python
# kardocore/ai/rag.py

from typing import List, Optional, Dict, Any, AsyncIterator
from .kardoai import KardoAI
from .search import SemanticSearch
from .protocols import AIMessage

class RAGSystem:
    """
    Retrieval Augmented Generation system.
    
    Features:
    - Smart context retrieval
    - Token budget management
    - Streaming support
    - Cost optimization
    """
    
    def __init__(
        self,
        ai: KardoAI,
        search: SemanticSearch,
        *,
        max_context_tokens: int = 2000,
        retrieval_limit: int = 5
    ):
        self.ai = ai
        self.search = search
        self.max_context_tokens = max_context_tokens
        self.retrieval_limit = retrieval_limit
    
    async def generate_with_context(
        self,
        query: str,
        *,
        system_prompt: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        stream: bool = False,
        **kwargs
    ):
        """Generate content with RAG"""
        # Retrieve relevant context
        results = await self.search.search(
            query,
            limit=self.retrieval_limit,
            filters=filters
        )
        
        # Build context
        context = self._build_context(results)
        
        # Build prompt
        full_prompt = self._build_prompt(query, context)
        
        if stream:
            async for chunk in self.ai.stream(
                full_prompt,
                system_prompt=system_prompt,
                **kwargs
            ):
                yield chunk
        else:
            response = await self.ai.generate(
                full_prompt,
                system_prompt=system_prompt,
                **kwargs
            )
            return response
    
    def _build_context(self, results: List) -> str:
        """Build context from search results"""
        context_parts = []
        total_tokens = 0
        
        for result in results:
            # Estimate tokens (rough: 1 token ≈ 4 chars)
            doc_tokens = len(result.document.content) // 4
            
            if total_tokens + doc_tokens > self.max_context_tokens:
                break
            
            context_parts.append(
                f"[Source {len(context_parts) + 1}] {result.document.content}"
            )
            total_tokens += doc_tokens
        
        return "\n\n".join(context_parts)
    
    def _build_prompt(self, query: str, context: str) -> str:
        """Build RAG prompt"""
        return f"""
Use the following context to answer the query. If the context doesn't contain
relevant information, say so and provide a general answer.

Context:
{context}

Query: {query}

Answer:
"""

# Content generator with RAG
class ContentGenerator:
    """AI content generation with RAG"""
    
    def __init__(self, rag: RAGSystem):
        self.rag = rag
    
    async def generate_article(
        self,
        topic: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate article with RAG"""
        # Implementation...
        pass
    
    async def generate_summary(
        self,
        content: str
    ) -> str:
        """Generate summary"""
        # Implementation...
        pass
    
    async def expand_outline(
        self,
        outline: str,
        section: str
    ) -> str:
        """Expand outline section"""
        # Implementation...
        pass
```

#### Deliverables

- ✅ RAG system
- ✅ Content generator
- ✅ Streaming support
- ✅ Token management
- ✅ Admin UI widgets
- ✅ API endpoints
- ✅ Documentation

#### Timeline
**3-4 weeks**

---

## 📅 Overall Timeline

**Total: 9-12 weeks**

| Phase | Duration |
|-------|----------|
| Step 1: Universal Provider System | 3-4 weeks |
| Step 2: Semantic Search | 3-4 weeks |
| Step 3: RAG & Content Generation | 3-4 weeks |

---

## 🎯 Success Metrics

**Technical**:
- Support ANY AI provider via plugin system
- <50ms provider switching overhead
- 95%+ cache hit rate for embeddings
- <2s average response time
- 90%+ test coverage

**User**:
- 90%+ satisfaction
- 60%+ reduction in content creation time
- 85%+ accuracy in semantic search

---

## 🔗 Repository

- https://github.com/webcien/Kardo/blob/main/docs/KARDOAI_ROADMAP_V2.md

