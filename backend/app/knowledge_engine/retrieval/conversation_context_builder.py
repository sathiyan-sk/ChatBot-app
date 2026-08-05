from __future__ import annotations


class ConversationContextBuilder:
    def build(self, messages: list[dict[str, str]], max_messages: int = 12) -> list[dict[str, str]]:
        if not messages:
            return []
        return messages[-max_messages:]