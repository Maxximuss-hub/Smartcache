from .decorators.sync import cache
from .decorators.async_ import async_cache

__all__ = ["cache", "async_cache"]
__version__ = "0.2.0"