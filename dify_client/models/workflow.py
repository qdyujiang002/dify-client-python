try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel

from dify_client.models.base import ResponseMode, File


class WorkflowStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    STOPPED = "stopped"


class ExecutionMetadata(BaseModel):
    total_tokens: Optional[int] = None
    total_price: Optional[str] = None
    currency: Optional[str] = None


class WorkflowStartedData(BaseModel):
    id: Optional[str] = None  # workflow run id
    workflow_id: Optional[str] = None  # workflow id
    sequence_number: Optional[int] = None
    inputs: Optional[dict] = None
    created_at: Optional[int] = None  # unix timestamp seconds


class NodeStartedData(BaseModel):
    id: Optional[str] = None  # workflow run id
    node_id: Optional[str] = None
    node_type: Optional[str] = None
    title: Optional[str] = None
    index: Optional[int] = None
    predecessor_node_id: Optional[str] = None
    inputs: Optional[dict] = None
    created_at: Optional[int] = None
    extras: Optional[dict] = {}


class NodeFinishedData(BaseModel):
    id: Optional[str] = None  # workflow run id
    node_id: Optional[str] = None
    node_type: Optional[str] = None
    title: Optional[str] = None
    index: Optional[int] = None
    predecessor_node_id: Optional[str] = None
    inputs: Optional[dict] = None
    process_data: Optional[dict] = None
    outputs: Optional[dict] = {}
    status: WorkflowStatus
    error: Optional[str] = None
    elapsed_time: Optional[float] = None  # seconds
    execution_metadata: Optional[ExecutionMetadata] = None
    created_at: Optional[int] = None
    finished_at: Optional[int] = None
    files: Optional[List] = []


class WorkflowFinishedData(BaseModel):
    id: Optional[str] = None  # workflow run id
    workflow_id: Optional[str] = None  # workflow id
    sequence_number: Optional[int] = None
    status: WorkflowStatus
    outputs: Optional[dict] = None
    error: Optional[str] = None
    elapsed_time: Optional[float] = None
    total_tokens: Optional[int] = None
    total_steps: Optional[int] = 0
    created_at: Optional[int] = None
    finished_at: Optional[int] = None
    created_by: Optional[dict] = {}
    files: Optional[List] = []


class WorkflowsRunRequest(BaseModel):
    inputs: Dict = {}
    response_mode: ResponseMode
    user: str = None
    conversation_id: Optional[str] = ""
    files: List[File] = []


class WorkflowsRunResponse(BaseModel):
    log_id: Optional[str] = None
    task_id: Optional[str] = None
    workflow_run_id: Optional[str] = None
    data: WorkflowFinishedData
