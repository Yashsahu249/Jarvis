from pydantic import BaseModel, Field
from typing import Any
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    SAFE = "SAFE"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: str | None = None
    metadata: dict[str, Any] | None = None


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None
    stream: bool = True
    agent_id: str | None = None
    context: dict[str, Any] | None = None


class ChatResponse(BaseModel):
    message: ChatMessage
    conversation_id: str
    agent_id: str | None = None


class VoiceTranscribeRequest(BaseModel):
    file_path: str
    language: str | None = None
    model_size: str | None = None


class VoiceTranscribeResponse(BaseModel):
    text: str
    segments: list[dict[str, Any]] | None = None
    duration: float | None = None
    language: str | None = None


class VoiceSynthesizeRequest(BaseModel):
    text: str
    voice: str | None = None
    speed: float = 1.0


class VoiceSynthesizeResponse(BaseModel):
    audio_path: str
    duration: float | None = None


class AgentInfo(BaseModel):
    id: str
    name: str
    role: str
    status: str
    model: str | None = None
    capabilities: list[str] = []
    metadata: dict[str, Any] = {}


class AgentTask(BaseModel):
    id: str
    agent_id: str
    type: str
    description: str
    status: str = "pending"
    input: dict[str, Any] = {}
    output: Any = None
    created_at: str | None = None
    completed_at: str | None = None


class BrowserAction(BaseModel):
    action: str
    selector: str | None = None
    value: str | None = None
    url: str | None = None
    options: dict[str, Any] = {}


class BrowserState(BaseModel):
    url: str | None = None
    title: str | None = None
    tabs: list[dict[str, Any]] = []
    is_launched: bool = False


class BrowserScreenshot(BaseModel):
    base64: str | None = None
    file_path: str | None = None


class RepoInfo(BaseModel):
    id: str
    name: str
    url: str
    local_path: str
    branch: str | None = None
    description: str | None = None
    last_analyzed: str | None = None
    size_bytes: int | None = None
    file_count: int | None = None


class RepoFile(BaseModel):
    path: str
    name: str
    type: str
    size: int | None = None
    language: str | None = None
    children: list["RepoFile"] | None = None


class MemoryEntry(BaseModel):
    id: str
    type: str
    content: str
    metadata: dict[str, Any] = {}
    created_at: str
    updated_at: str | None = None
    importance: float | None = None


class MemorySearchResult(BaseModel):
    query: str
    results: list[MemoryEntry]
    total: int
    time_taken: float | None = None


class SystemStatus(BaseModel):
    status: str
    version: str
    uptime: float
    cpu_percent: float
    memory_percent: float
    active_agents: int
    active_browsers: int
    llm_provider: str
    llm_connected: bool


class SystemMetrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    uptime_seconds: float
    active_connections: int
    requests_total: int
    requests_per_minute: float
    avg_response_time_ms: float
    timestamp: str


class CommandExecuteRequest(BaseModel):
    command: str
    shell: bool = False
    timeout: int = 30
    workdir: str | None = None
    env: dict[str, str] | None = None


class CommandExecuteResponse(BaseModel):
    exit_code: int
    stdout: str
    stderr: str
    risk_level: RiskLevel | None
    confirmed: bool = True
    duration: float | None = None


class RepoCloneRequest(BaseModel):
    url: str
    name: str | None = None
    branch: str | None = None
    depth: int | None = None


class RepoAnalyzeRequest(BaseModel):
    task: str
    files: list[str] | None = None
    context: str | None = None


class RepoSearchRequest(BaseModel):
    query: str
    file_pattern: str | None = None
    max_results: int = 20


class MemorySearchRequest(BaseModel):
    query: str
    limit: int = 10
    type: str | None = None


class ToolInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    parameters: dict[str, Any] = {}
    risk_level: RiskLevel = RiskLevel.SAFE


class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str
    module: str | None = None
    line: int | None = None
