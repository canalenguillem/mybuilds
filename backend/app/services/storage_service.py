"""Local file storage: validation, checksummed save, and PDF page counting."""
import hashlib
import os
import uuid
from dataclasses import dataclass

from fastapi import UploadFile
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.config import settings
from app.exceptions import BadRequestError

# Read uploads in chunks so large files don't load fully into memory.
_CHUNK = 1024 * 1024


@dataclass
class StoredFile:
    file_path: str
    file_size: int
    file_extension: str
    checksum: str
    original_filename: str
    pages: int | None
    storage_location: str = "local"


class StorageService:
    def __init__(self) -> None:
        self.base_path = settings.documents_path
        self.max_bytes = settings.file_max_size_mb * 1024 * 1024
        self.allowed = settings.allowed_file_types_list

    def _validate_extension(self, filename: str) -> str:
        ext = os.path.splitext(filename)[1].lstrip(".").lower()
        if not ext or ext not in self.allowed:
            raise BadRequestError(
                f"File type '.{ext or '?'}' is not allowed.",
                {"field": "file", "allowed": self.allowed},
            )
        return ext

    def save(self, upload: UploadFile, product_id: int) -> StoredFile:
        """Validate, stream to disk, and return file metadata."""
        if not upload.filename:
            raise BadRequestError("A filename is required.", {"field": "file"})
        ext = self._validate_extension(upload.filename)

        product_dir = os.path.join(self.base_path, str(product_id))
        os.makedirs(product_dir, exist_ok=True)
        dest = os.path.join(product_dir, f"{uuid.uuid4().hex}.{ext}")

        sha = hashlib.sha256()
        size = 0
        upload.file.seek(0)
        with open(dest, "wb") as out:
            while chunk := upload.file.read(_CHUNK):
                size += len(chunk)
                if size > self.max_bytes:
                    out.close()
                    os.remove(dest)
                    raise BadRequestError(
                        f"File exceeds the {settings.file_max_size_mb} MB limit.",
                        {"field": "file"},
                    )
                sha.update(chunk)
                out.write(chunk)

        if size == 0:
            os.remove(dest)
            raise BadRequestError("The uploaded file is empty.", {"field": "file"})

        return StoredFile(
            file_path=dest,
            file_size=size,
            file_extension=ext,
            checksum=sha.hexdigest(),
            original_filename=upload.filename,
            pages=self._count_pages(dest) if ext == "pdf" else None,
        )

    @staticmethod
    def _count_pages(path: str) -> int | None:
        try:
            return len(PdfReader(path).pages)
        except (PdfReadError, OSError, ValueError):
            return None

    @staticmethod
    def delete(path: str | None) -> None:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass
