import asyncio
from smartcache import async_cache
from smartcache.backends.disk import DiskBackend


# ТЕСТ 1: Async с TTL
@async_cache(ttl=3, log=True)
async def fetch_data(url: str):
    """Имитация асинхронного запроса."""
    print(f"  🌐 Запрос к {url}...")
    await asyncio.sleep(1)
    return f"Data from {url}"


# ТЕСТ 2: Disk Backend (сохранение между запусками)
disk_backend = DiskBackend("./my_cache")

@async_cache(backend=disk_backend, log=True)
async def heavy_computation(x: int):
    """Тяжелое вычисление с сохранением на диск."""
    print(f"   Вычисляю {x}^2...")
    await asyncio.sleep(1)
    return x ** 2


async def main():
    print("=" * 50)
    print("ТЕСТ 1: Async Cache")
    print("=" * 50)
    
    result1 = await fetch_data("https://api.example.com")
    print(f"Результат: {result1}")
    
    result2 = await fetch_data("https://api.example.com")
    print(f"Из кэша: {result2}")
    
    print("\nЖдём 4 секунды...")
    await asyncio.sleep(4)
    
    result3 = await fetch_data("https://api.example.com")
    print(f"После TTL: {result3}")
    
    print("\n" + "=" * 50)
    print("ТЕСТ 2: Disk Backend")
    print("=" * 50)
    
    result4 = await heavy_computation(42)
    print(f"Результат: {result4}")
    
    result5 = await heavy_computation(42)
    print(f"Из кэша: {result5}")
    
    print("\n✅ Кэш сохранён на диск! Перезапусти скрипт — он загрузится.")


if __name__ == "__main__":
    asyncio.run(main())