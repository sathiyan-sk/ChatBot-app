from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class GetConversationDetailQuery:
    conversation_id: str


@dataclass(slots=True, frozen=True)
class ListApplicationConversationsQuery:
    application_id: str


@dataclass(slots=True, frozen=True)
class ListIdentityConversationsQuery:
    application_id: str
    conversation_identity: str