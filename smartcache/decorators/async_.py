import functools
from typing import Callable, Any
from ..core.engine import CacheEngine
from ..backends.memory import MemoryBackend
from ..backends.base import NOT_FOUND
from ..utils.logger import CacheLogger


def async_cache(
    func: Callable | None = None,
    *,
    ttl: int | None = None,
    max_size: int | None = None,
    backend: Any = None,
    log: bool = False,
):
    """
    Асинхронный декоратор кэширования.
    """
    
    if func is not None and callable(func):
        return _create_async_decorator()(func)
    else:
        return _create_async_decorator(
            ttl=ttl,
            max_size=max_size,
            backend=backend,
            log=log,
        )


def _create_async_decorator(
    ttl: int | None = None,
    max_size: int | None = None,
    backend: Any = None,
    log: bool = False,
):
    """Создаёт асинхронный декоратор."""
    
    if backend is None:
        backend = MemoryBackend()
    
    engine = CacheEngine(
        backend=backend,
        max_size=max_size,
        default_ttl=ttl,
    )
    
    logger = CacheLogger() if log else None
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if logger:
                logger.log_attempt(func.__name__)
            
            cached_value = engine.get(func, args, kwargs)
            
            if cached_value is not NOT_FOUND:
                if logger:
                    logger.log_hit(func.__name__)
                return cached_value
            
            if logger:
                logger.log_miss(func.__name__)
            
            result = await func(*args, **kwargs)
            
            engine.set(func, args, kwargs, result, ttl=ttl)
            
            return result
        
        wrapper.cache_clear = engine.clear
        wrapper.cache_stats = engine.stats
        
        return wrapper
    
    return decorator