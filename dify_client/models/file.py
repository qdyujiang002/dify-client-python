from pydantic import BaseModel
from typing import Optional

class UploadFileRequest(BaseModel):
    user: str


class UploadFileResponse(BaseModel):
    id: Optional[str]
    name: Optional[str]
    size: Optional[int]
    extension: Optional[str]
    mime_type: Optional[str]
    created_by: Optional[str]  # created by user
    created_at: Optional[int]  # unix timestamp seconds
