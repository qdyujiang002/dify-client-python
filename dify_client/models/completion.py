from typing import Optional, List

from pydantic import BaseModel

from dify_client.models.base import CompletionInputs, ResponseMode, File, Metadata, Mode


class CompletionRequest(BaseModel):
    inputs: Optional[CompletionInputs] = None
    response_mode: Optional[ResponseMode] = None
    user: Optional[str] = None
    conversation_id: Optional[str] = ""
    files: Optional[List[File]] = []


class CompletionResponse(BaseModel):
    message_id: Optional[str] = None
    conversation_id: Optional[str] = ""
    mode: Optional[Mode] = None
    answer: Optional[str] = None
    metadata: Optional[Metadata] = None
    created_at: Optional[int] = None  # unix timestamp seconds
