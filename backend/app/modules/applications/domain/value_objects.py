from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ApplicationSlug:
    value: str


@dataclass(slots=True, frozen=True)
class RawApiKey:
    value: str


@dataclass(slots=True, frozen=True)
class ApiKeyMaterial:
    key_prefix: str
    key_hash: str
    raw_key: str