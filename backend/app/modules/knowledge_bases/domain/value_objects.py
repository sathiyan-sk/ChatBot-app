from __future__ import annotations


class KnowledgeBaseName:
    def __init__(self, value: str) -> None:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Knowledge base name cannot be empty.")
        self.value = cleaned


class KnowledgeBaseStatus:
    def __init__(self, value: str) -> None:
        cleaned = value.strip()
        if cleaned not in {"ready", "active", "inactive"}:
            raise ValueError(f"Invalid knowledge base status: {cleaned}")
        self.value = cleaned