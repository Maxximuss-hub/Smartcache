import functools
from typing import Callable, Any
from ..core.engine import CacheEngine
from ..backends.memory import MemoryBackend
from ..backends.base import NOT_FOUND
from ..utils.logger import CacheLogger


def cache(
    func: Callable | None = None,
    *,
    ttl: int | None = None,
    max_size: int | None = None,
    backend: Any = None,
    log: bool = False,
):
    """
    Умный декоратор кэширования.
    
    Работает в двух режимах:
    - @cache
    - @cache(ttl=60, max_size=100)
    """
    
    #  МАГИЯ: Определяем, как нас вызвали
    if func is not None and callable(func):
        # Вызов без скобок: @cache
        return _create_decorator()(func)
    else:
        # Вызов со скобками: @cache(ttl=60)
        return _create_decorator(
            ttl=ttl,
            max_size=max_size,
            backend=backend,
            log=log,
        )


def _create_decorator(
    ttl: int | None = None,
    max_size: int | None = None,
    backend: Any = None,
    log: bool = False,
):
    """Создаёт декоратор с заданными параметрами."""
    
    # Создаём движок кэша (или используем предоставленный бэкенд)
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
        def wrapper(*args, **kwargs):
            # 🔥 Логгируем попытку
            if logger:
                logger.log_attempt(func.__name__)
            
            # Пытаемся достать из кэша
            cached_value = engine.get(func, args, kwargs)
            
            if cached_value is not NOT_FOUND:
                if logger:
                    logger.log_hit(func.__name__)
                return cached_value
            
            # Кэш не найден — вызываем функцию
            if logger:
                logger.log_miss(func.__name__)
            
            result = func(*args, **kwargs)
            
            # Сохраняем результат в кэш
            engine.set(func, args, kwargs, result, ttl=ttl)
            
            return result
        
        # Добавляем методы для доступа к статистике и очистке
        wrapper.cache_clear = engine.clear
        wrapper.cache_stats = engine.stats
        wrapper.cache_info = lambda: engine.stats  # Для совместимости с lru_cache
        
        return wrapper
    
    return decorator