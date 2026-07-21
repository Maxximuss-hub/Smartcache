import hashlib
import pickle

def generate_key(args: tuple, kwargs: dict) -> str:
    """
    Превращает ЛЮБЫЕ аргументы функции в уникальную строку-ключ.
    """
    # 1. Сортируем kwargs по ключам. 
    # Зачем? Чтобы вызовы func(a=1, b=2) и func(b=2, a=1) 
    # сгенерировали ОДИНАКОВЫЙ ключ.
    sorted_kwargs = tuple(sorted(kwargs.items()))
    
    # 2. Собираем всё в единый кортеж
    data = (args, sorted_kwargs)
    
    # 3. Сериализуем через pickle. 
    # Он умеет превращать в байты вообще всё (списки, словари, кастомные классы).
    serialized_data = pickle.dumps(data)
    
    # 4. Хэшируем байты в MD5, чтобы получить короткую и быструю строку
    return hashlib.md5(serialized_data).hexdigest()