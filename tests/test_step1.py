import time
from smartcache.utils.keymaker import generate_key
from smartcache.backends.memory import MemoryBackend, NOT_FOUND

# 1. Тестируем генератор ключей
key1 = generate_key((1, 2), {'a': 5, 'b': [1, 2]})
key2 = generate_key((1, 2), {'b': [1, 2], 'a': 5}) # Порядок kwargs другой!
print(f"Ключи совпадают? {key1 == key2}") # Должно быть True

# 2. Тестируем бэкенд
cache = MemoryBackend()

# Сохраняем на 2 секунды
cache.set("test_key", "Hello World", ttl=2)

# Достаем сразу
val = cache.get("test_key")
print(f"Сразу: {val}") # Hello World

# Ждем 3 секунды
time.sleep(3)

# Достаем после истечения TTL
val_expired = cache.get("test_key")
print(f"Через 3 сек: {val_expired is NOT_FOUND}") # Должно быть True