from __future__ import annotations

from app.knowledge_engine.shared.models import RetrievedChunk


class PromptBuilder:
    def build_system_prompt(self) -> str:
        return (
            "You are an AI knowledge assistant. "
            "Answer only from the retrieved knowledge and the recent conversation context. "
            "Do not invent facts. If the knowledge is insufficient, clearly say so."
        )

    def build_user_prompt(
        self,
        *,
        query_text: str,
        conversation_messages: list[dict[str, str]],
        retrieved_chunks: list[RetrievedChunk],
    ) -> str:
        conversation_block = "\n".join(
            f"{item['role']}: {item['content']}"
            for item in conversation_messages
        ) or "No recent conversation."

        knowledge_block = "\n\n".join(
            f"[{index + 1}] {chunk.document_title}\n{chunk.content}"
            for index, chunk in enumerate(retrieved_chunks)
        ) or "No retrieved knowledge."

        return (
            f"Recent conversation:\n{conversation_block}\n\n"
            f"Retrieved knowledge:\n{knowledge_block}\n\n"
            f"Question:\n{query_text}\n\n"
            "Return a concise grounded answer."
        )