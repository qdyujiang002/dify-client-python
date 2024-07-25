from typing import Dict, List, Optional, Any

from pydantic import BaseModel, Field

from dify_client.models.base import ResponseMode, File
from dify_client.models.completion import CompletionResponse


class ChatRequest(BaseModel):
    query: Optional[str]
    inputs: Optional[Dict[str, Any]] = Field(default_factory=dict)
    response_mode: Optional[ResponseMode]
    user: Optional[str]
    conversation_id: Optional[str] = ""
    files: Optional[List[File]] = []
    auto_generate_name: Optional[bool] = True


class ChatResponse(CompletionResponse):
    pass


class ChatSuggestRequest(BaseModel):
    user: Optional[str]


class ChatSuggestResponse(BaseModel):
    result: Optional[str]
    data: Optional[List[str]] = []
