from typing import Literal, Optional
from pydantic import BaseModel, Field

RunMode = Literal["deepseek", "local"]

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    mode: RunMode
    session_id: str = "default"

class DebugInfo(BaseModel):
    mode: str
    route: str
    sources: list[dict] = []
    tools: list[dict] = []

class ChatResponse(BaseModel):
    answer: str
    debug: DebugInfo
