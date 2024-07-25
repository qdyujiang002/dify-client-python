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
    total_tokens: Optional[int]
    total_price: Optional[str]
    currency: Optional[str]


class WorkflowStartedData(BaseModel):
    id: Optional[str]  # workflow run id
    workflow_id: Optional[str]  # workflow id
    sequence_number: Optional[int]
    inputs: Optional[dict] = None
    created_at: Optional[int]  # unix timestamp seconds


class NodeStartedData(BaseModel):
    id: Optional[str]  # workflow run id
    node_id: Optional[str]
    node_type: Optional[str]
    title: Optional[str]
    index: Optional[int]
    predecessor_node_id: Optional[str] = None
    inputs: Optional[dict] = None
    created_at: Optional[int]
    extras: Optional[dict] = {}


class NodeFinishedData(BaseModel):
    id: Optional[str]  # workflow run id
    node_id: Optional[str]
    node_type: Optional[str]
    title: Optional[str]
    index: Optional[int]
    predecessor_node_id: Optional[str] = None
    inputs: Optional[dict] = None
    process_data: Optional[dict] = None
    outputs: Optional[dict] = {}
    status: WorkflowStatus
    error: Optional[str] = None
    elapsed_time: Optional[float]  # seconds
    execution_metadata: Optional[ExecutionMetadata] = None
    created_at: Optional[int]
    finished_at: Optional[int]
    files: List = []


class WorkflowFinishedData(BaseModel):
    id: Optional[str]  # workflow run id
    workflow_id: Optional[str]  # workflow id
    sequence_number: Optional[int]
    status: WorkflowStatus
    outputs: Optional[dict]
    error: Optional[str]
    elapsed_time: Optional[float]
    total_tokens: Optional[int]
    total_steps: Optional[int] = 0
    created_at: Optional[int]
    finished_at: Optional[int]
    created_by: Optional[dict] = {}
    files: Optional[List] = []


class WorkflowsRunRequest(BaseModel):
    inputs: Dict = {}
    response_mode: ResponseMode
    user: str
    conversation_id: Optional[str] = ""
    files: List[File] = []


class WorkflowsRunResponse(BaseModel):
    log_id: Optional[str]
    task_id: Optional[str]
    workflow_run_id: Optional[str]
    data: WorkflowFinishedData
