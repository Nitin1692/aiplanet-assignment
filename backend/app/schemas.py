from pydantic import BaseModel, Field
from typing import Any, List, Optional

class WorkflowCreate(BaseModel):
    name: str
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]

class WorkflowOut(WorkflowCreate):
    id: int
    class Config:
        from_attributes = True

class RunWorkflowRequest(BaseModel):
    session_id: Optional[int] = None
    query: str
    custom_prompt: Optional[str] = None

class RunWorkflowResponse(BaseModel):
    session_id: int
    answer: str
    used_context: Optional[str] = None
    web_snippets: Optional[list[str]] = None

class ChatMessageOut(BaseModel):
    role: str
    content: str

class ChatHistoryOut(BaseModel):
    session_id: int
    messages: list[ChatMessageOut]