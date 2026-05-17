# Jarvis Architecture

## System Layers

### 1. Interface Layer
- **CLI** (`cli.py`): Argparse-based command entry point
- **Terminal UI** (`ui/tui.py`): Interactive chat loop
- **Streamlit UI** (`ui/streamlit_app.py`): Web-based chat
- **Voice UI** (`ui/voice_ui.py`): Voice conversation loop
- **FastAPI Server** (`main.py`): REST API for external integration

### 2. Intent Layer
Routes user input to appropriate handlers - chat processing, tool execution, or agent delegation.

### 3. LLM Provider Layer (`llm/`)
Abstract interface with multiple implementations:
- `base.py`: Abstract provider
- `ollama_provider.py`: Local Ollama inference
- `groq_provider.py`: Cloud Groq inference
- `openrouter_provider.py`: OpenRouter multi-model access
- `gemini_provider.py`: Google Gemini API
- `router.py`: Auto-fallback and provider selection

### 4. Memory Layer (`memory/`)
Persistent storage using SQLite:
- `store.py`: Core database operations
- `conversation.py`: Chat history management
- `semantic.py`: Vector-search ready interface

### 5. Tool System (`tools/`)
Extensible tool registry:
- `base.py`: Abstract tool interface
- `filesystem.py`: File read/write/list
- `shell.py`: Safe command execution
- `git_tool.py`: Git operations
- `code.py`: Code file manipulation
- `browser_tool.py`: Playwright browser control
- `python_tool.py`: Sandboxed Python execution
- `registry.py`: Central tool registration

### 6. Safety Layer (`safety/`)
- `permissions.py`: Risk classification
- `sandbox.py`: Isolated execution
- `audit.py`: Execution logging

### 7. Reasoning Layer (`reasoning/`)
- `thinker.py`: Strategic analysis
- `critic.py`: Self-critique
- `planner.py`: Task decomposition

### 8. Agent System (`agents/`)
- `base.py`: Abstract agent
- `planner.py`: Task planning
- `coder.py`: Code generation
- `browser_agent.py`: Web automation
- `memory_agent.py`: Memory management
- `research.py`: Research
- `execution.py`: Tool execution
- `orchestrator.py`: Inter-agent delegation

## Data Flow

```
User Input
  -> Interface (CLI/Web/Voice)
    -> Conversation Manager (memory)
      -> Build Context (system + history + memories)
        -> LLM Provider (with auto-fallback)
          -> Stream Response
            -> Save to Memory
              -> Display/Play Response
```

## Safety Architecture

Commands classified as:
- **SAFE**: Auto-executed (ls, pwd, cat, git status)
- **MEDIUM**: Confirmation required (rm, mv, docker)
- **HIGH**: Blocked entirely (shutdown, mkfs, sudo)

Tool actions follow same pattern via PermissionSystem.
