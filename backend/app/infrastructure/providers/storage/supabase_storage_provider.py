from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.storage import StorageContract


@dataclass(slots=True)
class SupabaseStorageProvider(StorageContract):
    settings: object

    def download_text(self, storage_path: str) -> str:
        content_bytes = self.download_bytes(storage_path)
        try:
            return content_bytes.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ApplicationError(
                message="Stored file is not valid UTF-8 text.",
                code="storage_text_decode_failed",
                status_code=422,
            ) from exc

    def download_bytes(self, storage_path: str) -> bytes:
        normalized_path = storage_path.strip().lstrip("/")
        if not normalized_path:
            raise ApplicationError(
                message="Storage path is required.",
                code="storage_path_required",
                status_code=400,
            )

        url = (
            f"{self.settings.supabase_url.rstrip('/')}"
            f"/storage/v1/object/{self.settings.supabase_bucket_name}/{normalized_path}"
        )

        headers = {
            "apikey": self.settings.supabase_service_role_key,
            "Authorization": f"Bearer {self.settings.supabase_service_role_key}",
        }

        try:
            response = httpx.get(
                url,
                headers=headers,
                timeout=self.settings.provider_timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="Storage provider download failed.",
                code="storage_download_failed",
                status_code=502,
            ) from exc

        return response.content