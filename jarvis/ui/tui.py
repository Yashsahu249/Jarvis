import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from jarvis.llm.router import get_llm_router
from jarvis.memory.conversation import get_conversation_manager
from jarvis.system_prompts.jarvis import SYSTEM_PROMPT
from jarvis.utils.helpers import detect_language
from jarvis.utils.logger import JarvisLogger


class TerminalUI:
    def __init__(self):
        self.logger = JarvisLogger.get_logger("ui.terminal")
        self.llm = get_llm_router()
        self.cm = get_conversation_manager()
        self.running = True

    def print_banner(self):
        banner = """
    ╔══════════════════════════════════════╗
    ║            JARVIS v1.0              ║
    ║   Local AI Operating System         ║
    ╚══════════════════════════════════════╝
        """
        print(banner)
        print(f"Provider: {self.llm.active_provider}")
        print(f"Model: {self.llm.get_provider().model_name}")
        print("Type 'exit' to quit, 'clear' to reset memory\n")

    async def chat_loop(self):
        self.print_banner()

        while self.running:
            try:
                user_input = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye.")
                break

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Goodbye.")
                break

            if user_input.lower() == "clear":
                self.cm.clear()
                print("Memory cleared.\n")
                continue

            self.cm.add_user_message(user_input)
            context = self.cm.build_context(SYSTEM_PROMPT)

            print("\nJarvis: ", end="", flush=True)
            full_response = ""

            try:
                stream = await self.llm.generate(context, stream=True)

                if hasattr(stream, "__aiter__"):
                    async for chunk in stream:
                        print(chunk, end="", flush=True)
                        full_response += chunk
                else:
                    print(stream, end="", flush=True)
                    full_response = stream

                print("\n")

            except Exception as e:
                error_msg = f"Error: {e}"
                print(error_msg)
                full_response = error_msg

            self.cm.add_assistant_message(full_response)


def main():
    ui = TerminalUI()
    asyncio.run(ui.chat_loop())


if __name__ == "__main__":
    main()
