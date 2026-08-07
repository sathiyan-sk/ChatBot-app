from __future__ import annotations

from dataclasses import dataclass

import httpx

from app.core.exceptions import ApplicationError
from app.knowledge_engine.contracts.storage import StorageContract


@dataclass(slots=True)
class SupabaseStorageProvider(StorageContract):
    settings: object

    def upload(
        self,
        *,
        path: str,
        content: bytes,
        content_type: str | None,
    ) -> None:
        normalized_path = path.strip().lstrip("/")

        if not normalized_path:
            raise ApplicationError(
                message="Storage path is required.",
                code="storage_path_required",
                status_code=400,
            )

        url = (
            f"{self.settings.supabase_url.rstrip('/')}"
            f"/storage/v1/object/"
            f"{self.settings.supabase_bucket_name}/"
            f"{normalized_path}"
        )

        headers = {
            "apikey": self.settings.supabase_service_role_key,
            "Authorization": (
                f"Bearer {self.settings.supabase_service_role_key}"
            ),
            "Content-Type": (
                content_type or "application/octet-stream"
            ),
            "x-upsert": "false",
        }

        try:
            response = httpx.post(
                url,
                headers=headers,
                content=content,
                timeout=self.settings.provider_timeout_seconds,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ApplicationError(
                message="File upload failed.",
                code="storage_upload_failed",
                status_code=502,
            ) from exc

    def upload_bytes(
        self,
        storage_path: str,
        content_bytes: bytes,
    ) -> None:
        self.upload(
            path=storage_path,
            content=content_bytes,
            content_type="application/octet-stream",
        )

    def download_bytes(
        self,
        storage_path: str,
    ) -> bytes:
        normalized_path = storage_path.strip().lstrip("/")

        if not normalized_path:
            raise ApplicationError(
                message="Storage path is required.",
                code="storage_path_required",
                status_code=400,
            )

        url = (
            f"{self.settings.supabase_url.rstrip('/')}"
            f"/storage/v1/object/"
            f"{self.settings.supabase_bucket_name}/"
            f"{normalized_path}"
        )

        headers = {
            "apikey": self.settings.supabase_service_role_key,
            "Authorization": (
                f"Bearer {self.settings.supabase_service_role_key}"
            ),
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
                message="Storage download failed.",
                code="storage_download_failed",
                status_code=502,
            ) from exc

        return response.content

    def download_text(
        self,
        storage_path: str,
    ) -> str:
        content = self.download_bytes(storage_path)

        try:
            return content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ApplicationError(
                message="Stored file is not valid UTF-8 text.",
                code="storage_text_decode_failed",
                status_code=422,
            ) from exc