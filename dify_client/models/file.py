from pydantic import BaseModel
from typing import Optional

class UploadFileRequest(BaseModel):
    user: str


class UploadFileResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    size: Optional[int] = None
    extension: Optional[str] = None
    mime_type: Optional[str] = None
    created_by: Optional[str] = None  # created by user
    created_at: Optional[int] = None  # unix timestamp seconds
