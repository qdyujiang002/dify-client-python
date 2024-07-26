try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum
from http import HTTPStatus
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class Mode(StrEnum):
    WORKFLOW = "workflow"
    ADVANCED_CHAT = "advanced-chat"
    AGENT_CHAT = "agent-chat"
    COMPLETION = "completion"


class ResponseMode(StrEnum):
    STREAMING = 'streaming'
    BLOCKING = 'blocking'


class FileType(StrEnum):
    IMAGE = "image"


class TransferMethod(StrEnum):
    REMOTE_URL = "remote_url"
    LOCAL_FILE = "local_file"


# Allows the entry of various variable values defined by the App.
# The inputs parameter contains multiple key/value pairs, with each key corresponding to a specific variable and
# each value being the specific value for that variable.
# The text generation application requires at least one key/value pair to be inputted.
class CompletionInputs(BaseModel):
    model_config = ConfigDict(extra='allow')
    # Required The input text, the content to be processed.
    query: Optional[str] = None


class File(BaseModel):
    type: Optional[FileType] = None
    transfer_method: Optional[TransferMethod] = None
    url: Optional[str] = None
    # Uploaded file ID, which must be obtained by uploading through the File Upload API in advance
    # (when the transfer method is local_file)
    upload_file_id: Optional[str] = None


class Usage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None

    prompt_unit_price: Optional[str] = None
    prompt_price_unit: Optional[str] = None
    prompt_price: Optional[str] = None
    completion_unit_price: Optional[str] = None
    completion_price_unit: Optional[str] = None
    completion_price: Optional[str] = None
    total_price: Optional[str] = None
    currency: Optional[str] = None

    latency: Optional[float] = None


class RetrieverResource(BaseModel):
    position: Optional[int] = None
    dataset_id: Optional[str] = None
    dataset_name: Optional[str] = None
    document_id: Optional[str] = None
    document_name: Optional[str] = None
    segment_id: Optional[str] = None
    score: Optional[float] = None
    content: Optional[str] = None


class Metadata(BaseModel):
    usage: Optional[Usage] = None
    retriever_resources: Optional[List[RetrieverResource]] = []


class StopRequest(BaseModel):
    user: Optional[str] = None


class StopResponse(BaseModel):
    result: Optional[str] = None  # success


class ErrorResponse(BaseModel):
    status: Optional[int] = HTTPStatus.INTERNAL_SERVER_ERROR  # HTTP status code
    code: Optional[str] = ""
    message: Optional[str] = ""
