import time
from typing import Any
from .base import StorageBackend, NOT_FOUND, EXPIRED


class MemoryBackend(StorageBackend):
    """Хранилище в оперативной памяти."""

    def __init__(self):
        self._store: dict[str, tuple[Any, float | None]] = {}

    def get(self, key: str) -> Any:
        if key not in self._store:
            return NOT_FOUND
        
        value, expire_at = self._store[key]
        
        if expire_at is not None and time.monotonic() >= expire_at:
            del self._store[key]
            return EXPIRED  # ✅ Возвращаем EXPIRED вместо NOT_FOUND
        
        return value

    def set(self, key: str, value: Any, ttl: int | None) -> None:
        expire_at = None
        if ttl is not None:
            expire_at = time.monotonic() + ttl
        
        self._store[key] = (value, expire_at)

    def clear(self) -> None:
        self._store.clear()