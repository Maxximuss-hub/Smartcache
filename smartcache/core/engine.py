from typing import Any
from collections import OrderedDict

from ..backends.base import StorageBackend, NOT_FOUND, EXPIRED
from ..utils.keymaker import generate_key
from .stats import CacheStats


class CacheEngine:
    """Главное ядро кэша."""

    def __init__(
        self,
        backend: StorageBackend,
        max_size: int | None = None,
        default_ttl: int | None = None,
    ):
        self._backend = backend
        self._max_size = max_size
        self._default_ttl = default_ttl
        self._stats = CacheStats()
        self._access_order: OrderedDict[str, None] = OrderedDict()

    def get(self, func, args: tuple, kwargs: dict) -> Any:
        """Пытается достать значение из кэша."""
        key = generate_key((func.__name__, *args), kwargs)
        
        if key in self._access_order:
            self._access_order.move_to_end(key)

        value = self._backend.get(key)

        # ✅ Обрабатываем истечение TTL
        if isinstance(value, EXPIRED.__class__):
            self._stats.record_expired()
            self._stats.record_miss()
            return NOT_FOUND
        
        if isinstance(value, NOT_FOUND.__class__):
            self._stats.record_miss()
            return NOT_FOUND
        
        self._stats.record_hit()
        return value

    def set(self, func, args: tuple, kwargs: dict, value: Any, ttl: int | None = None) -> None:
        """Сохраняет значение в кэш."""
        key = generate_key((func.__name__, *args), kwargs)
        
        if self._max_size is not None and len(self._access_order) >= self._max_size:
            self._evict_oldest()

        effective_ttl = ttl if ttl is not None else self._default_ttl
        self._backend.set(key, value, effective_ttl)
        
        self._access_order[key] = None

    def _evict_oldest(self):
        """Удаляет самую старую запись (LRU)."""
        if self._access_order:
            oldest_key, _ = self._access_order.popitem(last=False)
            self._backend._store.pop(oldest_key, None)

    def clear(self):
        """Очищает весь кэш."""
        self._backend.clear()
        self._access_order.clear()
        self._stats.reset()

    @property
    def stats(self) -> CacheStats:
        return self._stats