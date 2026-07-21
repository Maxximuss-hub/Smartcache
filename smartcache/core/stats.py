class CacheStats:
    """Сборщик статистики кэша."""

    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.expired = 0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    def record_expired(self):
        self.expired += 1

    @property
    def hit_rate(self) -> float:
        total = self.hits + self.misses
        if total == 0:
            return 0.0
        return (self.hits / total) * 100

    def __str__(self) -> str:
        total = self.hits + self.misses
        return (
            f"📊 Cache Statistics\n"
            f"   Hits:     {self.hits}\n"
            f"   Misses:   {self.misses}\n"
            f"   Expired:  {self.expired}\n"
            f"   Hit Rate: {self.hit_rate:.1f}%\n"
            f"   Total:    {total}"
        )

    def reset(self):
        self.hits = 0
        self.misses = 0
        self.expired = 0