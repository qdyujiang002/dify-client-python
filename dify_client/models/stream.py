try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum
from typing import Union, Optional, List

from pydantic import BaseModel, ConfigDict, field_validator

from dify_client import utils
from dify_client.models.base import Metadata, ErrorResponse
from dify_client.models.workflow import WorkflowStartedData, WorkflowFinishedData, NodeStartedData, NodeFinishedData

STREAM_EVENT_KEY = "event"


class StreamEvent(StrEnum):
    MESSAGE = "message"
    AGENT_MESSAGE = "agent_message"
    AGENT_THOUGHT = "agent_thought"
    MESSAGE_FILE = "message_file"  # need to show file
    WORKFLOW_STARTED = "workflow_started"
    NODE_STARTED = "node_started"
    NODE_FINISHED = "node_finished"
    WORKFLOW_FINISHED = "workflow_finished"
    MESSAGE_END = "message_end"
    MESSAGE_REPLACE = "message_replace"
    ERROR = "error"
    PING = "ping"
    TTS_MESSAGE_END = 'tts_message_end'
    ITERATION_STARTED = 'iteration_started'
    ITERATION_NEXT = 'iteration_next'
    ITERATION_END = 'iteration_end'
    ITERATION_COMPLETED = 'iteration_completed'
    PARALLEL_BRANCH_STARTED = 'parallel_branch_started'
    PARALLEL_BRANCH_END = 'parallel_branch_end'
    PARALLEL_BRANCH_COMPLETED = 'parallel_branch_completed'
    PARALLEL_BRANCH_FINISHED = 'parallel_branch_finished'



    @classmethod
    def new(cls, event: Union["StreamEvent", str]) -> "StreamEvent":
        if isinstance(event, cls):
            return event
        return utils.str_to_enum(cls, event)


class StreamResponse(BaseModel):
    model_config = ConfigDict(extra='allow')

    event: StreamEvent
    task_id: Optional[str] = ""

    @field_validator("event", mode="before")
    def transform_stream_event(cls, event: Union[StreamEvent, str]) -> StreamEvent:
        return StreamEvent.new(event)


class PingResponse(StreamResponse):
    pass


class ErrorStreamResponse(StreamResponse, ErrorResponse):
    message_id: Optional[str] = ""


class MessageStreamResponse(StreamResponse):
    message_id: Optional[str] = None
    conversation_id: Optional[str] = ""
    answer: Optional[str] = None
    created_at: Optional[int] = None  # unix timestamp seconds


class MessageEndStreamResponse(StreamResponse):
    message_id: Optional[str] = None
    conversation_id: Optional[str] = ""
    created_at: Optional[int] = None  # unix timestamp seconds
    metadata: Optional[Metadata] = None


class MessageReplaceStreamResponse(MessageStreamResponse):
    message_id: Optional[str] = None
    conversation_id: Optional[str] = ""
    created_at: Optional[int] = None  # unix timestamp seconds
    answer: Optional[str] = None


class TTSMessageEndStreamResponse(StreamResponse):
    audio: Optional[str] = ""
    created_at: Optional[int] = None  # unix timestamp seconds
    message_id: Optional[str] = None
    conversation_id: Optional[str] = ""
    answer: Optional[str] = ""


class AgentMessageStreamResponse(MessageStreamResponse):
    pass


class AgentThoughtStreamResponse(StreamResponse):
    id: Optional[str] = None  # agent thought id
    message_id: Optional[str] = None
    conversation_id: Optional[str] = None
    position: Optional[int] = None  # thought position, start from 1
    thought: Optional[str] = None
    observation: Optional[str] = None
    tool: Optional[str] = None
    tool_input: Optional[str] = None
    message_files: Optional[List[str]] = []
    created_at: Optional[int] = None  # unix timestamp seconds


class MessageFileStreamResponse(StreamResponse):
    id: Optional[str] = None  # file id
    conversation_id: Optional[str] = None
    type: Optional[str] = None  # only image
    belongs_to: Optional[str] = None  # assistant
    url: Optional[str] = None


class WorkflowsStreamResponse(StreamResponse):
    workflow_run_id: Optional[str] = None
    data: Optional[Union[
        WorkflowStartedData,
        WorkflowFinishedData,
        NodeStartedData,
        NodeFinishedData]
    ]


class ChatWorkflowsStreamResponse(WorkflowsStreamResponse):
    message_id: Optional[str] = None
    conversation_id: Optional[str] = None
    created_at: Optional[int] = None


_COMPLETION_EVENT_TO_STREAM_RESP_MAPPING = {
    StreamEvent.PING: PingResponse,
    StreamEvent.MESSAGE: MessageStreamResponse,
    StreamEvent.MESSAGE_END: MessageEndStreamResponse,
    StreamEvent.MESSAGE_REPLACE: MessageReplaceStreamResponse,
    StreamEvent.TTS_MESSAGE_END: MessageEndStreamResponse
}

CompletionStreamResponse = Union[
    PingResponse,
    MessageStreamResponse,
    MessageEndStreamResponse,
    MessageReplaceStreamResponse,
    TTSMessageEndStreamResponse
]


def build_completion_stream_response(data: dict) -> CompletionStreamResponse:
    event = StreamEvent.new(data.get(STREAM_EVENT_KEY))
    return _COMPLETION_EVENT_TO_STREAM_RESP_MAPPING.get(event, StreamResponse)(**data)


_CHAT_EVENT_TO_STREAM_RESP_MAPPING = {
    StreamEvent.PING: PingResponse,
    # chat
    StreamEvent.MESSAGE: MessageStreamResponse,
    StreamEvent.MESSAGE_END: MessageEndStreamResponse,
    StreamEvent.MESSAGE_REPLACE: MessageReplaceStreamResponse,
    StreamEvent.MESSAGE_FILE: MessageFileStreamResponse,
    StreamEvent.TTS_MESSAGE_END: TTSMessageEndStreamResponse,
    # agent
    StreamEvent.AGENT_MESSAGE: AgentMessageStreamResponse,
    StreamEvent.AGENT_THOUGHT: AgentThoughtStreamResponse,
    # workflow
    StreamEvent.WORKFLOW_STARTED: WorkflowsStreamResponse,
    StreamEvent.NODE_STARTED: WorkflowsStreamResponse,
    StreamEvent.NODE_FINISHED: WorkflowsStreamResponse,
    StreamEvent.WORKFLOW_FINISHED: WorkflowsStreamResponse,
}

ChatStreamResponse = Union[
    PingResponse,
    MessageStreamResponse,
    MessageEndStreamResponse,
    MessageReplaceStreamResponse,
    MessageFileStreamResponse,
    AgentMessageStreamResponse,
    AgentThoughtStreamResponse,
    WorkflowsStreamResponse,
    TTSMessageEndStreamResponse
]


def build_chat_stream_response(data: dict) -> ChatStreamResponse:
    event = StreamEvent.new(data.get(STREAM_EVENT_KEY))
    return _CHAT_EVENT_TO_STREAM_RESP_MAPPING.get(event, StreamResponse)(**data)


_WORKFLOW_EVENT_TO_STREAM_RESP_MAPPING = {
    StreamEvent.PING: PingResponse,
    StreamEvent.TTS_MESSAGE_END: TTSMessageEndStreamResponse,
    # workflow
    StreamEvent.WORKFLOW_STARTED: WorkflowsStreamResponse,
    StreamEvent.NODE_STARTED: WorkflowsStreamResponse,
    StreamEvent.NODE_FINISHED: WorkflowsStreamResponse,
    StreamEvent.WORKFLOW_FINISHED: WorkflowsStreamResponse,
}

WorkflowsRunStreamResponse = Union[
    PingResponse,
    WorkflowsStreamResponse,
]


def build_workflows_stream_response(data: dict) -> WorkflowsRunStreamResponse:
    event = StreamEvent.new(data.get(STREAM_EVENT_KEY))
    return _WORKFLOW_EVENT_TO_STREAM_RESP_MAPPING.get(event, StreamResponse)(**data)
