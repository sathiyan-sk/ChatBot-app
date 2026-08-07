from __future__ import annotations


class DocumentTitle:
    def __init__(self, value: str) -> None:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Document title cannot be empty.")
        self.value = cleaned


class DocumentSourceType:
    def __init__(self, value: str) -> None:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Document source type cannot be empty.")
        self.value = cleaned


class DocumentStatus:
    def __init__(self, value: str) -> None:
        cleaned = value.strip()
        if cleaned not in {"pending", "processing", "ready", "failed", "archived"}:
            raise ValueError(f"Invalid document status: {cleaned}")
        self.value = cleaned