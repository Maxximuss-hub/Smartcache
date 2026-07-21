import pickle
import time
from pathlib import Path
from typing import Any
from .base import StorageBackend, NOT_FOUND, EXPIRED


class DiskBackend(StorageBackend):
    """Хранилище на диске (через pickle)."""

    def __init__(self, cache_dir: str = ".smartcache"):
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(exist_ok=True)
        self._metadata_file = self._cache_dir / "metadata.pkl"
        
        # Загружаем метаданные при инициализации
        self._store = self._load_metadata()

    def _load_metadata(self) -> dict:
        """Загружает метаданные кэша с диска."""
        if self._metadata_file.exists():
            with open(self._metadata_file, "rb") as f:
                return pickle.load(f)
        return {}

    def _save_metadata(self):
        """Сохраняет метаданные на диск."""
        with open(self._metadata_file, "wb") as f:
            pickle.dump(self._store, f)

    def get(self, key: str) -> Any:
        if key not in self._store:
            return NOT_FOUND
        
        value, expire_at = self._store[key]
        
        if expire_at is not None and time.monotonic() >= expire_at:
            del self._store[key]
            self._save_metadata()
            return EXPIRED
        
        return value

    def set(self, key: str, value: Any, ttl: int | None) -> None:
        expire_at = None
        if ttl is not None:
            expire_at = time.monotonic() + ttl
        
        self._store[key] = (value, expire_at)
        self._save_metadata()

    def clear(self) -> None:
        self._store.clear()
        self._save_metadata()