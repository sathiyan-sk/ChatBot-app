from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass
class InMemoryMetricsRegistry:
    _lock: Lock = field(default_factory=Lock)
    _counters: dict[str, int] = field(default_factory=dict)

    def increment(self, name: str, amount: int = 1) -> None:
        with self._lock:
            self._counters[name] = self._counters.get(name, 0) + amount

    def snapshot(self) -> dict[str, int]:
        with self._lock:
            return dict(self._counters)