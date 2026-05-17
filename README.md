# Jarvis - Local AI Operating System Assistant

A production-style local AI operating system assistant with voice conversation, multilingual support, browser automation, coding workflows, long-term memory, and autonomous task execution.

## Architecture

```
User Interface (CLI / Voice / Web / API)
        |
   Intent Layer
        |
   Tool Router
        |
   Memory Layer (SQLite)
        |
   Reasoning Layer
        |
   LLM Provider Layer (Ollama / Groq / OpenRouter / Gemini)
        |
   Response Layer
```

## Quick Start

```bash
git clone <repo>
cd jarvis
chmod +x setup.sh
./setup.sh
source venv/bin/activate
python -m jarvis.cli chat
```

## Modes

| Mode | Command | Description |
|------|---------|-------------|
| Chat | `python -m jarvis.cli chat` | Terminal chat interface |
| Voice | `python -m jarvis.cli voice` | Voice conversation (wake word: jarvis) |
| Server | `python -m jarvis.cli server` | FastAPI server on :8000 |
| Web UI | `python -m jarvis.cli web` | Streamlit web interface |

## LLM Providers

- **Ollama** (default) - Local inference with qwen2.5:3b or mistral
- **Groq** - Fast cloud inference
- **OpenRouter** - Multi-model access
- **Gemini** - Google's models

Set `LLM_PROVIDER` in `.env` to switch. Falls back automatically if one fails.

## Features

- **Voice**: Speech-to-text (faster-whisper), TTS (Piper), wake word detection, Hindi/English/Hinglish
- **Memory**: Persistent SQLite storage, conversation history, semantic search, summarization
- **Tools**: Filesystem, shell, git, code editing, browser automation (Playwright), Python execution
- **Safety**: Permission system, sandboxing, audit logging, command classification
- **Multi-Agent**: Planner, coder, browser, memory, research, execution agents with orchestration
- **Strategic Thinking**: Self-critique, reasoning analysis, task planning

## Configuration

Copy `.env.example` to `.env` and configure:

```env
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5:3b
OPENROUTER_API_KEY=sk-or-v1-...
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIza...
```

## Project Structure

```
jarvis/
├── jarvis/
│   ├── cli.py              # CLI entry point
│   ├── main.py             # FastAPI server
│   ├── config/             # Configuration
│   ├── llm/                # LLM provider abstraction
│   ├── voice/              # STT, TTS, VAD, wake word
│   ├── memory/             # SQLite store, conversation
│   ├── tools/              # Tool system & registry
│   ├── agents/             # Multi-agent orchestration
│   ├── reasoning/          # Strategic thinking
│   ├── safety/             # Permissions & audit
│   ├── ui/                 # Streamlit, TUI, Voice UI
│   └── utils/              # Logger, helpers
├── tests/                  # Test suite
├── docs/                   # Documentation
├── voices/                 # TTS voice models
├── data/                   # Runtime data
└── setup.sh               # Setup script
```

## Requirements

- Python 3.10+
- Ollama (for local inference)
- Piper TTS (for voice output)
- Playwright (for browser automation)
- Microphone (for voice input)

## License

MIT
