# Setup Guide

## Prerequisites

### Python 3.10+
```bash
python3 --version
```

### Ollama (for local LLM)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
ollama pull qwen2.5:3b
```

### Piper TTS (for voice output)
```bash
# Debian/Ubuntu
sudo apt install piper-tts

# Or build from source:
# https://github.com/rhasspy/piper
```

### Playwright (for browser automation)
```bash
python3 -m playwright install chromium
```

### Audio
```bash
# ALSA (usually pre-installed on Linux)
sudo apt install alsa-utils
```

## Installation

```bash
cd jarvis
chmod +x setup.sh
./setup.sh
```

## Configuration

```bash
cp .env.example .env
# Edit .env with your API keys
```

## Voice Models

Download Piper voices to `voices/`:

- English: https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
- Hindi: https://huggingface.co/rhasspy/piper-voices/resolve/main/hi/hi_IN/pratham/medium/hi_IN-pratham-medium.onnx

Also download the corresponding .json files.

## Running

```bash
source venv/bin/activate

# Terminal chat
python -m jarvis.cli chat

# Voice mode
python -m jarvis.cli voice

# Web UI
python -m jarvis.cli web

# API server
python -m jarvis.cli server
```

## Testing

```bash
source venv/bin/activate
pytest tests/ -v
```

## Troubleshooting

### Ollama connection refused
Start Ollama: `ollama serve`

### No audio device
Check devices: `python3 -c "import sounddevice; print(sounddevice.query_devices())"`
Set `AUDIO_DEVICE` in `.env`

### Piper not found
Install piper-tts or add to PATH

### Playwright errors
`python3 -m playwright install chromium`

### Import errors
`source venv/bin/activate` then `pip install -r requirements.txt`
