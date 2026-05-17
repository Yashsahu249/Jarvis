import asyncio
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jarvis.utils.logger import JarvisLogger


def main():
    parser = argparse.ArgumentParser(
        description="Jarvis - Local AI Operating System Assistant"
    )
    parser.add_argument(
        "mode",
        nargs="?",
        default="chat",
        choices=["chat", "voice", "server", "web", "tui"],
        help="Operating mode (default: chat)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Server port (default: 8000)",
    )
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="Server host (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--provider",
        type=str,
        default=None,
        help="LLM provider (ollama, groq, openrouter, gemini)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Model name override",
    )

    args = parser.parse_args()

    logger = JarvisLogger.get_logger("cli")
    logger.info(f"Starting Jarvis in {args.mode} mode")

    if args.mode == "chat":
        from jarvis.ui.tui import TerminalUI

        ui = TerminalUI()
        asyncio.run(ui.chat_loop())

    elif args.mode == "voice":
        from jarvis.ui.voice_ui import VoiceUI

        ui = VoiceUI()
        asyncio.run(ui.chat_loop())

    elif args.mode == "server":
        import uvicorn
        from jarvis.config.settings import get_settings

        s = get_settings()
        uvicorn.run(
            "jarvis.main:app",
            host=args.host or s.HOST,
            port=args.port or s.PORT,
            reload=s.DEBUG,
        )

    elif args.mode == "web":
        import subprocess

        streamlit_path = Path(__file__).parent / "ui" / "streamlit_app.py"
        subprocess.run(["streamlit", "run", str(streamlit_path)])

    elif args.mode == "tui":
        from jarvis.ui.tui import TerminalUI

        ui = TerminalUI()
        asyncio.run(ui.chat_loop())


if __name__ == "__main__":
    main()
