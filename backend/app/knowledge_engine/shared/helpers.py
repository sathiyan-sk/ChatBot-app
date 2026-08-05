from __future__ import annotations

import re
from typing import Iterable


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def split_text_into_paragraphs(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"\n\s*\n", value) if item.strip()]


def build_chunk_id(*parts: str) -> str:
    normalized_parts = [part.strip().replace(" ", "-").lower() for part in parts if part.strip()]
    return "-".join(normalized_parts)


def truncate_text(value: str, max_length: int) -> str:
    if len(value) <= max_length:
        return value
    return value[: max_length - 3].rstrip() + "..."


def coalesce_metadata(*metadata_items: dict[str, str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in metadata_items:
        result.update({key: value for key, value in item.items() if value is not None})
    return result


def deduplicate_strings(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result