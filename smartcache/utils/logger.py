class CacheLogger:
    """Простой логгер для кэша."""
    
    def log_attempt(self, func_name: str):
        pass  # Можно добавить логирование попыток
    
    def log_hit(self, func_name: str):
        print(f"✅ CACHE HIT  | {func_name}")
    
    def log_miss(self, func_name: str):
        print(f"❌ CACHE MISS | {func_name}")
    
    def log_expired(self, func_name: str):
        print(f"⏰ CACHE EXPIRED | {func_name}")