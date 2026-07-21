from abc import ABC, abstractmethod
from typing import Any


class _NotFound:
    """Сентинел для отсутствующего значения."""
    pass


class _Expired:
    """Сентинел для истёкшего значения."""
    pass


NOT_FOUND = _NotFound()
EXPIRED = _Expired()


class StorageBackend(ABC):
    """Абстрактный интерфейс для любого хранилища."""

    @abstractmethod
    def get(self, key: str) -> Any:
        """Возвращает значение или NOT_FOUND/EXPIRED."""
        pass

    @abstractmethod
    def set(self, key: str, value: Any, ttl: int | None) -> None:
        """Сохраняет значение."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Очищает хранилище."""
        pass