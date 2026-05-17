#!/usr/bin/env bash
set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() { echo -e "${BLUE}[JARVIS]${NC} $1"; }
print_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
print_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
print_err() { echo -e "${RED}[ERR]${NC} $1"; }

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        Jarvis Setup Script          ║"
echo "╚══════════════════════════════════════╝"
echo ""

# Check Python
print_status "Checking Python..."
if command -v python3 &>/dev/null; then
    PYTHON=$(command -v python3)
    print_ok "Python found: $($PYTHON --version)"
else
    print_err "Python 3 not found. Install python3 first."
    exit 1
fi

# Check pip
print_status "Checking pip..."
if command -v pip3 &>/dev/null; then
    print_ok "pip found"
else
    print_err "pip3 not found"
    exit 1
fi

# Check/Setup venv
if [ ! -d "venv" ]; then
    print_status "Creating virtual environment..."
    $PYTHON -m venv venv
    print_ok "Virtual environment created"
fi
source venv/bin/activate
print_ok "Virtual environment activated"

# Install requirements
print_status "Installing Python dependencies..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
print_ok "Dependencies installed"

# Check Ollama
print_status "Checking Ollama..."
if command -v ollama &>/dev/null; then
    print_ok "Ollama found"
    # Check if running
    if curl -s http://127.0.0.1:11434/api/tags &>/dev/null; then
        print_ok "Ollama is running"
        print_status "Available models:"
        ollama list 2>/dev/null || true
    else
        print_warn "Ollama not running. Start with: ollama serve"
        print_warn "Then pull models: ollama pull qwen2.5:3b"
    fi
else
    print_warn "Ollama not found. Install from: https://ollama.com"
fi

# Check Piper
print_status "Checking Piper TTS..."
if command -v piper &>/dev/null; then
    print_ok "Piper found"
else
    print_warn "Piper not found. Install with:"
    print_warn "  sudo apt install piper-tts"
    print_warn "  or build from: https://github.com/rhasspy/piper"
fi

# Check Audio
print_status "Checking audio..."
if command -v aplay &>/dev/null; then
    print_ok "aplay found"
else
    print_warn "aplay not found (ALSA)"
fi

# Check Playwright
print_status "Checking Playwright..."
if python3 -c "import playwright" 2>/dev/null; then
    print_status "Installing Playwright browsers..."
    python3 -m playwright install chromium 2>/dev/null || print_warn "Playwright browsers not installed"
    print_ok "Playwright ready"
else
    print_warn "Playwright will be installed with requirements"
fi

# Voice models check
print_status "Checking voice models..."
if [ -f "voices/en_US-lessac-medium.onnx" ] && [ -f "voices/hi_IN-pratham-medium.onnx" ]; then
    print_ok "Voice models found"
else
    print_warn "Voice models missing. Download from:"
    print_warn "  https://huggingface.co/rhasspy/piper-voices"
    print_warn "  Place .onnx and .json files in voices/"
fi

# Create .env if missing
if [ ! -f ".env" ]; then
    print_status "Creating .env from .env.example..."
    cp .env.example .env
    print_ok ".env created - edit with your API keys"
fi

# Create data dirs
print_status "Creating data directories..."
mkdir -p data/logs repos
print_ok "Data directories created"

echo ""
echo "╔══════════════════════════════════════╗"
echo "║        Setup Complete!              ║"
echo "╚══════════════════════════════════════╝"
echo ""
echo "Run Jarvis:"
echo "  source venv/bin/activate"
echo "  python -m jarvis.cli chat      # Terminal chat"
echo "  python -m jarvis.cli voice     # Voice mode"
echo "  python -m jarvis.cli server    # API server"
echo "  python -m jarvis.cli web       # Streamlit UI"
echo ""
