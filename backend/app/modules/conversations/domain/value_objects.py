from __future__ import annotations


class ConversationIdentity:
    def __init__(self, value: str) -> None:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("Conversation identity cannot be empty.")
        self.value = cleaned


class MessageRole:
    def __init__(self, value: str) -> None:
        cleaned = value.strip().lower()
        if cleaned not in {"user", "assistant", "system"}:
            raise ValueError(f"Invalid message role: {cleaned}")
        self.value = cleaned