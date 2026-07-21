import time
from smartcache import cache

# 🔥 ТЕСТ 1: Декоратор без скобок
@cache
def fibonacci_slow(n):
    """Медленная функция Фибоначчи."""
    if n < 2:
        return n
    return fibonacci_slow(n-1) + fibonacci_slow(n-2)

# 🔥 ТЕСТ 2: Декоратор со скобками
@cache(ttl=3, max_size=2, log=True)
def expensive_calculation(x, y):
    """Дорогая функция с TTL."""
    print(f"  🔄 Вычисляю {x} + {y}...")
    time.sleep(1)
    return x + y

#  ТЕСТ 3: Функция с нехэшируемыми аргументами
@cache
def process_data(data_dict):
    """Функция со словарём (нехэшируемый аргумент)."""
    return sum(data_dict.values())


if __name__ == "__main__":
    print("=" * 50)
    print("ТЕСТ 1: Fibonacci (без скобок)")
    print("=" * 50)
    print(f"fib(10) = {fibonacci_slow(10)}")
    print(f"fib(10) из кэша = {fibonacci_slow(10)}")
    print(fibonacci_slow.cache_stats)
    
    print("\n" + "=" * 50)
    print("ТЕСТ 2: Expensive Calculation (с TTL и логами)")
    print("=" * 50)
    print(f"Результат: {expensive_calculation(5, 10)}")
    print(f"Результат из кэша: {expensive_calculation(5, 10)}")
    
    print("\nЖдём 4 секунды (TTL=3)...")
    time.sleep(4)
    
    print(f"Результат после TTL: {expensive_calculation(5, 10)}")
    print(expensive_calculation.cache_stats)
    
    print("\n" + "=" * 50)
    print("ТЕСТ 3: Нехэшируемые аргументы")
    print("=" * 50)
    data = {"a": 1, "b": 2, "c": 3}
    print(f"process_data(data) = {process_data(data)}")
    print(f"process_data(data) из кэша = {process_data(data)}")
    print(process_data.cache_stats)