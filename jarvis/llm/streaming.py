from typing import AsyncGenerator


async def collect_stream(stream: AsyncGenerator[str, None]) -> str:
    chunks = []
    async for chunk in stream:
        chunks.append(chunk)
    return "".join(chunks)
