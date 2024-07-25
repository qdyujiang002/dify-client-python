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
    query: Optional[str]


class File(BaseModel):
    type: Optional[FileType]
    transfer_method: Optional[TransferMethod]
    url: Optional[str]
    # Uploaded file ID, which must be obtained by uploading through the File Upload API in advance
    # (when the transfer method is local_file)
    upload_file_id: Optional[str]


class Usage(BaseModel):
    prompt_tokens: Optional[int]
    completion_tokens: Optional[int]
    total_tokens: Optional[int]

    prompt_unit_price: Optional[str]
    prompt_price_unit: Optional[str]
    prompt_price: Optional[str]
    completion_unit_price: Optional[str]
    completion_price_unit: Optional[str]
    completion_price: Optional[str]
    total_price: Optional[str]
    currency: Optional[str]

    latency: Optional[float]


class RetrieverResource(BaseModel):
    position: Optional[int]
    dataset_id: Optional[str]
    dataset_name: Optional[str]
    document_id: Optional[str]
    document_name: Optional[str]
    segment_id: Optional[str]
    score: Optional[float]
    content: Optional[str]


class Metadata(BaseModel):
    usage: Optional[Usage]
    retriever_resources: Optional[List[RetrieverResource]] = []


class StopRequest(BaseModel):
    user: Optional[str]


class StopResponse(BaseModel):
    result: Optional[str]  # success


class ErrorResponse(BaseModel):
    status: Optional[int] = HTTPStatus.INTERNAL_SERVER_ERROR  # HTTP status code
    code: Optional[str] = ""
    message: Optional[str] = ""
