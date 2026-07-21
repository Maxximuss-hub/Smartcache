import time
from smartcache.backends.memory import MemoryBackend
from smartcache.core.engine import CacheEngine
from smartcache.backends.base import NOT_FOUND

# Создаем движок с лимитом 3 записи и TTL по умолчанию 2 сек
backend = MemoryBackend()
engine = CacheEngine(backend, max_size=3, default_ttl=2)

def dummy_func():
    pass

# 1. Сохраняем 3 значения
engine.set(dummy_func, (1,), {}, "A")
engine.set(dummy_func, (2,), {}, "B")
engine.set(dummy_func, (3,), {}, "C")
print(engine.stats)  # Все misses

# 2. Достаем "A" — оно становится "свежим"
val = engine.get(dummy_func, (1,), {})
print(f"Достали A: {val}")  # A
print(engine.stats)  # 1 hit

# 3. Добавляем 4-е значение — должно вытисниться самое старое ("B")
engine.set(dummy_func, (4,), {}, "D")

# 4. Пытаемся достать "B" — его уже нет!
val_b = engine.get(dummy_func, (2,), {})
print(f"B вытеснен? {val_b is NOT_FOUND}")  # True

# 5. Ждем истечения TTL
time.sleep(3)
val_a = engine.get(dummy_func, (1,), {})
print(f"A истек? {val_a is NOT_FOUND}")  # True

print("\nИтоговая статистика:")
print(engine.stats)