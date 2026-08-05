from __future__ import annotations

from typing import Literal

SourceType = Literal["file", "website", "csv", "image"]
DocumentParserType = Literal["structured", "html", "ocr"]
ChunkingStrategy = Literal["recursive", "section-aware", "row-aware"]