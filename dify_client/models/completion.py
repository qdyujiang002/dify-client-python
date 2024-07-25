from typing import Optional, List

from pydantic import BaseModel

from dify_client.models.base import CompletionInputs, ResponseMode, File, Metadata, Mode


class CompletionRequest(BaseModel):
    inputs: Optional[CompletionInputs]
    response_mode: Optional[ResponseMode]
    user: Optional[str]
    conversation_id: Optional[str] = ""
    files: Optional[List[File]] = []


class CompletionResponse(BaseModel):
    message_id: Optional[str]
    conversation_id: Optional[str] = ""
    mode: Optional[Mode]
    answer: Optional[str]
    metadata: Optional[Metadata]
    created_at: Optional[int]  # unix timestamp seconds
